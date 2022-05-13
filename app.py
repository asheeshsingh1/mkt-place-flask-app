from crypt import methods
from email.policy import default
from turtle import title
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mktplace.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class mktplace(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    state = db.Column(db.Integer, nullable=True, default="Not_Sold")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} - {self.desc}"


@app.route("/", methods=["POST", "GET", "PUT"])
def home_html():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        mktplaceobj = mktplace(title=title, desc=desc)
        db.session.add(mktplaceobj)
        db.session.commit()
    allitems = mktplace.query.all()
    return render_template("index.html", allitems=allitems)


@app.route("/delete/<int:sno>")
def delete(sno):
    item = mktplace.query.filter_by(sno=sno).first()
    db.session.delete(item)
    db.session.commit()
    return redirect("/")


@app.route("/update/<int:sno>", methods=["POST", "GET"])
def update(sno):
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        item = mktplace.query.filter_by(sno=sno).first()
        item.title = title
        item.desc = desc
        db.session.add(item)
        db.session.commit()
        return redirect("/")
    item = mktplace.query.filter_by(sno=sno).first()
    return render_template("update.html", item=item)
