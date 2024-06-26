from flask import Flask, render_template, request, redirect, url_for
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)

class Base(DeclarativeBase):
  pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True,nullable=False)
    author: Mapped[str] = mapped_column(String(250),unique=False,nullable=False)
    rating: Mapped[float] = mapped_column(Float,unique=False,nullable=False)
    

with app.app_context():
    db.create_all()


@app.route('/', methods = ["POST", "GET"])
def home():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars()
    return render_template('index.html',books=all_books)

@app.route('/delete/<id>', methods=["GET", "POST"])
def delete(id):
    book_id = id
    book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))
        

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    book_id = id
    selected_book = db.get_or_404(Book, book_id)
    if request.method == "POST":
        selected_book.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", book=selected_book)

  

       


if __name__ == "__main__":
    app.run(debug=True)
