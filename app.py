from flask import Flask, render_template, request, redirect, url_for
from models import db, Gallery
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# create database
with app.app_context():
    db.create_all()


# ======================
# DASHBOARD (READ)
# ======================
@app.route("/")
def dashboard():
    galleries = Gallery.query.order_by(Gallery.created_at.desc()).all()
    return render_template("dashboard.html", galleries=galleries)


# ======================
# CREATE GALLERY
# ======================
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        image = request.files["image"]

        if image:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
            image.save(filepath)

            gallery = Gallery(
                title=title,
                filename=image.filename
            )

            db.session.add(gallery)
            db.session.commit()

            return redirect(url_for("dashboard"))

    return render_template("create.html")


if __name__ == "__main__":
    app.run(debug=True)