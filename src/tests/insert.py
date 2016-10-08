"""
	Test script to insert new data into the database

"""
from test_config import watch_db,watch_collection,host,port
from pymongo import MongoClient
client = MongoClient(host,port)
import time
db=client[watch_db]
col=db[watch_collection]
from random import randint

while True:
	status=col.update({"_id":1},{"artist_name":"johny","address":"sdfnskdnf","company":str(randint(0,10000)),"children":"123"},upsert=True)
	print status
	col.update({"_id":2},{"artist_name":"randy","address":"sdfnskdnf","company":str(randint(0,10000)),"children":"123"},upsert=True)
	print "inserted"
	time.sleep(1)
client.close()



