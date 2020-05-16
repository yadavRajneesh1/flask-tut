from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
app.secret_key = 'development key'
connection = psycopg2.connect(user="Sunil_flaskapplication", password="Sunilpostgre",
                              host="postgre-flaskapplication.cvrf1ckxxkpi.ap-south-1.rds.amazonaws.com", port="5432",
                              database="postgres")
cursor = connection.cursor()


class Login(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Email()])
    password = PasswordField('password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Send')


class Question(FlaskForm):
    Question = StringField('question', validators=[InputRequired()])
    option1 = StringField('option1', validators=[InputRequired()])
    option2 = StringField('option2', validators=[InputRequired()])
    option3 = StringField('option3', validators=[InputRequired()])
    option4 = StringField('option4', validators=[InputRequired()])


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
        insert_query = '''INSERT INTO public."user"(
        	 "UserEmail", "UserPassword")
        	VALUES (%s,%s);'''
        cursor.execute(insert_query, (name, password))
        connection.commit()

        return render_template('view.html', form=login)
        # name = request.form.get('username')
        # return "Form submitted Succesfully  " + login.username.data + " " + login.password.data
    return render_template('sindex.html', form=login)


@app.route('/ques', methods=['GET', 'POST'])
def ques():
    print("ram1")
    quest = Question()
    print("ram2")
    if quest.validate_on_submit():
        print("ram3")

        return render_template('question.html', quest=quest)
        # name = request.form.get('username')
        # return "Form submitted Succesfully  " + login.username.data + " " + login.password.data
    return render_template('question.html', quest=quest)


@app.route('/view', methods=['GET', 'POST'])
def view():
    return render_template('view.html')


if __name__ == '__main__':
    app.run(debug=True)
