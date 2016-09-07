import os
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from ml.mlmodel import MLModel
from models.model import User, Book, Rating

class MLEngine:
	""" machine learning engine
    """

	def __init__(self, dataset_path):
		"""Init the engine with the dataset path
		"""
		self.dataset_path = dataset_path
		self.weightsFile = os.path.join(dataset_path, 'weights.hdf5')

		ratings_filename = os.path.join(self.dataset_path, "Book-Ratings.csv")
		books_filename = os.path.join(self.dataset_path, "Books.csv")
		self.prefs = self.loadDataset(self.dataset_path)

	def getData(self):
		return self.prefs

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

		#Now load users and ratings from database
		users = User.query.all()
		for user in users:
			userid = str(user.id+500000)
			prefs.setdefault(userid, {})
			book_ratings = user.book_ratings
			for rating in book_ratings:
				#print rating.user.username, rating.book.name, rating.rating
				prefs[userid][rating.book.isbn] = float(rating.rating)

		self.prefs = prefs
		return prefs

	def add_book_rating(self, userid, bookid, rating):
		userid = str(userid + 500000)
		self.prefs.setdefault(userid,{})
		self.prefs[userid][bookid] = float(rating)
		print self.prefs[userid]

	def load_model(self):
		print "Loading model..."

	def train_model(self, saveWeights=True):
		#create model
		model = MLModel.build()
		"""
		print model.sim_distance(self.prefs,'98556', '180727')
		print model.sim_pearson(self.prefs,'98556', '180727')
		print model.topMatches(self.prefs,'98556',10,model.sim_distance)
		recommendations = model.getRecommendations(self.prefs,'180727')[0:3]
		for (val, item) in recommendations:
			print val, self.books[item]
		"""

		return model

	def predict(self):
		print "In predict"
