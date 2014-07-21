from flask import Flask, request, redirect, render_template
from web_server.auth import authorization_user
from web_server.validation import validate_username, validate_password
from web_server.db import create_user, get_user_by_user_id, get_user_by_username


app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/', methods=['GET', 'POST'])
def show_username():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        authorization = authorization_user(username, password)
        if authorization == True:
            return redirect('/page1')
        else:
            return render_template("main.html")
    else:
        return render_template("main.html")


@app.route('/page1', methods=['GET', 'POST'])
def info():
    return render_template("page1.html")


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    errors = []

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        errors.extend(validate_username(username))
        errors.extend(validate_password(password))

        if not errors:
            user_id = create_user(username, password)
            return redirect('/confirmation?userId={}'.format(user_id))
        else:
            return render_template('registration.html', errors=errors, username=username)
    return render_template('registration.html')


@app.route('/confirmation', methods=['GET', 'POST'])
def confirmation():
    user_id = request.args['userId']
    user_information = get_user_by_user_id(user_id)
    return render_template('confirmation.html', user_name=user_information[1], password=user_information[2])


if __name__ == "__main__":
    app.debug = True
    app.run()
