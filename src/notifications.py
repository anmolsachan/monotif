from oplog_config import host,port,changes_collection,changes_db
from global_congif import main_field  # Imports field artist name ............not hardcoded for extensibility
from global_congif import client_db,client_collection,email,password
from pymongo import MongoClient
from pymongo import bulk
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import threading
import json

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
		"""
			Assumed data structure for the client_collection
			{
  				"client_name": "anmol",
  				"client_email": "anmol13694@gmail.com",
				"subscription": [
				    {
				      "artist_name": ["johny"],
				      "fields":["all"]
				    },
				    {
				      "artist_name": ["randy"],
				      "fields":["address","children"]
				    }
  								]
			}
		"""
		
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
		#print query
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
	
	try:
		notification_fields=[] 							#fields to be sent in notifications	
		changed_doc_fields=changed_doc.keys()
		remove_field_list=["_id","doc_id","status"]  	# Fields irrelevent to the client (To be removed)
		for field in remove_field_list:
			changed_doc_fields.remove(field)         	# Removing irrelevent fields
		sub=(item for item in client_doc["subscription"] if (changed_doc[main_field] in item[main_field])).next()
		subscribed_fields=sub["fields"]
		#CASE 1: Subscription to particular fields
		if subscribed_fields!=["all"]:
			notification_fields=set(subscribed_fields).intersection(changed_doc_fields)
			notification_fields=list(notification_fields)
		#CASE 2: Subscription to all fields
		else:
			notification_fields=changed_doc_fields

		"""Assumed data structure of notification
		{
			"client name":"xyz"
			"clent email":"abc@xyz.com"
			.
			. fields to be notified
			.
		}
		"""

		notification={}								#Creating notification to be sent
		for field in notification_fields:
			notification[field]=changed_doc[field]
		notification[main_field]=changed_doc[main_field]
		notification["client_name"]=client_doc["client_name"]
		notification["client_email"]=client_doc["client_email"]
		return notification
	except Exception as e:
		print "Failed to generate notificaiton for given client"
		print e
		return False
	

def generate_notifications(changed_doc):
	print "generating"
	main_value=changed_doc[main_field]
	clients=fetch_clients(main_field,main_value)
	notifications_list=[]
	for client_doc in clients:
		notification=process_client(changed_doc,client_doc)
		if notification:
			notifications_list.append(notification)
	return notifications_list

# def send_email(notification):
# 	""" Function to generate email and send"""
# 	try:
# 		print notification
# 		fromaddr = email
# 		toaddr = notification["client_email"]
# 		msg = MIMEMultipart()
# 		msg['From'] = fromaddr
# 		msg['To'] = toaddr
# 		msg['Subject'] = "Monotif Notification"
		 
# 		#body = ', '.join("%s=%r" % (key,val) for (key,val) in notification.iteritems())
# 		body=str(notification)
# 		msg.attach(MIMEText(body, 'plain'))
		 
# 		server = smtplib.SMTP('smtp.gmail.com', 587)
# 		server.starttls()
# 		print fromaddr,password	
# 		server.login(fromaddr,password)
# 		text = msg.as_string()
# 		server.sendmail(fromaddr, toaddr, text)
# 		server.quit()
# 		return True
# 	except Exception as e:
# 		print e
# 		return False

def send_email(notification):
	to =notification["client_email"]
	subject ="Monotif Notification"
	body =str(notification)

	email_text = """\  
	From: %s  
	To: %s  
	Subject: %s

	%s
	""" % (email, ", ".join(to), subject, body)

	try:
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login(email,password)
		server.sendmail(email, to, email_text)
		server.close()
		print 'Email sent!'
		return True
	except Exception as e:
		print 'Something went wrong in sending email...'
		print e
		return False

def send_notifications(notifications):
	# T = threading.Thread
	# for notification in notifications:
	# 	while threading.active_count()>1:
	# 		continue
	# 	t = T(target=send_email,args=(notification,))
	# 	t.start()
	status=False
	for notification in notifications:
		print notification
		staus=send_email(notification)
	return status


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
				notifications=generate_notifications(doc)			# List of notifications to be sent
				status=send_notifications(notifications)
				if status:
					update_chaged_doc(doc)
		else:
			pass
		time.sleep(1)

if __name__ == '__main__':
	driver_function()