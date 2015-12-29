# -*- coding: utf-8 -*-
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bottle import Bottle, request, route, run, response
from bottle import TEMPLATE_PATH, jinja2_template as template
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
import Cookie
import string
import StringIO
#from urllib import urlencode

app = Bottle()
mc = memcache.Client()
kv = sae.kvdb.Client()
c = Cookie.SimpleCookie() 

TEMPLATE_PATH.append("./templates")

wx_appid = ''
wx_secret = ''

def getAT():
    at_extime_comp = mc.get("at_ex_time")
    at_use = mc.get("at_at")
    if at_extime_comp < time.time():
        at_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx_appid&secret=wx_secret"
        at_response = requests.get(at_url)
        at_res = json.loads(at_response.text)['access_token']
        mc.set("at_at", at_res)
        at_ex_time = int(time.time()) + 7000
        mc.set("at_ex_time",at_ex_time)
        at_use = mc.get("at_at")
    return at_use

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
亲，欢迎使用《记着买》购物助手！
小二在此等待已久，请让我介绍一下使用方法吧：
1. 直接贴图片即可上传图片；
2. 输入all或者a可以浏览图片清单；
3. 在图片清单内点击相应的图片，
   可以查看或者编辑图片信息。
就素这么简单！来吧，快来使用吧，亲！
    '''

    if msg['MsgType'] == 'event':
        if msg['Event'] == 'subscribe':
            echo_str = HELP
            echo_msg = response_msg % (
                msg['FromUserName'],msg['ToUserName'],str(int(time.time())),echo_str)
            return echo_msg

        elif msg['Event'] == 'LOCATION':
            userid = msg['FromUserName']
            s_userid = userid[:10]
            lid = userid[:10] + ('_lbs')
            Latitude = msg['Latitude']
            Longitude = msg ['Longitude'] 
            Precision = msg['Precision']
            LOCATION = dict(Latitude = Latitude, Longitude = Longitude)
            kv.set (lid,LOCATION)

    elif msg['MsgType'] == 'text':
        pass


    if msg['MsgType'] == 'image':
        meid = msg['MediaId']
        userid = msg['FromUserName']
        s_userid = userid[:10]
        s_meid = meid[:6]
#   验证
        imgAT = getAT()
#   取微信图片到七牛      
        wx_pic_url = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s" % (imgAT,meid)
        s_picid = s_userid + s_meid
        qn_fname = s_userid + s_meid +".jpg"
        bucket_name = 'jizhemai'
        qn_access_key = ''
        qn_secret_key = ''
        q = Auth(qn_access_key, qn_secret_key)
        bucket = BucketManager(q)
        ret, info = bucket.fetch(wx_pic_url, bucket_name, qn_fname)
#   定义数据库中每张图片的key
        up_full_id = s_userid + ('full') + s_meid
        up_prev_id = s_userid + ('prev') + s_meid
#   生成图片链接
        view_url_temp = ('http://7xp96y.com1.z0.glb.clouddn.com/') + qn_fname
        view_url_full = view_url_temp + ('-full')
        view_url_prev = view_url_temp + ('-prev')

#   为了后面的调用，生成html
#        html_full_id = ('html_') + s_userid + ('full') + s_meid
        html_prev_id = ('html_') + s_userid + ('prev') + s_meid
        html_view_url_full = ('&lt;a href="http://jizhemai.sinaapp.com/show?') + s_picid + ('\"&gt;') + ('&lt;img src = \"') + view_url_prev + ('\"&gt;') + ('&lt;/a&gt;')
        kv.set (html_prev_id,html_view_url_full)
        html_prefix = ('html_') + s_userid
        pers_html_urls_dict = dict(kv.get_by_prefix(html_prefix, max_count=100, marker=None))
        pers_html_urls = list(pers_html_urls_dict.values())
        html_all_id = s_userid + ('_htmlall')
        kv.set (html_all_id,pers_html_urls)

#   保存图片上传链接
        kv.set (up_full_id,view_url_full)
        kv.set (up_prev_id,view_url_prev)

#   存图片地理信息 
        lid = userid[:10] + ('_lbs')
        picloc = kv.get(lid)
        full_loc_id = ('loc_') + up_full_id
        kv.set (full_loc_id,picloc)

#   用户上传图片清单处理
#       定义前缀，以备后面生成每个用户的个人上传清单使用
        up_full_id_prefix = s_userid + ('full')
        up_prev_id_prefix = s_userid + ('prev')
#       生成清单
        pers_full_urls_dict = dict(kv.get_by_prefix(up_full_id_prefix, max_count=100, marker=None))
        pers_prev_urls_dict = dict(kv.get_by_prefix(up_prev_id_prefix, max_count=100, marker=None))
        pers_full_urls = list(pers_full_urls_dict.values())
        pers_prev_urls = list(pers_prev_urls_dict.values())
#       保存清单
        upfull_all_id = s_userid + ('upfull')
        upprev_all_id = s_userid + ('upprev')
        kv.set (upfull_all_id,pers_full_urls)
        kv.set (upprev_all_id,pers_prev_urls)

        c['userid'] = s_userid
#        response.COOKIES['account'] = s_userid
#        response.COOKIES['userupp'] = up_prev_id
        echo_str = (pers_html_urls_dict)

    elif msg['Content'] == 'll':
        userid = msg['FromUserName']
        s_userid = userid[:10]
        c['userid'] = s_userid
        echo_str = ('https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx_appid&redirect_uri=http%3a%2f%2fjizhemai.sinaapp.com%2fall&response_type=code&scope=snsapi_userinfo#wechat_redirect')
    elif msg['Content'] == 'a':
        userid = msg['FromUserName']
        s_userid = userid[:10]
        c['userid'] = s_userid
        echo_str = ('http://jizhemai.sinaapp.com/all')
    elif msg['Content'] == 'all':
        userid = msg['FromUserName']
        s_userid = userid[:10]
        c['userid'] = s_userid
        echo_str = ('http://jizhemai.sinaapp.com/all')


    else:
        echo_str = HELP
        
    echo_msg = response_msg % (
        msg['FromUserName'],msg['ToUserName'],str(int(time.time())),echo_str)
    
    return echo_msg

### OAuth2.0
from wechatAPI import Wechat as wc

@app.route('/all')
def all():
#    user_code = request.query.get("code")
#    web_resp = requests.get('https://api.weixin.qq.com/sns/oauth2/access_token?appid=wx_appid&secret=wx_secret&code=user_code&grant_type=authorization_code')
#    web_access_token = json.loads(web_resp.text)['access_token']

# 以下是使用cookies
    wxcookies = c.output()
    wxctemp = wxcookies[-10:]

# 以下是生成图片链接信息   
    show_html_all_id = wxctemp + ('_htmlall')
    showhtmllist = kv.get (show_html_all_id)
    showhtml = "".join(showhtmllist)
#   以下是模板
    return showhtml

@app.route('/show')
def show():
# 以下是使用cookies
    wxcookies = c.output()
    wxctemp = wxcookies[-10:]

# 以下是地理信息








application = sae.create_wsgi_app(app)
