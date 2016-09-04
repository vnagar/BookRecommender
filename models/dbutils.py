
import imp
import os.path
import numpy as np
import pandas as pd
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
from models.model import Book

class DBUtils:
	def __init__(self):
		print "Initializing DBUtils"

	@staticmethod
	def db_create():

		db.create_all()

		if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
			api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
			api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		else:
			api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

	@staticmethod
	def db_migrate():

		v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
		tmp_module = imp.new_module('old_model')
		old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		exec(old_model, tmp_module.__dict__)
		script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
		open(migration, "wt").write(script)
		api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		print('New migration saved as ' + migration)
		print('Current database version: ' + str(v))

	@staticmethod
	def db_upgrade():
		api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		print('Current database version: ' + str(v))

	@staticmethod
	def db_downgrade():
		v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
		v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		print('Current database version: ' + str(v))

	@staticmethod
	def import_books():
		books_filename = os.path.join("datastore/datasets", "Books.csv")
		df = pd.read_csv(books_filename,header=0, sep=';')
		for index, row in df.iterrows():
			name = row['Book-Title'].decode("ISO-8859-1")
			author = row['Book-Author'].decode("ISO-8859-1")
			isbn = row['ISBN'].decode("ISO-8859-1")
			url = row['Image-URL-S'].decode("ISO-8859-1")
			print name, author, isbn, url 
			book = Book(name, author, isbn, url)
			db.session.add(book)

		db.session.commit()

		print "QUERYING THE DB for books..."
		books = Book.query.all()
		for book in books:
			print "Book name is %s" %book.name

