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

headers = {
    "accept": "application/json",
    "Authorization": "Bearer 7b9edf26f9e0b444273acdbff2ddafe9"
}

response = requests.get(url, headers=headers)
data = response.json()
print(data)

# CREATE DB
class Base(DeclarativeBase):
  pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies-collection.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CREATE TABLE
class Movie(db.Model):
  id:Mapped[int] = mapped_column(primary_key=True)
  title:Mapped[str] = mapped_column(unique=True)
  year :Mapped[int] = mapped_column(Integer)
  description :Mapped[str] = mapped_column(String)
  rating :Mapped[int] = mapped_column(Integer)
  ranking:Mapped[int] = mapped_column(Integer)
  description :Mapped[str] = mapped_column(String)
  review:Mapped[str] = mapped_column(String)
  img_url:Mapped[str] = mapped_column(String)




with app.app_context():
    db.create_all()

class RateForm(FlaskForm):
   rating = StringField("Your Rating Out of 10 e.g. 7.5")
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

@app.route("/update", methods = ["POST", "GET"])
def update_rating():
  form=RateForm()
  movie_id = request.args.get("id")
  movie = db.get_or_404(Movie, movie_id)
  if form.validate_on_submit():
     movie.rating = form.rating.data
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

if __name__ == '__main__':
    app.run(debug=True)
