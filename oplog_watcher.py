from pymongo.cursor import _QUERY_OPTIONS
import pymongo
from oplog_config import host,port,changes_db,changes_collection,sleep
from pymongo import MongoClient
import time
from global_congif import watch_db,watch_collection

def doc_insertor(doc):
	"""  Function to insert documents caught by oplog watcher whose updates have to notified to the client """
	updated_client=doc["ns"]
	watch_client=watch_db+"."+watch_collection
	if updated_client==watch_client:
		try:
			client = MongoClient(host,port)
			db=client[changes_db]
			col=db[changes_collection]
			doc=doc["o"]
			doc["status"] ="unnotified"
			doc["doc_id"] = doc.pop("_id")
			col.insert(doc)
			client.close()
		except Exception as e:
			print "Mongo changed doc Insertion failed"
			print e

def watcher():
	"""  Function to monotor oplog and detect changes and update into the collection which contains updated documents """
	try:
		client = MongoClient(host,port)
		db=client["local"]
		tail_opts = { 'tailable': True, 'await_data': True }
		# get the latest timestamp in the database
		last_ts = db.oplog.rs.find().sort('$natural', -1)[0]['ts']
		print last_ts
		while True:
			query = { 'ts': { '$gt': last_ts } }  						#To get the latest timestamp from the oplog
			cursor = db.oplog.rs.find(query, **tail_opts)				#To get the docs which have been changed from the oplog
			cursor.add_option(_QUERY_OPTIONS['oplog_replay'])
			while cursor.alive:
				try:
					doc=cursor.next()
					print doc
					doc_insertor(doc)									#Inserting found docs into a saperate database for leter processing for notifications.
				except StopIteration as e:
					print e,"@"
					time.sleep(sleep)
	except Exception as e:
		print("Unable to run oplog_watcher")                            #This error will mostly come if either mongo is not running or replica set is not configured for oplog
		print e
		
if __name__ == '__main__':
	watcher()
