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
            response = redirect('/login_success')
            auth.authorize_user(response, user_id)
            return response
        else:
            error = True

    return render_template("main.html", error=error)


@app.route('/login_success', methods=['GET', 'POST'])
def login_success():
    users_data = db.get_all_users()
    return render_template("login_success.html", users_data=users_data)


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


@app.route('/message', methods=['GET', 'POST'])
def send_message():
    user_id = auth.get_user_id(request)
    recipient_id = request.args['recipient_id']
    if request.method == 'POST':
        text_message = request.form['message']
        db.set_message(user_id, recipient_id, text_message)
        render_template('message.html', recipient_id=recipient_id)

    return render_template('message.html', recipient_id=recipient_id)

if __name__ == "__main__":
    app.run()
