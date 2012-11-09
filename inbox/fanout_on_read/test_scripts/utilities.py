import random
import string

class RandomUsernamePool(): 
   def __init__(self, num_users = 100):
      self.num_users = num_users
      random.seed

   def get(self):
      value = random.randrange(0, self.num_users)
      return 'user' + str(value)


class RandomStringGenerator():
   def get(self,size=140):
      return ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(size))
