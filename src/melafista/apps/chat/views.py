from django.shortcuts import render_to_response, redirect
from apps.users import auth, models
from apps.chat import db


@auth.check_authorization
def chat(request, user_id):
    new_messages_number = db.get_number_new_messages(user_id)
    users = models.User.objects.get_all_users()
    data = []
    for user in users:
        number_new_messages = new_messages_number.get(user.id)
        data.append((user.id, user.name, number_new_messages))
    return render_to_response("chat/chat.html", {
        'data': data,
    })


@auth.check_authorization
def user_chat(request, recipient_id, user_id):

    user_id = int(user_id)
    recipient_id = int(recipient_id)
    message_history = db.get_messages(user_id, recipient_id)
    db.mark_messages_as_read(user_id, recipient_id)
    user = models.User.objects.get(user_id=user_id)
    recipient = models.User.objects.get(user_id=recipient_id)

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

