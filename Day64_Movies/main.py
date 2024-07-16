from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, URL
import requests

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-movie-collection.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[float] = mapped_column(Float, nullable=False)
    review: Mapped[str] = mapped_column(String(250), nullable=False)
    image_url: Mapped[str] = mapped_column(String(250), nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.

    def __repr__(self):
        return f'<Book {self.title}>'


class MovieForm(FlaskForm):
    title = StringField('Movie name', validators=[DataRequired()])
    year = IntegerField('Movie year', validators=[DataRequired()])
    description = StringField('Movie Description, eg: Great', validators=[DataRequired()])
    rating = FloatField('Movie rating',validators=[DataRequired()])
    ranking = SelectField('Movie ranking', choices=[0, 1, 2, 3, 4, 5], validators=[DataRequired()])
    review = StringField('Movie review', validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')


with app.app_context():
    db.create_all()
movies = []


@app.route("/")
def home():
    movies.clear()
    with app.app_context():
        result = db.session.execute(db.select(Movie).order_by(Movie.title))
        all_movies = result.scalars()
        for movie in all_movies:
            movies.append(movie)
        print(movies)
    return render_template("index.html", movies_list=movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = MovieForm()
    if form.validate_on_submit():
        with app.app_context():
            new_movie = Movie(title=form.title.data, year=form.year.data, description=form.description.data, rating=form.rating.data, ranking=form.ranking.data, review=form.review.data, image_url=form.image_url.data)
            db.session.add(new_movie)
            db.session.commit()
        return render_template("index.html")
    return render_template("add.html", form=form)


@app.route("/update")
def update():
    return render_template("edit.html")


@app.route("/delete")
def delete():
    return render_template("delete.html")


if __name__ == '__main__':
    app.run(debug=True)
