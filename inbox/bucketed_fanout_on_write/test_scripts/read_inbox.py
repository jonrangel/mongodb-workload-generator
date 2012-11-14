#!/usr/bin/env python

import time
import random
import mechanize
from pymongo import Connection, DESCENDING
from utilities import RandomUsernamePool, RandomStringGenerator

class Transaction(object):
   def __init__(self):
      self.custom_timers = {} 
      self.db = Connection('localhost',27017).fanout_on_write
      self.user_pool = RandomUsernamePool()
      pass

   def run(self):
      owner = self.user_pool.get()
      start_timer = time.time()
      for msg in self.db.inboxes.find({'owner': owner}).sort('sequence', DESCENDING).limit(1):
         continue
      latency = time.time() - start_timer
      self.custom_timers["Read inbox"] = latency

if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    print trans.custom_timers
