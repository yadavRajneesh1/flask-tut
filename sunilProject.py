from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
app.secret_key = 'development key'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@127.0.0.1/developerguide"
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgre-flask://Sunil_flaskapplication:@postgre-flaskapplication.cvrf1ckxxkpi.ap-south-1.rds.amazonaws.com/postgres"

db = SQLAlchemy(app)


class Login(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Email()])
    password = PasswordField('password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Send')


class user(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    UserEmail = db.Column(db.String(40))
    UserPassword = db.Column(db.String(40))


@app.route('/', methods=['GET', 'POST'])
def home():
    print("ram1")
    login = Login()
    print("ram2")
    if login.validate_on_submit():
        print("ram3")
        name = login.username.data
        password = login.password.data
        # name = request.form.get(login.username.name)
        # password = request.form.get(login.password.name)
        print(name)
        print(password)
        entry = user(UserEmail=name, UserPassword=password)
        db.session.add(entry)
        db.session.commit()
        return render_template('view.html', form=login)
        # name = request.form.get('username')
        # return "Form submitted Succesfully  " + login.username.data + " " + login.password.data
    return render_template('sindex.html', form=login)


@app.route('/view', methods=['GET', 'POST'])
def view():
    return render_template('view.html')


if __name__ == '__main__':
    app.run(debug=True)
