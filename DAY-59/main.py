from flask import Flask, render_template, url_for
import requests

#api_endpoint
url = "https://api.npoint.io/e96642dcb56ab3919e53"

posts= requests.get(url).json()


app = Flask(__name__)


@app.route("/index.html")
def get_home():
    return render_template("index.html", all_posts = posts)

@app.route("/about.html")
def get_about():
    return render_template("about.html")

@app.route("/contact.html")
def get_contact():
    return render_template("contact.html")

@app.route("/post/<int:index>")
def show_articles(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)
