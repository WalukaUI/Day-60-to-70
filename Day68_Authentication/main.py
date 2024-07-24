from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# CREATE DATABASE


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE IN DB


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))



with app.app_context():
    db.create_all()


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        password_with_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        new_user = User(name=name, email=email, password=password_with_hash)
        db.session.add(new_user)
        db.session.commit()
        return render_template("secrets.html", name=name)
    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        log_email = request.form["email"]
        pass_wd = request.form["password"]
        user = db.session.execute(db.select(User).where(User.email == log_email)).scalar()
        if check_password_hash(user.password, pass_wd) and user.email == log_email:
            login_user(user)
            return render_template("secrets.html", name=user.name)
        else:
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route('/secrets')
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
def logout():
    pass


@app.route('/download')
def download():
    return send_from_directory('static', path="files/cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(debug=True)
