from flask import Flask, request, redirect, render_template

from web_server import db, validation, auth


app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.debug = True


@app.route('/', methods=['GET', 'POST'])
def main():

    error = False

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_id = db.get_valid_user(username, password)

        if user_id:
            response = redirect('/chat')
            auth.authorize_user(response, user_id)
            return response
        else:
            error = True

    return render_template("main.html", error=error)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    errors = []

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        errors.extend(validation.validate_username(username))
        errors.extend(validation.validate_password(password))

        if not errors:
            user_id = db.create_user(username, password)
            return redirect('/confirmation?userId={}'.format(user_id))
        else:
            return render_template('registration.html', errors=errors, username=username)
    return render_template('registration.html')


@app.route('/confirmation', methods=['GET', 'POST'])
@auth.check_authorization
def confirmation(user_id):
    user_information = db.get_user_by_user_id(user_id)
    return render_template('confirmation.html', user_name=user_information[1], password=user_information[2])


@app.route('/chat', methods=['GET', 'POST'])
@auth.check_authorization
def chat(user_id):
    new_messages_number = db.get_number_new_messages(user_id)
    users_data = db.get_all_users()

    return render_template("chat.html", users_data=users_data, new_messages_number=new_messages_number)


@app.route('/chat/user/<recipient_id>/', methods=['GET', 'POST'])
@auth.check_authorization
def user_chat(user_id, recipient_id):

    message_history = db.get_messages(user_id, recipient_id)
    db.mark_messages_as_read(user_id, recipient_id)

    if request.method == 'POST':
        text_message = request.form['message']
        db.set_message(user_id, recipient_id, text_message)
        return redirect('/chat/user/{}/'.format(recipient_id))

    return render_template('user_chat.html', recipient_id=recipient_id, message_history=message_history)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    response = redirect('/')
    auth.logout_user(request, response)
    return response


if __name__ == "__main__":
    app.run()
