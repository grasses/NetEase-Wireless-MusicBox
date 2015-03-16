#!/usr/local/Cellar/python
# -*- coding: utf-8 -*-

# @Author: homeway
# @Link: http://homeway.me
# @Version: 15.03.15

import os
import time
import hashlib 
import pymongo

# cookie_secret
import base64 
import uuid

# { '_id':'', 'time':'', 'session':{} } 

'''setting for session'''
setting = {
    # mongodb
    'host':'localhost',
    'port': 27017,
    'databse':'homeway', # remember build test databse, you can use command: use mongosion
    
    'session_id': '',
    'sessionExpires': 24*60*60,
    'autoDeleteExpired': True, # clean expired sessions at every get 
    'secretKey':base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
    'session' : { 'uid':'', 'isLogin':False, 'isAdmin':False, 'last': time.time() } #default session data, add or change by yourself
} 

class SessionBase(object):
    # create _id
    def generateSessionId(self, salt):
        rand = os.urandom(16)
        now = time.time()
        return hashlib.md5("%s%s%s" %(rand, now, salt)).hexdigest()

    def createSession(self, secretKey):
        '''create session and return data'''
        session_id = self.generateSessionId(secretKey)
        # update setting["session_id"]
        self._setting['session_id']=session_id
        self.db.save({'_id':session_id, 'time': time.time(), 'session': self._setting['session'] })
    
        data = self.getSession(session_id)
        return data

    def saveSession(self, session_id, session):
        '''save session and return new session data'''
        self.db.save({'_id':session_id, 'time': time.time(), 'session':session });
        data = self.getSession(session_id)
        return data

    def deleteSession(self, session_id):
        '''delete session'''
        self.db.remove({'_id':session_id})
        return True

    def getSession(self, session_id = None):
        '''get session and update time'''
        expiredTime = time.time() - self._setting['sessionExpires']
        
        # update setting["session_id"]
        self._setting['session_id']=session_id
    
        data = self.db.find_one({'_id':session_id,'time':{'$gt':expiredTime}}) # SELECT * FROM `session` WHERE `_id`=session_id AND `time`<expiredTime
        
        # update time          
        if data:
            self.db.update({'_id':session_id},{'$set':{'time':time.time()}})
        else:
            pass

        return data

    def deleteExpired(self):
        expiredTime = time.time() - self._setting['sessionExpires']
        self.db.remove({'time':{'$lt': expiredTime }})
        return True

    def checkTime(self, sessionTime, sessionExpires):
        longth = time.time() - sessionTime #当前时间 - 保存时间 = 时间距离
        if longth >= sessionExpires:
            '''timeout'''
            return False
        else:
            return True

    def checkSession(self, session_id):
        '''check session exist in expired time and update time'''
        expiredTime = time.time() - self._setting['sessionExpires']
        self._setting['session_id']=session_id
        
        data = self.db.find_one({'_id':session_id,'time':{'$gt':expiredTime}})

        # update time          
        if data:
            self.db.update({'_id':session_id},{'$set':{'time':time.time()}})
        else:
            pass
        return data

    def updateTime(self, session_id):
        self.db.update({'_id':session_id},{'$set':{'time':time.time()}})
        return True 

class Session(SessionBase):
    def __init__(self,setting):
        '''connect databse'''   
        self._setting = setting
        # connect to mongodb
        self._connection = pymongo.Connection( setting['host'], setting['port'])
        self._database = self._connection[ setting['databse'] ]
        self.db = self._database.session

    def save(self, session_id, session={}):
        # check exist
        check = SessionBase.checkSession(self, session_id )

        debug('check ', check)

        if not check:
            data = SessionBase.createSession( self,self._setting['secretKey']) 
            session_id = data['_id']
        else:
            pass
        data = SessionBase.saveSession(self, session_id, session)
        return data

    def getSessionId(self):
        # data = SessionBase.generate_session_id(self, self._setting['secretKey'])
        return self._setting['session_id']

    def exist(self, session_id):
        data = self.checkSession(session_id)
        if data:
            return data
        else: 
            return False

    def expired(self):
        data = self.deleteExpired()
        return data

    def delete(self, session_id):
        return SessionBase.deleteSession( self, session_id)

    def get(self, session_id = None):
        
        # auto delete expired sessions 
        if self._setting['autoDeleteExpired']:
            SessionBase.deleteExpired(self)
        else:
            pass

        # get session
        data = {}
        # data = { _id, time, session }
        if session_id:
            data = self.getSession(session_id)
            
            # without session 
            if data:
                sessionTime = data['time']
                return data
            else:
                pass
        else:
            pass
        
        # not find this session then create it
        data = SessionBase.createSession( self,self._setting['secretKey']) 
        return data

    def  __del__(self):
        pass

def test():
    print 'Hello, welcome to mongosion, an easy session module, writed by python base on pymongo using for tornado.py or web.py! Make sure pymongo has installed and mongodb is running'

MongoSion = Session(setting)

def debug(title,data):
    print title+' is : '
    print data

def get( session_id ):
    return MongoSion.get( session_id )

def save( session_id, session={} ):
    return MongoSion.save( session_id, session )

def delete( session_id ):
    return MongoSion.delete( session_id )

# update all session and delete sessions out of time
def expired():
    return MongoSion.expired()

def exist( session_id ):
    return MongoSion.exist( session_id )

if __name__ == '__main__':
    pass