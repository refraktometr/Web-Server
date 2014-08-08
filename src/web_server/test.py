# coding=utf-8

b = [21]

query = """SELECT user_id, COUNT(text_message) FROM user_message
                WHERE recipient_id=%s AND flag=False  GROUP BY user_id""", b






print b
users = []


