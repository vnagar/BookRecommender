import os
import numpy as np
from app import app
from flask import jsonify, request
from ml.engine import MLEngine
from config import datasetdir

@app.route('/api')
@app.route('/api/index')
def api_index():
	return jsonify("Hello, World!")

@app.route('/api/predict', methods=['POST'])
def api_predict():
	print "Data:{}".format(request.data)
	linebits = request.data.split(',')
	newList = np.asfarray(linebits)
	engine = MLEngine(datasetdir)
	prediction = engine.predictImage(newList)
	return jsonify(prediction)
