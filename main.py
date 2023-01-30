from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import os

app = Flask(__name__)

app.config['SECRET_KEY'] = "superkey191919"


# Create a Form Class
class NameForm(FlaskForm):
    name =  StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField('Submit')



@app.route('/')
def index():
    favorite_pizza = ["Pepperoni", "Cheese", "Mushorons", 41]
    return render_template("home.html", title="Home", favorite_pizza=favorite_pizza)

@app.route('/user/<name>')
def profile(name):
    return render_template("profile.html", title="Profile", name=name)

@app.route('/name', methods = ['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    # Validate Form
    if form.validate_on_submit():
       name = form.name.data
       form.name.data = '' 

    return render_template('name.html',
    name = name,
    form = form)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 9002))
    app.run(debug=True, host="0.0.0.0", port=port)