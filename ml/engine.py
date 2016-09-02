import os
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import datasets
from keras.optimizers import SGD
from keras.utils import np_utils
from ml.mlmodel import MLModel

class MLEngine:
	""" machine learning engine
    """

	def __init__(self, dataset_path):
		"""Init the engine with the dataset path
		"""
		print("Creating engine with dataset path=%s" %dataset_path)
		self.dataset_path = dataset_path
		self.weightsFile = os.path.join(dataset_path, 'weights.hdf5')

		print("[INFO] downloading MNIST...")
		dataset = datasets.fetch_mldata("MNIST Original")
		# reshape the MNIST dataset from a flat list of 784-dim vectors, to
		# 28 x 28 pixel images, then scale the data to the range [0, 1.0]
		# and construct the training and testing splits
		# reshape to 28x28
		data = dataset.data.reshape((dataset.data.shape[0], 28, 28))
		# add 1 channel per image for keras
		data = data[:, np.newaxis, :, :]
		(self.trainData, self.testData, self.trainLabels, self.testLabels) = train_test_split( data / 255.0, dataset.target.astype("int"), test_size=0.33)
		print "{Dims[0]} x {Dims[1]} x {Dims[2]} x {Dims[3]}".format(Dims=self.testData.shape)
		print self.testData[0]
		self.trainLabels = np_utils.to_categorical(self.trainLabels, 10)
		self.testLabels = np_utils.to_categorical(self.testLabels, 10)

	def load_model(self):
		model = MLModel.build(width=28, height=28, depth=1, classes=10, weightsPath=self.weightsFile)
		opt = SGD(lr=0.01)
		model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
		return model

	def train_model(self, saveWeights=True):
		#create model
		model = MLModel.build(width=28, height=28, depth=1, classes=10)
		opt = SGD(lr=0.01)
		model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

		#train model
		print("Training model...")
		model.fit(self.trainData, self.trainLabels, batch_size=128, nb_epoch=20, verbose=1)

		#show accuracy
		print("Evaluating model...")
		(loss, accuracy) = model.evaluate(self.testData, self.testLabels, batch_size=128, verbose=1)
		print("[INFO] accuracy: {:.2f}%".format(accuracy * 100))
		#save model
		print("Saving weights to file...")
		model.save_weights(self.weightsFile, overwrite=True)

		return model

	def predict(self):
		file = os.path.join(self.dataset_path, 'mnist_test_10.csv')
		f = open(file, 'r')
		a = f.readlines()
		f.close()
		for line in a:
			linebits = line.split(',')
			myInt = 255
			newList = [x / myInt for x in np.asfarray(linebits)]
			imageData = newList[1:]
			print "Actual label:{}".format(linebits[0])
			self.predictImage(imageData)

	def predictImage(self, data):
		model = self.load_model()

		imageData = np.asfarray(data).reshape((28,28))
		imageData = np.expand_dims(imageData, axis=0)
		imageData = np.expand_dims(imageData, axis=0)

		probs = model.predict(imageData)
		prediction = probs.argmax(axis=1)

		print "Prediction: {}".format(prediction[0])
		return prediction[0]
