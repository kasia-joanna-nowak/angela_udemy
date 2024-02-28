from flask import Flask, render_template, request, redirect, url_for
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap



app = Flask(__name__)
app.config['SECRET_KEY'] = '1112224444'

all_books = []


class BookForm(FlaskForm):
    book = StringField('Book Name', validators=[DataRequired()])
    author = StringField('Book Author', validators=[DataRequired()])
    rating = StringField('Rating', validators=[DataRequired()])
    add = SubmitField('Add Book')


@app.route('/')
def home():
    return render_template('index.html',books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
        if request.method == "POST":
            new_book = {
            "title": request.form["book"],
            "author":  request.form["author"],
            "rating": request.form["rating"]
            }

            all_books.append(new_book)
            return redirect(url_for('home'))
        return render_template('add.html')


       


if __name__ == "__main__":
    app.run(debug=True)
