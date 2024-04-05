from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

api_key = "7b9edf26f9e0b444273acdbff2ddafe9"


url = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"



headers = {
    "accept": "application/json",
    "Authorization": "Bearer 7b9edf26f9e0b444273acdbff2ddafe9"
}

# CREATE DB
class Base(DeclarativeBase):
  pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies-collection.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CREATE TABLE
class Movie(db.Model):
   id: Mapped[int] = mapped_column(Integer, primary_key=True)
   title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
   year: Mapped[int] = mapped_column(Integer, nullable=False)
   description: Mapped[str] = mapped_column(String(500), nullable=False)
   rating: Mapped[float] = mapped_column(Float, nullable=True)
   ranking: Mapped[int] = mapped_column(Integer, nullable=True)
   review: Mapped[str] = mapped_column(String(250), nullable=True)
   img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()

class RateForm(FlaskForm):
   rating = StringField("Your Rating Out of 10 e.g. 7.5" )
   review = StringField("Your Review")
   submit = SubmitField("Done")

class AddMovie(FlaskForm):
   movie = StringField("Movie Title")
   submit= SubmitField("Add Movie")

@app.route("/", methods = ["POST", "GET"])
def home():
    movies = db.session.execute(db.select(Movie))
    all_movies = movies.scalars()
    return render_template("index.html", movies = all_movies)


@app.route("/update/<id>", methods = ["POST", "GET"])
def update_rating(id):
  form=RateForm()
  movie = db.get_or_404(Movie, id)
  if form.validate_on_submit():
     movie.rating = form.rating.data
     movie.review = form.review.data
     db.session.commit()
     return redirect(url_for('home'))
  return render_template("edit.html", movie=movie, form=form)


@app.route("/delete", methods = ["POST", "GET"])
def delete_movie():
  movie_id = request.args.get("id")
  movie = db.get_or_404(Movie, movie_id)
  db.session.delete(movie)
  db.session.commit()
  return redirect(url_for("home"))


@app.route("/add", methods = ["POST", "GET"])
def add_new_movie():
   form= AddMovie()
   if form.validate_on_submit():
      new_movie = Movie(
         title = request.form["movie"]
      )
      response = requests.get(url = f"https://api.themoviedb.org/3/search/movie?query={new_movie.title}&api_key={api_key}")
      data = response.json()
      # db.session.add(new_movie)
      # db.session.commit() 
      return render_template("select.html", data=data["results"])
   return render_template("add.html", form=form)

@app.route("/choose")
def choose_movie():
   movie_id = request.args.get("id")
   if movie_id:
      response = requests.get(url = f"https://api.themoviedb.org/3/movie/{movie_id}", params={"api_key":api_key})
      data = response.json()
      new_movie_info = Movie(
         title = data["title"],
         year=data["release_date"].split("-")[0],
         img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
         description=data["overview"]
      )
      db.session.add(new_movie_info)
      db.session.commit()
      return redirect(url_for("update_rating", id=new_movie_info.id))
      # return redirect(url_for("home", id=new_movie_info.movie_id))

if __name__ == '__main__':
    app.run(debug=True)
