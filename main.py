from flask import Flask, render_template, request
from post import Post
import requests
import smtplib


# user email address adn password to allow contact form to send information
email = "user@email.com"
password = "password"

url = "https://api.npoint.io/abc670c6290f7d9f80ff"  # url to blog API
posts = requests.get(url).json()
print(posts)

post_objects = []
for post in posts:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
    post_objects.append(post_obj)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", all_posts=post_objects)


@app.route('/index.html')
def home():
    return render_template("index.html", all_posts=post_objects)


@app.route('/about.html')
def about():
    return render_template("about.html")


@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        full_name = request.form['full_name']  # gets username entry data from html form
        contact_email = request.form['email']  # gets email entry data from html form
        phone_number = request.form['phone_number']  # gets phone number entry data from html form
        message = request.form['message']  # gets message entry data from html form
        success_message = "Thank you! Your message has been successfully sent!"
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(
                from_addr=gmail,
                to_addrs=gmail,
                msg=f"Subject:Contact Enquiry\n\nName: {full_name}\nEmail: {contact_email}\nPhone Number: {phone_number}\nmessage: {message}"
            )

        return render_template("contact_success.html", message=success_message)
    else:
        return render_template("contact.html")


@app.route('/post.html')
def post():
    return render_template("post.html", all_posts=post_objects)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in post_objects:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template("post2.html", post=requested_post)


if __name__ == "__main__":  # to check the code is running from within this file
    app.run(debug=True)
