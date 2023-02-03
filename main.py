from flask import Flask, render_template, flash, request, Response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, EmailField
from wtforms.validators import DataRequired, EqualTo, Length

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from datetime import datetime
# import pymysql
from os import environ, path
from dotenv import load_dotenv

from werkzeug.security import generate_password_hash, check_password_hash




# Set path to .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

app = Flask(__name__)



# Add Database
# DATABASE='mysql://user:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = str(environ.get('DATABASE'))
# Secret key
app.config['SECRET_KEY'] = str(environ.get('SECRET_KEY'))
# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Create Model
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(60))
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    # passwrd
    password_hash = db.Column(db.String(128))
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name


# Create a Form Class
class NameForm(FlaskForm):
    name =  StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class PasswordForm(FlaskForm):
    email =  EmailField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class UserForm(FlaskForm):
    name =  StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite color")
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must match')])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField('Submit')

# Json thing




@app.route('/test_pw', methods = ['GET', 'POST'])
def test_pwd():
    email = None
    password = None
    passed = None
    
    form = PasswordForm()
    # Validate form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        
        # check user
        user = users.query.filter_by(email = email).first()
        if user:
            passed = user.verify_password(password)
            print(passed)
                
        # Clear form
        form.email.data = ''
        form.password_hash.data = ''
    return render_template('test_pwd.html', email=email, password = password, form = form)
        


@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!")
        
        our_users = users.query.order_by(users.date_added)
        return render_template('add_user.html', form=form, name=name, our_users=our_users)
    except:
        flash("Something goes wrong")
        our_users = users.query.order_by(users.date_added)
        return render_template('add_user.html', form=form, name=name, our_users=our_users)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = users.query.get_or_404(id)

    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash("User Updated Successfully")
            our_users = users.query.order_by(users.date_added)
            return render_template('update.html', form=form, name_to_update=name_to_update,our_users=our_users)
        except:
            flash("Something goes wrong, Try Again")
            our_users = users.query.order_by(users.date_added)
            return render_template('update.html', form=form, name_to_update=name_to_update, our_users=our_users)
    else:
        our_users = users.query.order_by(users.date_added)
        return render_template('update.html', form=form, name_to_update=name_to_update, our_users=our_users)

@app.route('/user/add', methods = ['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Password hash
            hashed_password = generate_password_hash(form.password_hash.data, "sha256")
            user = users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''
        flash('User Added Successfully')
    our_users = users.query.order_by(users.date_added)
    return render_template('add_user.html', form=form, name=name, our_users=our_users)

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
       flash("Form Submitted Sucessfully")

    return render_template('name.html',
    title="Name",
    name = name,
    form = form)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500



if __name__ == '__main__':
    port = int(environ.get("PORT", 9002))
    app.run(debug=True, host="0.0.0.0", port=port)