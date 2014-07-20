from web_server.db import  get_users, create_user, truncate_users, get_user_by_username, get_user_by_user_id

print(get_user_by_user_id(11))
print (get_user_by_username('krinart'))
user = get_user_by_user_id(11)
print (user[1])



# k = get_users()
# kollichestvo_userov = len(k)
# d = k[kollichestvo_userov-1]
#
# e = get_user_by_username('zarabotalo')
#
#
# print (d)
# print (e)
