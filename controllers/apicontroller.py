import os
import numpy as np
from flask import abort, url_for, request, g, jsonify
from app import app, engine, db, auth
from ml.engine import MLEngine
from config import datasetdir
from models.model import User, Book

@auth.verify_password
def verify_password(username_or_token, password):
	# first try to authenticate by token
	user = User.verify_auth_token(username_or_token)
	if not user:
		#try to authenticate with username/password
		user = User.query.filter_by(username=username_or_token).first()
		if not user or not user.verify_password(password):
			return False
	g.user = user
	return True

@app.route('/api/token')
@auth.login_required
def get_auth_token():
	token = g.user.generate_auth_token()
	return jsonify({'token': token.decode('ascii') })


@app.route('/api/ratebook', methods=['POST'])
def rate_book():
	print "In rate book"
	bookid = request.json.get('bookid')
	print bookid
	rating = request.json.get('rating')
	print rating
	return jsonify({'result':'success'})

@app.route('/api/users', methods=['POST'])
def new_user():
	username = request.json.get('username')
	password = request.json.get('password')
	email = request.json.get('email')
	if username is None or password is None or email is None:
		abort(400, 'Missing user information') # missing arguments
	user = User.query.filter_by(username=username).first()
	if user is not None:
		abort(400, 'User already exists') # existing user
	user = User(username = username, password=password, email=email)
	db.session.add(user)
	db.session.commit()
	return jsonify({'username':user.username}), 201, {'Location': url_for('get_user', id = user.id, _external = True)}

@app.route('/api/users/<int:id>')
def get_user(id):
	user = User.query.get(id)
	if not user:
		abort(400, 'User does not exist')
	return jsonify({'username': user.username})

@app.route('/api')
@app.route('/api/index')
@auth.login_required
def api_index():
	return jsonify("Hello, World!")

@app.route('/api/predict', methods=['POST'])
def api_predict():
	print "Data:{}".format(request.data)
	linebits = request.data.split(',')
	newList = np.asfarray(linebits)
	prediction = engine.predictImage(newList)
	return jsonify(prediction)
