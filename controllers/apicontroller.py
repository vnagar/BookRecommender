import os
import numpy as np
from flask import abort, url_for, request, g, jsonify
from app import app, engine, db
from ml.engine import MLEngine
from config import datasetdir
from models.model import User, Book

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
def api_index():
	return jsonify("Hello, World!")

@app.route('/api/predict', methods=['POST'])
def api_predict():
	print "Data:{}".format(request.data)
	linebits = request.data.split(',')
	newList = np.asfarray(linebits)
	prediction = engine.predictImage(newList)
	return jsonify(prediction)
