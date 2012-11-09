#!/usr/bin/env python

import time
import random
import mechanize
import datetime
from pymongo import Connection, ASCENDING
from utilities import RandomUsernamePool, RandomStringGenerator



class Transaction(object):
   def __init__(self):
      self.custom_timers = {} 
      self.db = Connection('localhost',27017).bucketed_fanout_on_write
      self.user_pool = RandomUsernamePool()
      self.msg_gen   = RandomStringGenerator()
      self.db.inboxes.ensure_index([('owner',ASCENDING),('sequence',ASCENDING)])
      pass

   def get_sequence(self,user):
      user = self.db.users.find_and_modify( 
               query  = {'_id':user},
               update = {'$inc': { 'count': 1 }},
               upsert = True,
               new    = True )
      return user['count'] / 50

   def run(self):
      sender = self.user_pool.get()
      receivers = []
      for x in range(random.randint(1,10)):
         receivers.append( self.user_pool.get() )

      doc = { "from": sender, 
              "to" : receivers, 
              "time": datetime.datetime.utcnow(),  
              "msg": self.msg_gen.get() } 
            
      start_timer = time.time()

      for x in receivers:
         sequence = self.get_sequence( x ) 
         self.db.inboxes.update( {'owner': x, 'sequence': sequence },
               {'$push': {'messages': doc }}, upsert=True, safe=True )

      latency = time.time() - start_timer

      self.custom_timers["Send message"] = latency

if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    print trans.custom_timers
