from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, URL
from wtforms import StringField, SubmitField, SelectField, BooleanField
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


class AddCafe(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    map_url = StringField("Insert Google Map Url", validators=[DataRequired(), URL()])
    img_url = StringField("Insert Image Url of Location", validators=[DataRequired(), URL()])
    location = StringField("City of Cafe", validators=[DataRequired()])
    seats = SelectField('Number of Seats', choices=[('0-10', '0-10'), ('10-20', '10-20'), ('20-30', '20-30'),
                                                    ('40-50', '40-50'), ('50+', '50+')])
    has_toilet = BooleanField()
    has_wifi = BooleanField()
    has_sockets = BooleanField()
    can_take_calls = BooleanField()
    coffee_price = StringField("Avg Price of Coffee", validators=[DataRequired()])
    submit = SubmitField("Add your Cafe!")


@app.route("/")
def home():
    cafes = Cafe.query.all()
    return render_template("index.html", all_cafes=cafes)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddCafe()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            seats=form.seats.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            coffee_price=form.coffee_price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=form)


@app.route("/delete/<int:cafe_id>")
def delete(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
