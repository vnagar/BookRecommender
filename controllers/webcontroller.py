from datetime import datetime
from app import app
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from views.forms import LoginForm, RegisterForm, EditForm
from models.model import User, Book

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated:
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
	user = g.user
	books = Book.query.limit(6).all()
	return  render_template('index.html', title='Home', user=user, books=books)

@app.route('/register' , methods=['GET','POST'])
def register():
	form = RegisterForm()

	if form.validate_on_submit():
		user = User(form.username.data, form.password.data, form.email.data)
		db.session.add(user)
		db.session.commit()

		#make the user follow him/herself
		db.session.add(user.follow(user))
		db.session.commit()

		flash('User successfully registered')
		return redirect('/login')
	return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for ="%s", remember_me=%s' %
			(form.username.data, str(form.remember_me.data)))
		session['remember_me'] = form.remember_me.data
		registered_user = User.query.filter_by(username=form.username.data).first()
		if not registered_user or not registered_user.verify_password(form.password.data):
			flash('Username or password is invalid', 'error')
			return redirect(url_for('login'))
		remember_me = False
		if 'remember_me' in session:
			remember_me = session['remember_me']
			session.pop('remember_me', None)
		login_user(registered_user, remember=remember_me)
		flash('Logged in successfully')
		return redirect(request.args.get('next') or url_for('index'))
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first()
	if user == None:
		flash('User %s not found.' %username)
		return redirect(url_for('index'))
	posts = [
		{'author': user, 'body': 'Test post #1'},
		{'author': user, 'body': 'Test post #2'}
	]
	return render_template('user.html', user=user, posts=posts)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
	form = EditForm(g.user.username)
	if form.validate_on_submit():
		g.user.username = form.username.data
		g.user.about_me = form.about_me.data
		db.session.add(g.user)
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit'))
	else:
		form.username.data = g.user.username
		form.about_me.data = g.user.about_me
	return render_template('edit.html', form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('User %s not found.' %username)
		return redirect(url_for('index'))
	if user == g.user:
		flash('You cannot follow yourself!')
		return redirect(url_for('user', username=username))
	u = g.user.follow(user)
	if u is None:
		flash('Cannot follow ' + username + '.')
		return redirect(url_for('user', username=username))
	db.session.add(u)
	db.session.commit()
	flash('You are now following ' + username + '!')
	return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('User %s not found.' % username)
		return redirect(url_for('index'))
	if user == g.user:
		flash('You can\'t unfollow yourself!')
		return redirect(url_for('user', username=username))
	u = g.user.unfollow(user)
	if u is None:
		flash('Cannot unfollow ' + username + '.')
		return redirect(url_for('user', username=username))
	db.session.add(u)
	db.session.commit()
	flash('You have stopped following ' + username + '.')
	return redirect(url_for('user', username=username))

@app.route('/ratebooks')
@app.route('/ratebooks/<int:page>')
@login_required
def ratebooks(page=1):
	books = Book.query.paginate(page, 24, False)
	if books.has_next:
		print "There are next books"
	if books.has_prev:
		print "There are prev books"

	return render_template('ratebooks.html', user=g.user, books=books)

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500

