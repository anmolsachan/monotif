from oplog_config import host,port,changes_collection,changes_db
from global_congif import main_field  # Imports field artist name ............not hardcoded for extensibility
from global_congif import client_db,client_collection
from pymongo import MongoClient
from pymongo import bulk
import time
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
		db=client[client_db]
		col=db[client_collection]
		
		"""Cases for diferent types in which main_field can be given
		Case1:	artist_name: [only one artist]
		Case2: 	artist_name: [list of multiple artists]
		Case3:  artist_name: [all]
		"""

		# subscription is field name for each user
		query={"subscription":{
								"$elemMatch": {
												main_field : { "$in": ["all",main_value] }
												} 
							}              
			}
		print query
		client_docs=col.find()
		client.close()
		return client_docs
	except Exception as e:
		print "Could not fetch client documents"
		print e
		return[]

def process_client(changed_doc,client_doc):
	print "processing"
	""" Process each client for their particular specification 
	Eg:  For instance, Blair only wants to track changes made to Chuck's whereabouts while Georgina wants to track everything about everyone.

	"""


	print changed_doc,client_doc
	return "done"

def generate_notifications(changed_doc):
	print "generating"
	print changed_doc
	main_value=changed_doc[main_field]
	clients=fetch_clients(main_field,main_value)
	notifications_list=[]
	for client_doc in clients:
		print client_doc
		notifications=process_client(changed_doc,client_doc)
		notifications_list.extend(notifications)
	return notifications_list
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
				if status:
					update_chaged_doc(doc)
		else:
			pass
		time.sleep(1)

if __name__ == '__main__':
	driver_function()