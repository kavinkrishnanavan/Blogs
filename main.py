from flask import Flask,  render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# Flask reading the keys from your file

with open("config.json" , "r") as c:

    config_params = json.load(c)["parameters"]

app = Flask(__name__)

app.secret_key = config_params["secret_key"]

if config_params["local_server"]:

    app.config["SQLALCHEMY_DATABASE_URI"] = config_params["local_uri"]

else:
    app.config["SQLALCHEMY_DATABASE_URI"] = config_params["prod_uri"]

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer,primary_key=True)

    title = db.Column(db.String(50))

    image = db.Column(db.String(200))

    post_date = db.Column(db.DateTime , default = datetime.utcnow)

    content = db.Column(db.Text)

@app.route("/")
def index():

    blogpost = Blog.query.all()

    return render_template("index.html" , blogpost = blogpost)

@app.route("/<int:id>")
def post(id):

    blogpost = Blog.query.get(id)

    return render_template("post.html" , blogpost = blogpost)

@app.route("/delete/<int:id>")
def delete(id):

    delpost = Blog.query.get(id)

    db.session.delete(delpost)

    db.session.commit()

    return redirect(url_for('index'))

@app.route("/addpost" , methods=["POST" , "GET"])
def addpost():

    if request.method == "POST":

        post_title = request.form.get("title")

        post_content = request.form.get("content")

        post_image = request.form.get("image")

        newpost = Blog(title = post_title , image = post_image , content = post_content)

        db.session.add(newpost)

        db.session.commit()

        return redirect(url_for("index"))
    
    return render_template("addpost.html")

if __name__ == "__main__":

    with app.app_context():

        app.run(debug=True, host="0.0.0.0")