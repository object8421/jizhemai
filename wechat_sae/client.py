# -*- coding: utf-8 -*- 
# author: bambooom
'''
My Diary Web App - CLI for client
'''  
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from bs4 import BeautifulSoup
import time
import re

HELP = '''
Input h/help/? for help.
Input q/quit to quit the process.
Input s/sync to sync the diary log.
Input lt/ListTags to list all tags.
Input st:TAG to set or delete tags
Input FLUSH to clear all diary entries.
      e:MSG to start wechat test
Input e:?/h/H for help in wechat
Input e:s to see diary in wechat
Input e:d=<diary> to write diary in wechat
'''

url = "http://omoocpy.sinaapp.com/"

def get_log_all():
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	log = ''
	for i in soup.find_all('pre'):
		log += i.get_text()+'\n'
	return log

def get_log_bytag(tags):
	response = requests.get(url)
	soup = BeautifulSoup(response.text,"html.parser")
	ti=list(soup.find_all('i', class_='etime'))
	ta=list(soup.find_all('i', class_='tags'))
	di=list(soup.find_all('pre',class_='diary'))
	diary_tag = []
	for i in range(len(ti)):
		if tags in ta[i].get_text():
			diary_tag.append(ti[i].get_text()+"  "+di[i].get_text())
	return "\n".join(diary_tag)

def get_tags():
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	t = [i.get_text() for i in soup.find_all('i', class_='tags')] # list of lists
	t = [t[i].split(" ") for i in range(len(t))]
	t = [y for x in t for y in x] # one-dimensional list
	t1 = [t[i] for i in range(len(t)) if t[i].startswith('TAG:')]
	t2 = ['TAG:'+t[i] for i in range(len(t)) if not t[i].startswith('TAG:')]
	tag_set = list(set(t1+t2))
	for i in tag_set:
		print i

def delete_log():
	res = raw_input('ARE YOU SURE?(y/n)>')
	if res.lower() == 'y':
		response = requests.delete(url)
		print "All clear!Restart a new diary!"
	else:
		print "Well, keep going on!"

def write_log(message, tags):
	values = {'newdiary':message,'tags':tags}
	response = requests.post(url, data=values)

#def wechat_cli():

def client():
	url_local = 'http://localhost:1180/wechat'
	headers = {'Content-Type': 'application/xml'}
	send_msg = '''
	<xml><ToUserName><![CDATA[gh_b2f5086656aa]]></ToUserName>
	<FromUserName><![CDATA[bambooom]]></FromUserName>
	<CreateTime>%s</CreateTime>
	<MsgType><![CDATA[text]]></MsgType>
	<Content><![CDATA[%s]]></Content></xml>'''

	print HELP 
	tags='NULL'

	while True:
		print 'TAG:'+tags
		message = raw_input('Input>')
		if message.lower() in ['h','help','?']:
			print HELP
		elif message.lower() in ['s','sync']:
			print get_log_bytag(tags)
		elif message.lower() in ['q','quit']:
			print 'Bye~'
			break
		elif message in ['lt','ListTags']:
			get_tags()
		elif message.startswith('st:'):
			tags = message[3:]
			tags = tags if tags else 'NULL'
		elif message == 'FLUSH':
			delete_log()
		elif message.lower() in ['e:?','e:h','e:help']:
			r = requests.post(url_local, data = send_msg % (
				str(int(time.time())),"help"), headers = headers)
			print r.text
		elif message.lower() == 'e:s':
			r = requests.post(url_local, data = send_msg % (
				str(int(time.time())),"see"), headers = headers)
			print r.text
		elif message.lower().startswith('e:d='):
			raw_diary = message[2:]
			r = requests.post(url_local, data = send_msg % (
				str(int(time.time())),raw_diary), headers = headers)
			print r.text
			tags = "Wechat"
		else:
			write_log(message,tags)


if __name__ == '__main__':
	client()
