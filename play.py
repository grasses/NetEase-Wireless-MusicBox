#!/usr/local/Cellar/python
# -*- coding: utf-8 -*-

# @Author: homeway
# @Link: http://homeway.me
# @Version: 15.03.17

import pygame
import pymongo
import shutil
import wget,threading,time,os,api
threads = []

class MusicData(object):
    def set_music_info(self, info):
        return self.db.save(info)
    
    def get_music_info(self, sid):
		res = self.db.find_one({ 'sid': sid })
		if res:
			return res
		else:
			return False

class Play(MusicData):
    def __init__ (self, option):
        self.db_option = option
        self.is_playing = False
        self.music_option = {
            'frequence' : 44100,
            'bitsize' : -16,
            'channels' : 1,
            'buffer' : 2048,
        }
        self.music_info={
            'sid' : '',
            'name' : '',
            'md5' : '',
            'mp3Url' : '',
            'path' :'',
        }
        # connect to mongodb
        self._conn = pymongo.Connection( option['host'], option['port'] )
        self._db = self._conn[ option['db'] ]
        self.db = self._db[ option['db'] ].music
        # setting pygame
        pygame.mixer.init( self.music_option['frequence'], self.music_option['bitsize'], self.music_option['channels'], self.music_option['buffer'])
        pygame.mixer.music.set_volume(1)
   	
   	# play music
    def play_music(self, sid):
        item = threading.Thread( target=self.play_music_thread, args=( sid,), name="player" )
        threads.append( item )
        item.start()

    # play threading
    def play_music_thread(self,sid):
        music_info = MusicData.get_music_info(self, sid)
        if not music_info:
        	music_info = self.search_music_info(sid)
        else:
            self.music_info=music_info
        # play now
    	clock = pygame.time.Clock()
        try:
            print self.music_info['path']
            pygame.mixer.music.load(self.music_info['path'])
            print("Music file {} loaded!".format(self.music_info['path']))
       	except pygame.error:
            print("File {} error! {}".format(self.music_info['path'], pygame.get_error()))
            return
       	pygame.mixer.music.play()
       	while pygame.mixer.music.get_busy():
       		clock.tick(30)
    	pass
    # search by api and get info
    def search_music_info(self, sid):
        NetEase = api.NetEase()
        login = NetEase.login('username', 'password')
        music_data = NetEase.song_detail(sid)
        self.music_info['mp3Url'] = music_data[0]['mp3Url']
        self.music_info['name'] = music_data[0]['name']
        self.music_info['sid'] = music_data[0]['id']
        music_place = self.download_music(self.music_info['mp3Url'])
        if music_place:
			MusicData.set_music_info( self, self.music_info )
        else:
			return
	# download and move
    def download_music(self, url):
        abs_path = os.path.abspath('./')
        file_path = abs_path + '/music'
    	if not os.path.exists( file_path ):
    		try:
    			os.makedirs( file_path )
    		except:
    			print '权限不足，无法创建目录...'
        else:
      		pass
        # 下载并移动
        try:
	        music = wget.download(url)
        except:
    		print '下载出错...'
		
        try:
            dest = file_path+'/'+music
            shutil.move( music, dest)
            self.music_info['path'] = dest#'music/'+music
            return dest
		
        except:
			print '文件写入错误...'

	def set_volume(self, value):
		try:
			pygame.mixer.music.set_volume( float(value) )
			return value
		except:
			return False
    	pass

if __name__ == "__main__":
    option = {
        'host':'localhost',
        'port': 27017,
        'db':'MusicBox',   
    }
    play = Play(option)
    play.play_music(27731178)





