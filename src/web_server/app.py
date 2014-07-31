from flask import Flask, request, redirect, render_template

from web_server import db, validation, auth, utils


app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.debug = True


@app.route('/', methods=['GET', 'POST'])
def main():
    sessionid = auth.get_sessionid_from_cookie(request)
    if db.get_valid_sessionid(sessionid):
        return redirect('/chat')

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
def confirmation():
    user_id = request.args['userId']
    user_information = db.get_user_by_user_id(user_id)
    return render_template('confirmation.html', user_name=user_information[1], password=user_information[2])


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    users_data = db.get_all_users()
    return render_template("chat.html", users_data=users_data)


@app.route('/chat/user/<recipient_id>/', methods=['GET', 'POST'])
def user_chat(recipient_id):
    user_id = auth.get_user_id(request)
    old_message = db.get_messages(user_id, recipient_id)

    if request.method == 'POST':
        text_message = request.form['message']
        db.set_message(user_id, recipient_id, text_message)
        return redirect('/chat/user/{}/'.format(recipient_id))

    return render_template('user_chat.html', recipient_id=recipient_id, old_message=old_message)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    sessionid = auth.get_sessionid_from_cookie(request)
    db.del_session(sessionid)
    response = redirect('/')
    utils.delete_cookie(response, 'sessionid')
    return response

if __name__ == "__main__":
    app.run()
