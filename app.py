import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
auth = HTTPBasicAuth()

from ml.engine import MLEngine
engine = MLEngine(os.path.join('./datastore', 'datasets'))
model = engine.train_model(saveWeights=True)

if not app.debug:
	import logging
	from logging.handlers import RotatingFileHandler
	file_handler = RotatingFileHandler('datastore/MovieRecommender.log', 'a', 1 * 1024 * 1024, 10)
	file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	app.logger.setLevel(logging.INFO)
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.info('BookRecommender startup')

from controllers import webcontroller, apicontroller
from models.model import User

#login manager callback to load user
@lm.user_loader
def load_user(id):
	return User.query.get(int(id))


