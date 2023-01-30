from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    favorite_pizza = ["Pepperoni", "Cheese", "Mushorons", 41]
    return render_template("home.html", title="Home", favorite_pizza=favorite_pizza)

@app.route('/user/<name>')
def profile(name):
    return render_template("profile.html", title="Profile", name=name)

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 9002))
    app.run(debug=True, host="0.0.0.0", port=port)