from app import app
from flask import render_template, flash, redirect, session, url_for, request, g

@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'Miguel'}  # fake user
	g.user = user
	return  render_template('index.html', title='Home', user=user)

@app.route('/register' , methods=['GET','POST'])
def register():
	print "Registering"

@app.route('/ratemovies')
@app.route('/ratemovies/<int:page>')
def ratebooks(page=1):
	print "Rating books:"
