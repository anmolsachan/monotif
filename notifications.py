from oplog_config import host,port,changes_collection,changes_db
from global_congif import main_field  # Imports field artist name ............not hardcoded for extensibility
from pymongo import MongoClient


def get_changed_docs():
	try:
		client = MongoClient(host,port)
		db=client[changes_db]
		col=db[changes_collection]
		docs=col.find({"status": "unotified"})
		client.close()
		return docs

	except Exception as e:
		print "Failed on fetching docs from changes db"
		print e
		return False

def fetch_clients(main_field,main_value):
	""" fetches client docs according to changed documents"""
	try:
		client = MongoClient(host,port)
		db=client[changes_db]
		col=db[changes_collection]

	"""
		Cases for diferent types in which main_field can be given
		Case1:	artist_name: only one artist
		Case2: 	artist_name: [list of multiple artists]
		Case3:  artist_name: all


	"""

	except Exception as e:
		print "Could not fetch"


def process_client():
	""" Process each client for their particular specification 
	Eg:  For instance, Blair only wants to track changes made to Chuck's whereabouts while Georgina wants to track everything about everyone.

	"""


def generate_notifications(changed_doc):
	print "generating"
	main_value=doc[main_field]
	clients=fetch_clients(main_field,main_value)
	for client in process_client



def driver_function():
	while True:
		docs=get_changed_docs()
		if docs != False and docs.count()>0 :
			for doc in docs:
				generate_notifications(doc)
		else:
			pass

if __name__ == '__main__':
	driver_function()