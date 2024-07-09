from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Length
'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(min=6, message=('Little short for an email address?'))])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message=('Little short for a passsword?'))])
    submit = SubmitField(label="Log In")


app = Flask(__name__)
app.secret_key = "any-string-you-want-just-keep-it-secret"


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.email.data == "admin@email.com" and login_form.password.data == "12345678":
            print(login_form.email.data)
            print(login_form.password.data)
            return render_template('success.html')
        else:
            return render_template('denied.html')
    return render_template('login.html', form=login_form)


@app.route("/submitted")
def sub():
    return render_template('formsubmitted.html')


if __name__ == '__main__':
    app.run(debug=True)
