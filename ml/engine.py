import os
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
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

		ratings_filename = os.path.join(self.dataset_path, "Book-Ratings.csv")
		books_filename = os.path.join(self.dataset_path, "Books.csv")
		self.prefs = self.loadDataset(self.dataset_path)


	def loadDataset(self, path=""):
		""" To load the dataSet"
			Parameter: The folder where the data files are stored
			Return: the dictionary with the data
		"""
		#Recover the titles of the books
		self.books = {}
		for line in open(path+"/Books.csv"):
			line = line.replace('"', "")
			(id,title) = line.split(";") [0:2]
			self.books[id] = title
	
		#Load the data
		prefs = {}
		count = 0
		for line in open(path+"/Book-Ratings.csv"):
			line = line.replace('"', "")
			line = line.replace("\\","")
			(user,bookid,rating) = line.split(";")
			try:
				if float(rating) > 0.0:
					prefs.setdefault(user,{})
					prefs[user][bookid] = float(rating)
			except ValueError:
				count+=1
				print "value error found! " + user + bookid + rating
			except KeyError:
				count +=1
				print "key error found! " + user + " " + bookid
		return prefs

	def load_model(self):
		print "Loading model..."

	def train_model(self, saveWeights=True):
		#create model
		model = MLModel.build()
		#train model
		print("Training model...")
		print model.sim_distance(self.prefs,'98556', '180727')
		print model.sim_pearson(self.prefs,'98556', '180727')
		print model.topMatches(self.prefs,'98556',10,model.sim_distance)
		recommendations = model.getRecommendations(self.prefs,'180727')[0:3]
		for (val, item) in recommendations:
			print val, self.books[item]

		return model

	def predict(self):
		print "In predict"
