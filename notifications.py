from oplog_config import host,port,changes_collection,changes_db
from global_congif import main_field  # Imports field artist name ............not hardcoded for extensibility
from pymongo import MongoClient
from pymongo import bulk

def get_changed_docs():
	""" Function to fetch docs which very whose notificatons have not been sen to the users. """
	try:
		client = MongoClient(host,port)
		db=client[changes_db]
		col=db[changes_collection]
		docs=col.find({"status": "unnotified"})
		client.close()
		return docs

	except Exception as e:
		print "Failed on fetching docs from changes db"
		print e
		return False

def fetch_clients(main_field,main_value):
	print "fetching"
	""" fetches client docs according to changed documents"""
	try:
		client = MongoClient(host,port)
		db=client[changes_db]
		col=db[changes_collection]
		
		"""Cases for diferent types in which main_field can be given
		Case1:	artist_name: [only one artist]
		Case2: 	artist_name: [list of multiple artists]
		Case3:  artist_name: [all]
		"""
		client_docs=col.find({"$or":[
										{main_field: { "$in": ["all",main_value] } }
			]})
		client.close()
		return client_docs
	except Exception as e:
		print "Could not fetch client documents"
		print e


def process_client(changed_doc,client):
	print "processing"
	""" Process each client for their particular specification 
	Eg:  For instance, Blair only wants to track changes made to Chuck's whereabouts while Georgina wants to track everything about everyone.

	"""
	print changed_doc,client
	return "done"

def generate_notifications(changed_doc):
	print "generating"
	print changed_doc
	main_value=changed_doc[main_field]
	clients=fetch_clients(main_field,main_value)
	for client in clients:
		print client
		notification=process_client(changed_doc,clients)
		
def send_notifications(notifications):
	return True


def update_chaged_doc(doc):
	""" Function to change the status to "notified" in changes_collections of the doc whose notification have been """			
	""" Can be configured to delete the doc to reduce load on db...............for now this just changes the status of the doc """
	try:
		client = MongoClient(host,port)
		db=client[changes_db]
		col=db[changes_collection]
		col.update(doc,{"$set":{"status":"Notified"}})
		client.close()
	except Exception as e:
		print "failed to update the ststus of doc in changed_db" 
		print e

def driver_function():
	while True:
		docs=get_changed_docs()
		if docs != False and docs.count()>0 :
			for doc in docs:
				print doc
				notifications=generate_notifications(doc) # List of notifications to be sent
				status=send_notifications(notifications)
				if staus:
					update_chaged_doc(doc)
		else:
			print "No Doc"
			pass

if __name__ == '__main__':
	driver_function()