from flask import Flask, render_template, request, redirect, session, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json
from flask_mail import Mail

with open('config.json','r') as c:
    params = json.load(c)['params']
    # print(params['databaseurl'])

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = params['gmailusername']
app.config['MAIL_PASSWORD'] = params['gmailpassword']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

if params['localserver']:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['databaseurl']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['productionurl']

db = SQLAlchemy(app)

class Posts(db.Model):
    s_no = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80),nullable=False)
    description = db.Column(db.String(120),nullable=False)
    slug = db.Column(db.String(120),nullable=False)
    image = db.Column(db.String(120),nullable=False)
    date = db.Column(db.String(120),nullable=False)

class Contact(db.Model):
    s_no = db.Column(db.Integer, primary_key = True)
    s_name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    phn_no = db.Column(db.String(120))
    message = db.Column(db.String(120))

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))

@app.context_processor
def inject_year():
    return {'year': datetime.now().year}

@app.route('/')
def index():
    posts = Posts.query.filter_by().all()
    return render_template('index.html',image='home-bg.jpg',params=params,posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',image='about-bg.jpg',params=params)

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phn_no = request.form.get('phn_no')
        message = request.form.get('message')
        entry = Contact(s_name=name,email=email,phn_no=phn_no,message=message)
        db.session.add(entry)
        db.session.commit()
        mail.send_message(
            'New message from: ' + name,
            sender = email,
            recipients = [params['gmailusername']],
            body = message + '\n' + phn_no
        )
    return render_template('contact.html',image='contact-bg.jpg',params=params)

@app.route('/post/<string:post_slug>',methods=['GET'])
def post(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html',image=post.image,params=params,post=post)

@app.route('/dashboard',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Login.query.filter_by(email=email,password=password).first()
        if user == None:
            # session['adminEmail'] = ''
            # session['adminName'] = ''
            return render_template('dashboard/login.html', params=params,error='Invalid Credentials')
        else:
            # session['adminEmail'] = user.email
            # session['adminName'] = user.name
            return redirect('/dashboard/index')
    return render_template('dashboard/login.html',params=params)

@app.route('/dashboard/index')
def dashboardIndex(success=None):
    posts = Posts.query.filter_by().all()
    return render_template('dashboard/index.html',params=params,posts=posts,success=success)

@app.route('/dashboard/edit/<string:post_id>',methods=['GET','POST'])
def editPost(post_id):
    post = Posts.query.filter_by(s_no=post_id).first()
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.slug = request.form.get('slug')
        post.description = request.form.get('description')
        post.date = datetime.now().strftime('%d/%m/%Y')
        db.session.commit()
        flash('Successfully Edited Post', 'success')
        return redirect('/dashboard/index')

    return render_template('dashboard/edit.html',post=post,params=params)

@app.route('/dashboard/add',methods=['GET','POST'])
def addPost():
    if request.method == 'POST':
        title = request.form.get('title')
        slug = request.form.get('slug')
        description = request.form.get('description')
        image = request.form.get('image')
        entry = Posts(title=title,slug=slug,description=description,image=image,date=datetime.now().strftime('%d/%m/%Y'))
        db.session.add(entry)
        db.session.commit()
        flash('Successfully Added New Post', 'success')
        return redirect('/dashboard/index')
    return render_template('dashboard/add.html',params=params)

@app.route('/dashboard/delete/<string:post_id>',methods=['GET','POST'])
def deletePost(post_id):
    db.session.delete(Posts.query.get(post_id))
    db.session.commit()
    flash('Successfully Deleted Post','success')
    return redirect('/dashboard/index')

app.run(debug=True)