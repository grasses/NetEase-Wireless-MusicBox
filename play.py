#!/usr/local/bin/python2.7
#-*- coding: utf-8 -*-

# @Author: homeway
# @Link: http://homeway.me
# @Version: 15.03.15

import pygame as pg 
import shutil
import wget,threading,time,os
threads = []

class Play(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.url =''
        self.option={
            'frequence' : 44100,
            'bitsize' : -16,
            'channels' : 2,
            'buffer' : 2048,
        }
        pg.mixer.init( self.option['frequence'], self.option['bitsize'], self.option['channels'], self.option['buffer'])
        pg.mixer.music.set_volume(0.8)
        
    # 播放音乐
    def playMusic(self, music_file):
        item = threading.Thread( target=self.playMusicThread, args=(music_file,), name="player" )
        threads.append( item )
        item.start()

    def playMusicThread(self, music_file):
        clock = pg.time.Clock()
        try:
            pg.mixer.music.load(music_file)
            print("Music file {} loaded!".format(music_file))
        except pg.error:
            print("File {} error! {}".format(music_file, pg.get_error()))
            return
        pg.mixer.music.play()
        while pg.mixer.music.get_busy():
            clock.tick(30)
    # 添加file文件夹，用于存放缓存文件
    def makedirs(self, name):
        absPath = os.path.abspath('./')
        try:
            os.makedirs(name)
            filePath = absPath + '/'+ name
            return filePath
        except:
            return False
    # 下载音乐
    def downloadMusic(self, url):
        if not os.path.exists('music'):
            self.makedirs('music')
        music = wget.download(url)
        res = './music/'+music
        shutil.move( music, res)
        return res

    # 设置连接
    def setUrl(self, url):
        self.url = url
        return self.url

    # 设置音量
    def setVolume(self, value):
        pg.mixer.music.set_volume( float(value) )
        return value
    
    # 控制台
    def main(self):
        music_file = self.downloadMusic( self.url )
        try:
            self.playMusic(music_file)
        except KeyboardInterrupt:
            pg.mixer.music.fadeout(1000)
            pg.mixer.music.stop()
            raise SystemExit