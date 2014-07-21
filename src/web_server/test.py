import hashlib
import random
import string


salt = ''.join(random.choice(string.hexdigits) for i in range(25))

print(salt)



#from web_server.db import  get_users, create_user, truncate_users, get_user_by_username, get_user_by_user_id
password = 'ekrjgnkelgrjekgn'
password = hashlib.sha256(password hexdigest()+ salt).
print password



# k = get_users()
# kollichestvo_userov = len(k)
# d = k[kollichestvo_userov-1]
#
# e = get_user_by_username('zarabotalo')
#
#
# print (d)
# print (e)
