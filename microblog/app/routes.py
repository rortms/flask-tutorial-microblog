from flask import render_template
from app import myapp
from app.forms import LoginForm


# Index View
@myapp.route('/')
@myapp.route('/index')
def index():
    user = {'username' : 'BamBam'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]    
    return render_template('index.html', title='Home', user=user, posts=posts)

# Login View
@myapp.route('/loging')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)
