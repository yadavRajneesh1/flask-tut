from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import json

with open('config.json', 'r') as conf:
    params = json.load(conf)['params']
local_server = True
app = Flask(__name__)
app.secret_key = 'my-secret-key'
app.config.update(
    DEBUG=True,
    Mail_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['mail_user'],
    MAIL_PASSWORD=params['mail_pass']
)
mail = Mail(app)

if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

'''sno,name,email,phone_num,mass,date'''


class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    massages = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(20), nullable=True)


class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(12), nullable=False)
    tagline = db.Column(db.String(12), nullable=False)
    date = db.Column(db.String(20), nullable=True)
    img_file = db.Column(db.String(20), nullable=True)


@app.route('/')
def home():
    posts = Posts.query.filter_by().all()[0:params['no_of_post']]
    return render_template('index.html', params=params, posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', params=params)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        '''Add entries to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        phone_num = request.form.get('phone')
        date = request.form.get('date')

        entry = Contact(name=name, email=email, massages=message, phone_num=phone_num, date=datetime.now())

        db.session.add(entry)
        db.session.commit()
    # mail.send_message('New massage from' + name, sender=email, recipients=[params['mail_user']],
    #                body=message + "\n" + phone_num)

    return render_template('contact.html')


@app.route('/post/<string:post_slug>', methods=['GET'])
def post_rout(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()

    return render_template('post.html', params=params, post=post)


@app.route('/post', methods=['GET', 'POST'])
def dashboard():
    if 'user' in session and session['user'] == params['user_name']:
        posts = Posts.query.filter_by().all()
        return render_template('dashboard.html', params=params, posts=posts)
    if request.method == 'POST':
        username = request.form.get('uname')
        password = request.form.get('pass')
        if username == params['user_name'] and password == params['password']:
            session['user'] = username
            posts = Posts.query.filter_by().all()
            return render_template('dashboard.html', params=params, posts=posts)
    return render_template('login.html', params=params)


@app.route('/edit/<string:sno>', methods=['GET', 'POST'])
def edit(sno):
    if 'user' in session and session['user'] == params['user_name']:
        print("sno-----{}".format(sno))
        if request.method == 'POST':
            box_title = request.form.get('title')
            taglib = request.form.get('taglib')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            date = datetime.now()

            if sno == '0':
                print("sno1====={}".format(sno))
                post = Posts(title=box_title, tagline=taglib, slug=slug, content=content, img_file=img_file, date=date)
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sno).first()
                post.title = box_title
                post.tagline = taglib
                post.slug = slug
                post.content = content
                post.img_file = img_file
                post.date = date
                db.session.commit()
        return render_template('edit.html', params=params, sno=sno)


if __name__ == '__main__':
    app.run(debug=True)
