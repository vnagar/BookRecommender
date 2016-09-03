from app import app
from flask import render_template, flash, redirect, session, url_for, request, g
from views.forms import LoginForm, RegisterForm, EditForm

@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'Miguel'}  # fake user
	g.user = user
	return  render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
	user = {'username': 'Miguel'}  # fake user
	g.user = user
	form = LoginForm()
	return render_template('login.html', title='Sign In', form=form)

@app.route('/register' , methods=['GET','POST'])
def register():
	print "Registering"

@app.route('/ratemovies')
@app.route('/ratemovies/<int:page>')
def ratebooks(page=1):
	print "Rating books:"
