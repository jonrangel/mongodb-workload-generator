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
      self.db = Connection('localhost',27017).fanout_on_write
      self.user_pool = RandomUsernamePool()
      self.msg_gen   = RandomStringGenerator()
      self.db.messages.ensure_index([('owner',ASCENDING),('time',ASCENDING)])
      pass

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
         this_doc = doc.copy()
         this_doc["owner"] = x 
         self.db.messages.insert( this_doc, safe=True ) 

      latency = time.time() - start_timer

      self.custom_timers["Send message"] = latency

if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    print trans.custom_timers
