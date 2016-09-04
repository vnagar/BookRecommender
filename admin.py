import os
import argparse

def create_datastore_dirs(path):
	try: 
		if not os.path.isdir(path):
			print "Creating directory %s" %path
			os.makedirs(path)
		else:
			print "Directory %s already exists" %path

	except OSError:
		if not os.path.isdir(path):
			raise

dataset_path = os.path.join('.', 'datastore')
create_datastore_dirs(dataset_path)
dataset_path = os.path.join(dataset_path, 'datasets')
create_datastore_dirs(dataset_path)

from app import app
from models.dbutils import DBUtils
from ml.engine import MLEngine

ap = argparse.ArgumentParser(add_help=False)
subparsers = ap.add_subparsers(dest='cmd')
parser_start = subparsers.add_parser("start", help="start the server")
parser_create = subparsers.add_parser("create_db", help="create the db")
parser_create = subparsers.add_parser("import_books", help="import the books")
parser_migrate = subparsers.add_parser("migrate_db", help="migrate db")
parser_upgrade = subparsers.add_parser("upgrade_db", help="upgrade db")
parser_downgrade = subparsers.add_parser("downgrade_db", help="downgrade db")
parser_train = subparsers.add_parser("train_model", help="train the model")
parser_train = subparsers.add_parser("predict", help="test prediction")

dbutil = DBUtils()
args = ap.parse_args()

if args.cmd == 'start':
	app.run(debug=True)
elif args.cmd == 'create_db':
	print "Creating db..."
	dbutil.db_create()
elif args.cmd == 'import_books':
	print "In import books"
	dbutil.import_books()
elif args.cmd == 'migrate_db':
	print "Migrating db..."
	dbutil.db_migrate()
elif args.cmd == 'upgrade_db':
	print "Upgrading db..."
	dbutil.db_upgrade()
elif args.cmd == 'downgrade_db':
	print "Downgrading db..."
	dbutil.db_downgrade()
elif args.cmd == 'train_model':
	print "Training model..."
	engine = MLEngine(dataset_path)
	engine.train_model(saveWeights=True)
elif args.cmd == 'predict':
	print "Predicting model..."
	engine = MLEngine(dataset_path)
	engine.predict()
else:
	print "Unknown command"

