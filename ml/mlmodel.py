
from keras.models import Sequential
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dense

class MLModel:
	@staticmethod
	def build(width, height, depth, classes, weightsPath=None):
		#initialize the model
		model = Sequential()
		
		#first set of CONV => RELU => POOL
		# 20 convolution filter of size 5x5
		model.add(Convolution2D(20, 5, 5, border_mode="same", input_shape=(depth, height, width)))
		model.add(Activation("relu"))
		model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2)))

		# second set of CONV => RELU => POOL
		# 50 convolution filter of size 5x5
		model.add(Convolution2D(50, 5, 5, border_mode="same"))
		model.add(Activation("relu"))
		model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

		#fully connected or Dense layers
		# set of FC => RELU layers
		# take output of prev MaxPooling layer and flatten into single vector
		model.add(Flatten())
		model.add(Dense(500))
		model.add(Activation("relu"))

		# softmax classifier
		model.add(Dense(classes))
		model.add(Activation("softmax"))

		if weightsPath is not None:
			#load model from weights
			model.load_weights(weightsPath)
	
		return model


