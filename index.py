#!/usr/local/Cellar/python python
#-*- coding: utf-8 -*-

import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.httpserver
import tornado.web
import os.path
import json
import time
import random

# upload
import shutil
import os

#url
import urlparse

import logging
#import Image 
#import exifread 
import tempfile

# cookie_secret
import base64 
import uuid 
import hashlib 

# mongodb
import pymongo
# session
#from mongosion import Session
#import session

from tornado.escape import json_encode
from tornado.options import define, options


#some global information like session
global isAdmin
global isLogin
global user
global base_url
global sid
global typeList

import api

define("port", default=80, help="run on the given port", type=int)
define("db", default='jueShare', help="database name", type=str)
define("user", default='root', help="database user", type=str)
define("pwd", default='xiaocao', help="database password", type=str) 

NetEase = api.NetEase()
login = NetEase.login('15958153676', '0814891WLT')

class Application(tornado.web.Application):
    '''setting || main || router'''
    def __init__(self):
        handlers = [
            #for html
            (r"/", MainHandler),
            (r"/song.html", GetSongHandler),
            (r"/album.html", GetAlbumHandler),
            
            #for ajax
            (r"/ajaxSearch", AjaxSearchHandler),
            (r"/ajaxGetSong", AjaxGetSongHandler),
            (r"/ajaxAlbum", AjaxGetAlbumHandler),
            (r"/ajaxLogin", AjaxLoginHandler),
            (r"/ajaxPlayMusic", AjaxPlayMusicHandler),
            (r"/ajaxNewAlbums", AjaxNewAlbumsHandler),
        ]
        
        settings = dict(
            cookie_secret=base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
            base_path=os.path.join(os.path.dirname(__file__), ""),
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


################################## html ############################################

class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        '''database init'''
        self.sid = self.get_secure_cookie("sid")
        #self.data = session.get(self.sid)
        #self.set_secure_cookie("sid",self.data['_id'])
        
    def get(self):
        self.set_header("Accept-Charset", "utf-8")
        NetEase.refresh()
        new_albums = NetEase.artists('4292')
        self.render("index.html", title="homeway|share", base_url=base_url, data=new_albums[0])

class GetSongHandler(tornado.web.RequestHandler):
    def initialize(self):
    	pass
    def get(self):
        self.set_header("Accept-Charset", "utf-8")
        NetEase.refresh()
        req = { 'sid':self.get_argument("sid") } 
        res = NetEase.song_detail(  req['sid'] )
        #self.write( tornado.escape.json_encode(res) )
        self.render("song.html", title="homeway|share", data=res)

class GetAlbumHandler(tornado.web.RequestHandler):
    def initialize(self):
    	pass
    def get(self):
        self.set_header("Accept-Charset", "utf-8")
        NetEase.refresh()
        req = { 'aid':self.get_argument("aid") } 
        res = NetEase.album(  req['aid'] )
        #self.write( tornado.escape.json_encode(res) )
        self.render("album.html", title="homeway|share", data=res)

################################## ajax ############################################
#搜索信息
class AjaxSearchHandler(tornado.web.RequestHandler):
    def initialize(self):
        '''database init'''
        self.sid = self.get_secure_cookie("sid")
        #self.data = session.get(self.sid)
        #self.set_secure_cookie("sid",self.data['_id'])
    def get(self):
    	self.write( tornado.escape.json_encode( {'result': False, 'info': '拒绝GET请求！！' } ) )
    def post(self):
        self.set_header("Accept-Charset", "utf-8")
        NetEase.refresh()
        req = { 'key':self.get_argument("key") } 
        res = NetEase.search(  req['key'] )
        self.write( tornado.escape.json_encode(res['result']) )
# 播放音乐
class AjaxPlayMusicHandler(tornado.web.RequestHandler):
    def initialize(self):
        '''database init'''
        self.sid = self.get_secure_cookie("sid")
        #self.data = session.get(self.sid)
        #self.set_secure_cookie("sid",self.data['_id'])
    def post(self):
    	self.write( tornado.escape.json_encode( {'result': False, 'info': '拒绝GET请求！！' } ) )
    def post(self):
        self.set_header("Accept-Charset", "utf-8")
        req = { 'sid':self.get_argument("sid"), 'url':self.get_argument("url"), } 
        import play
        player = play.Play()
        player.setUrl( req['url'] )
        player.main()
        self.write( tornado.escape.json_encode( {'result': True, 'info': 'play now...！！' } ) )
# 登录网易云
class AjaxLoginHandler(tornado.web.RequestHandler):
    def initialize(self):
        '''database init'''
        self.sid = self.get_secure_cookie("sid")
        #self.data = session.get(self.sid)
        #self.set_secure_cookie("sid",self.data['_id'])
    def post(self):
    	self.write( tornado.escape.json_encode( {'result': False, 'info': '拒绝GET请求！！' } ) )
    def get(self):
        self.set_header("Accept-Charset", "utf-8")
        NetEase.refresh()
        req = { 'user':self.get_argument("user"), 'pass':self.get_argument("pass") } 
        res = NetEase.login(  req['user'], req['pass'] )
        self.write( tornado.escape.json_encode(res['profile']) )
# 获取音乐信息
class AjaxGetSongHandler(tornado.web.RequestHandler):
    def initialize(self):
        '''database init'''
        self.sid = self.get_secure_cookie("sid")
        #self.data = session.get(self.sid)
        #self.set_secure_cookie("sid",self.data['_id'])
    def post(self):
    	self.write( tornado.escape.json_encode( {'result': False, 'info': '拒绝GET请求！！' } ) )
    def get(self):
        self.set_header("Accept-Charset", "utf-8")
        NetEase.refresh()
        req = { 'sid':self.get_argument("sid") } 
        res = NetEase.song_detail( req['sid'] )
        self.write( tornado.escape.json_encode(res) )

class AjaxGetAlbumHandler(tornado.web.RequestHandler):
    def initialize(self):
        '''database init'''
        self.sid = self.get_secure_cookie("sid")
        #self.data = session.get(self.sid)
        #self.set_secure_cookie("sid",self.data['_id'])
    def post(self):
    	self.write( tornado.escape.json_encode( {'result': False, 'info': '拒绝GET请求！！' } ) )
    def get(self):
        self.set_header("Accept-Charset", "utf-8")
        NetEase.refresh()
        req = { 'aid':self.get_argument("aid") } 
        res = NetEase.album(  req['aid'] )
        self.write( tornado.escape.json_encode(res) )

# 获取最新的专辑
class AjaxNewAlbumsHandler(tornado.web.RequestHandler):
    def initialize(self):
        '''database init'''
        self.sid = self.get_secure_cookie("sid")
        #self.data = session.get(self.sid)
        #self.set_secure_cookie("sid",self.data['_id'])
    def get(self):
    	self.write( tornado.escape.json_encode( {'result': False, 'info': '拒绝GET请求！！' } ) )
    def post(self):
        self.set_header("Accept-Charset", "utf-8")
        NetEase.refresh()
        req = { 'offset': self.get_argument("offset"), 'limit': self.get_argument("limit") }
        res = NetEase.top_songlist( req['offset'],req['limit'] )
        self.write( tornado.escape.json_encode(res) )

def base_url(path):
    return "http://127.0.0.1/"+path

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main() 

