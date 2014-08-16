from django.shortcuts import render_to_response, redirect
from apps import users
from apps.users import db, auth
from apps.chat.db import get_number_new_messages, get_messages, set_message, mark_messages_as_read


@auth.check_authorization
def chat(request, user_id):
    new_messages_number = get_number_new_messages(user_id)
    users_data = users.db.get_all_users()
    data = []
    for id, name in users_data:
        number = new_messages_number.get(id)
        data.append((id, name, number))
    return render_to_response("chat/chat.html", {
        'data': data,
    })


@auth.check_authorization
def user_chat(request, recipient_id, user_id):

    message_history = get_messages(user_id, recipient_id)
    mark_messages_as_read(user_id, recipient_id)
    _, user_name, _, _ = users.db.get_user_by_user_id(user_id)
    _, recipient_name, _, _ = users.db.get_user_by_user_id(recipient_id)
    recipient_id = int(recipient_id)
    user_id = int(user_id)

    if request.method == 'POST':
        text_message = request.POST['message']
        set_message(user_id, recipient_id, text_message)
        return redirect('/chat/user/{}/'.format(recipient_id))

    return render_to_response('chat/user_chat.html', {
        'recipient_id'    : recipient_id,
        'user_id'         : user_id,
        'message_history' : message_history,
        'user_name'       : user_name,
        'recipient_name'  : recipient_name
    })

