from django.shortcuts import render_to_response, redirect
from apps.users import auth, validation, models


def index(request):
    error = False

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = models.User.objects.get(username=username)

        if user and user.check_password(password):
            response = redirect('/chat/')
            auth.authorize_user(response, user.id)
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
            user = models.User.objects.create(username, password)
            return redirect('/confirmation/user_id/{}/'.format(user.id))

    return render_to_response('users/registration.html', {
                'errors' : errors,
            })


def confirmation(request, user_id):
    user = models.User.objects.get(user_id=user_id)
    return render_to_response('users/confirmation.html', {
        'user_name' : user.username
    })


def logout(request):
    response = redirect('/')
    auth.logout_user(request, response)
    return response
