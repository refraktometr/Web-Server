from django.shortcuts import render_to_response, redirect
from apps.users import auth
from apps.users import db as user_db
from apps.chat import db


@auth.check_authorization
def chat(request, user_id):
    new_messages_number = db.get_number_new_messages(user_id)
    users_data = user_db.get_id_and_username_all_users()
    data = []
    for id, name in users_data:
        number = new_messages_number.get(id)
        data.append((id, name, number))
    return render_to_response("chat/chat.html", {
        'data': data,
    })


@auth.check_authorization
def user_chat(request, recipient_id, user_id):

    user_id = int(user_id)
    recipient_id = int(recipient_id)
    message_history = db.get_messages(user_id, recipient_id)
    db.mark_messages_as_read(user_id, recipient_id)
    user = user_db.get_user(user_id=user_id)
    recipient = user_db.get_user(user_id=recipient_id)

    if request.method == 'POST':
        text_message = request.POST['message']
        db.create_message(user_id, recipient_id, text_message)
        return redirect('/chat/user/{}/'.format(recipient_id))

    return render_to_response('chat/user_chat.html', {
        'recipient_id': recipient.id,
        'user_id': user.id,
        'message_history': message_history,
        'user_name': user.username,
        'recipient_name': recipient.username
    })

