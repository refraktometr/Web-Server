from django.shortcuts import render_to_response, redirect
from apps.users import db, auth, validation
from apps.users.db import get_cursor


def index(request):
    error = False

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_id = db.get_valid_user(username, password)

        if user_id:
            response = redirect('/chat/')
            auth.authorize_user(response, user_id)
            return response
        else:
            error = True

    return render_to_response('users/index.html', {'error' : error})


def registration(request):
    errors = []

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        errors.extend(validation.validate_username(username))
        errors.extend(validation.validate_password(password))

        if not errors:
            user_id = db.create_user(username, password)
            return redirect('/confirmation/user_id/{}/'.format(user_id))
        else:
            return render_to_response('users/registration.html', {
                'errors' : errors,
                username : username
            })
    return render_to_response('users/registration.html')


def confirmation(request, user_id):
    user_information = db.get_user_by_user_id(user_id)
    return render_to_response('users/confirmation.html', {
        'user_name' : user_information[1],
    })



def logout(request):
    response = redirect('/')
    auth.logout_user(request, response)
    return response
