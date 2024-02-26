from flask import Flask, render_template, request, redirect, url_for
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_wtf import FlaskForm

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
    return render_template('index.html')


@app.route("/add", methods=["GET", "POST"])
def add():
        if request.method == "POST":
            new_book = {
            "book_title": request.form["book"],
            "book_author":  request.form["author"],
            "book_rating": request.form["rating"]}
            all_books.append(new_book)
            return render_template('index.html')
        return render_template('add.html')




if __name__ == "__main__":
    app.run(debug=True)
