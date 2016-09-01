import os

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


