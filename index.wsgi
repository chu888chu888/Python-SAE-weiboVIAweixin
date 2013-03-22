#!/usr/bin/python
#--coding:utf-8--
import os
import sae
import json
import web
import urllib
import urllib2
from lxml import etree
from weibo import *

config={"TOKEN":'',		#your weixin token
    "WEIXIN": 'weixin'}
    
urls = (
	'/','weixin'
)

app_root = os.path.dirname(__file__)


class weixin:
    def GET(self):
        '''response to the signature from weixin'''
        
	data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        token = config['TOKEN']
 
        tmplist = [ token, timestamp, nonce ]
        tmplist.sort()
        tmpstr = ''.join( tmplist )
        hashstr = hashlib.sha1( tmpstr ).hexdigest()
    
        if hashstr == signature:
            return echostr
    
        print signature,timestamp,nonce
        print tmpstr,hashstr
        return 'Error' + echostr
    
    
    def POST(self):
        data = web.data()
    	
        #parse the XML
        root = etree.fromstring( data )
        child = list( root )
        recv = {}
        for i in child:
            recv[i.tag] = i.text
     
        textTpl = """<xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[%s]]></MsgType>
            <Content><![CDATA[%s]]></Content>
            <FuncFlag>0</FuncFlag>
            </xml>"""

        content = recv['Content'].strip()
        response = self.copewithMsg(content)
        echostr = textTpl % (recv['FromUserName'],recv['ToUserName'],recv['CreateTime'],recv['MsgType'],response)
        return echostr

    
    def copewithMsg(self,content):
    
        #welcome message for following the weixin public account
    	if content == 'subscribe':
            response = '欢迎添加微信公众帐号!\n需要帮助请回复 h '
            return response

        #help message
        if content == 'h':
            response = '把待发送的文字内容包含在一对英文双引号内，即可发送微博'
            return response
        
        #post a weibo message
        if content.startswith('"') and content.endswith('"'):
	    content = content[1:-1]
            response = self.press(content)  
            return response

        else:
            response = '需要帮助请回复 h '
            return response
    

	def press(self,message):

	    #fill your information from sina
    	    appkey = ''
    	    appsecret = ''
    	    callback_url = ''
    	    access_token = ''
    	    expires_in = ''

    	    client = APIClient(app_key = appkey,app_secret = appsecret,redirect_uri = callback_url)
    	    client.set_access_token(access_token,expires_in)
    	    try:
                clt.post.statuses__update(status=message)
                return '发布成功'
            except APIError,e:
            	return str(e)


#main
app = web.application(urls,globals()).wsgifunc()
application = sae.create_wsgi_app(app)


