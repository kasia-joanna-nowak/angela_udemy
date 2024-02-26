from flask import Flask, render_template, request
import requests
import smtplib


OWN_EMAIL = "1988kowalskaania@gmail.com"
OWN_PASSWORD = "aniakowalska1"



app = Flask(__name__)

posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

@app.route('/home')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data= request.form
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

def send_email(name, email, phone, message):
        email_message = f"Topic:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
        with smtplib.SMTP("smtp.gmail.com",port=465) as connection:
            connection.starttls()
            connection.login(OWN_EMAIL, OWN_PASSWORD)
            connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)



if __name__ == "__main__":
    app.run(debug=True)
