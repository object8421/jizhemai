# -*- coding: utf-8 -*-
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bottle import Bottle, request, route, run,template
import sae
import sae.kvdb
import time
from time import localtime, strftime
import hashlib
import xml.etree.ElementTree as ET
import random
import string
sae.add_vendor_dir('vendor')
import json
import requests
import pylibmc as memcache
from qiniu import Auth
from qiniu import BucketManager

app = Bottle()
mc = memcache.Client()
kv = sae.kvdb.Client()

@app.route('/wxserv')
def check_signature():
	'''
	wechat access verification
	'''
	token = "jizhemai"
	signature = request.GET.get('signature',None)
	timestamp = request.GET.get('timestamp',None)
	nonce = request.GET.get('nonce',None)
	echostr = request.GET.get('echostr',None)
	L = [token,timestamp,nonce]
	L.sort()
	s=L[0]+L[1]+L[2]
	if hashlib.sha1(s).hexdigest() == signature:
		return echostr
	else:
		return None

def parse_xml_msg():
	recv_xml = request.body.read()
	root = ET.fromstring(recv_xml)
	msg = {}
	for child in root:
		msg[child.tag] = child.text
	return msg

@app.route('/wxserv', method = 'POST')
def response_wechat():
	'''
	response in wechat platform
	'''
	msg = parse_xml_msg()
	
	response_msg = '''
	<xml>
	<ToUserName><![CDATA[%s]]></ToUserName>
	<FromUserName><![CDATA[%s]]></FromUserName>
	<CreateTime>%s</CreateTime>
	<MsgType><![CDATA[text]]></MsgType>
	<Content><![CDATA[%s]]></Content>
	</xml>
	'''
	HELP = '''
	111
	'''

	if msg['MsgType'] == 'event':
		if msg['Event'] == 'subscribe':
			echo_str = HELP
			echo_msg = response_msg % (
				msg['FromUserName'],msg['ToUserName'],str(int(time.time())),echo_str)
			return echo_msg
	elif msg['MsgType'] == 'text':
		pass


	if msg['MsgType'] == 'image':
		meid = msg['MediaId']
		userid = msg['FromUserName']
		s_userid = userid[:10]
		s_meid = meid[:6]

		at_extime_comp = mc.get("at_ex_time")
		at_use = mc.get("at_at")
		if at_extime_comp < time.time():
			at_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=xxx&secret=xxx"
			at_response = requests.get(at_url)
			at_res = json.loads(at_response.text)['access_token']
			mc.set("at_at", at_res)
			at_ex_time = int(time.time()) + 7000
			mc.set("at_ex_time",at_ex_time)
			at_use = mc.get("at_at")
		
		wx_pic_url = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s" % (at_use,meid)
		qn_fname = s_userid + s_meid +".jpg"

		bucket_name = 'jizhemai'
		qn_access_key = 'xxx'
		qn_secret_key = 'xxx'
		q = Auth(qn_access_key, qn_secret_key)
		bucket = BucketManager(q)
		ret, info = bucket.fetch(wx_pic_url, bucket_name, qn_fname)
		up_full_id = s_userid + ('full') + s_meid
		up_prev_id = s_userid + ('prev') + s_meid
		up_full_id_prefix = s_userid + ('full')
		up_prev_id_prefix = s_userid + ('prev')
		view_url_temp = ('http://7xp96y.com1.z0.glb.clouddn.com/') + qn_fname
		view_url_full = view_url_temp + ('-full')
		view_url_prev = view_url_temp + ('-prev')
		kv.set (up_full_id,view_url_full)
		kv.set (up_prev_id,view_url_prev)
		pers_full_urls_dict = dict(kv.get_by_prefix(up_full_id_prefix, max_count=100, marker=None))
		pers_prev_urls_dict = dict(kv.get_by_prefix(up_prev_id_prefix, max_count=100, marker=None))
		pers_full_urls = list(pers_full_urls_dict.values())
		pers_prev_urls = list(pers_prev_urls_dict.values())
		echo_str = (pers_full_urls)
	elif msg['MsgType'] == 'text':
		echo_str = ('111')
	else:
		echo_str = ""
		
	echo_msg = response_msg % (
		msg['FromUserName'],msg['ToUserName'],str(int(time.time())),echo_str)
	
	return echo_msg

application = sae.create_wsgi_app(app)