import datetime
from flask import Flask, render_template, request, jsonify, make_response, session
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email
from flask_sqlalchemy import SQLAlchemy
import uuid
import jwt
import psycopg2
import json

app = Flask(__name__)
with open("config.json", "r") as f:
    params = json.load(f)['params']
app.secret_key = params['secret_key']
app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Login(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Email()])
    password = PasswordField('password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Send')


class RegisterFree(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Email()])
    password = PasswordField('password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Submit')


class user(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    UserEmail = db.Column(db.String(40))
    UserPassword = db.Column(db.String(40))


class usernew(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(80), unique=True)
    UserEmail = db.Column(db.String(40), unique=True)
    UserPassword = db.Column(db.String(40))


@app.route('/', methods=['GET', 'POST'])
def home():
    print("ram1")
    login = Login()
    print("ram2")
    if login.validate_on_submit():
        data = request.form.get('username')
        print("data====={}".format(data))
        print("ram3")
        name = login.username.data
        # password = login.password.data
        hassed_password = generate_password_hash(login.password.data, method='sha256')
        # name = request.form.get(login.username.name)
        # password = request.form.get(login.password.name)
        print(name)
        # print(password)
        entry = user(UserEmail=name, UserPassword=hassed_password)
        db.session.add(entry)
        db.session.commit()
        return render_template('view.html', form=login)
        # name = request.form.get('username')
        # return "Form submitted Succesfully  " + login.username.data + " " + login.password.data
    return render_template('sindex.html', form=login)


@app.route('/user', methods=['POST'])
def create_user():
    registerFree = RegisterFree()
    if registerFree.validate_on_submit():
        data = request.form.get('username')
        name = registerFree.username.data
        hassed_password = generate_password_hash(request.form.get('password'), method='sha256')
        entry = usernew(public_id=str(uuid.uuid4()), UserEmail=request.form.get('username'),
                        UserPassword=hassed_password)
        db.session.add(entry)
        db.session.commit()
        return jsonify({'message': 'New User Created'})
    return render_template('newIndex.html', form=registerFree)


@app.route('/user', methods=['GET'])
def get_all_user():
    users = usernew.query.all()
    output = []
    for User in users:
        User_data = {'public_id': User.public_id, 'username': User.UserEmail, 'password': User.UserPassword}
        output.append(User_data)
    # return json.dumps(output)
    # j = json.dumps(output)
    return jsonify({'users': output})


@app.route('/user/<public_id>', methods=['GET'])
def get_one_user(public_id):
    userone = usernew.query.filter_by(public_id=public_id).first()
    if not userone:
        return jsonify({'Message': 'No user found'})
    output = []
    User_data = {'public_id': userone.public_id, 'username': userone.UserEmail, 'password': userone.UserPassword}
    output.append(User_data)
    return jsonify({'users': output})


@app.route('/user/<public_id>', methods=['PUT'])
def promote_user(public_id):
    return 'ram'


@app.route('/user/<public_id>', methods=['DELETE'])
def delete_user(public_id):
    userone = usernew.query.filter_by(public_id=public_id).first()
    if not userone:
        return jsonify({'Message': 'No user found'})
    db.session.delete(userone)
    db.session.commit()
    return jsonify({'Message': 'User Deleted Successfully'})


@app.route('/login', methods=['GET', 'POST'])
def login():
    log = Login()
    print("login====1")
    if log.validate_on_submit():
        print("login====2")
        print(request)
        auth = request.authorization
        print("auth-------{}".format(auth))
        if not auth or not auth.username or not auth.password:
            return make_response('could not verify correctly eigher username or password or both')
        userone = usernew.query.filter_by(UserEmail=auth.username).first()
        if not userone:
            return make_response('Please make you account before login')
        if check_password_hash(userone.UserPassword, auth.password):
            token = jwt.encode(
                {'public_id': userone.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)},
                app.config['secret_key'])
            return jsonify({'token': token.decode('UTF-8')})
    print("login====3")
    return render_template('newlogin.html', form=log)


@app.route('/loginnew', methods=['GET', 'POST'])
def loginnew():
    log = Login()
    if request.method == 'POST':
        session.pop('username', None)
        username = request.form['username']
        password = request.form['password']
        print(username)
        print(password)
        userone = usernew.query.filter_by(UserEmail=username).first()
        #print(userone.UserEmail)
        if userone and check_password_hash(userone.UserPassword, password):
            session['user_id']=userone.public_id
            return '<h1>you are login</h1>'
        return '<h1>Please make sure your credentials your username or password or both are incorrect</h1>'

    return render_template('newlogin.html', form=log)


@app.route('/view', methods=['GET', 'POST'])
def view():
    return render_template('view.html')


@app.route('/test', methods=['GET', 'POST'])
def test():
    data = request.args.get('name')
    passw = request.args['password']
    print(data)
    print(passw)
    # return jsonify({'Message': 'New user created'})
    return '''<h1>My name is {} and password is {}</h1>'''.format(data, passw)


@app.route('/jtest', methods=['GET', 'POST'])
def jtest():
    req_data = request.get_json()
    print(req_data)
    name = req_data['name']
    passw = req_data['password']
    print(name)
    print(passw)
    # return jsonify({'Message': 'New user created'})
    return '''<h1>My name is {} and password is {}</h1>'''.format(name, passw)


if __name__ == '__main__':
    app.run(debug=True)
