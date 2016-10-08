#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
from pymongo import MongoClient
from global_congif import host,port,client_db,client_collection
import json

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()
client = MongoClient(host,port)
db=client[client_db]
col=db[client_collection]

@auth.get_password
def get_password(username):
	if username == 'monotif':
		return 'python'
	return None

@auth.error_handler
def unauthorized():
	return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
	# return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    
@app.errorhandler(400)
def not_found(error):
	return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'error': 'Not found' } ), 404)


@app.route('/', methods = ['GET'])
@auth.login_required


def verify_client():
	""" Function for user to check if he already has any subscription 
		required fields : client_name & client email	
	"""
	data=json.dumps(request.data)
	if not data or not 'client_name' in data or not 'client_email' in data :
		print "error"
		abort(400)
	try:
		doc=col.find_one(json.loads(request.data))
		if doc:
			doc.pop("_id")
		else:
			return(jsonify({"response":"Subscription not found !!"}))
	except Exception as e:
		print e
	return jsonify(doc)


@app.route('/', methods = ['POST'])
@auth.login_required
def create_client():
	""" Function for a new user to subscribe
		required fields : client_name , client email & subscription
	"""
	""" Assuming the POST data is in correct schema for insertion (Can be validated at frontend)
		Else a validation function can be added to check the schema of the POST data

	"""
	data=json.loads(request.data)
	try:
		if col.insert(data):
			return jsonify({"response":"Success !!"})
		else:
			return jsonify({"response":"Subscription failed !!"})
	except Exception as e:
		print e
		


@app.route('/', methods = ['PUT'])
@auth.login_required
def update_subscription():
	""" Function for client to update his/her subscription
		required : client_name , client email & subscription(with new values)
	"""
	""" Assuming the PUT data is in correct schema for update (Can be validated at frontend)
		Else a validation function can be added to check the schema of the PUT data

	"""
	#	The function will find the matching client_name and client_email and will update the subscription field

	data=json.loads(request.data)
	subscription={"subscription":data.pop("subscription")}
	try:
		response=col.update(data,{"$set":{"subscription":subscription}})
		if response["updatedExisting"]==True:
			return jsonify({"response":"Success !!"})
		else:
			return jsonify({"response":"Update failed !!"})
	except Exception as e :
		print e


@app.route('/', methods = ['DELETE'])
@auth.login_required
def delete_subscription():
	""" Function for client to delete his/her subscription
		required : client_name,client_email
	"""
	data=json.loads(request.data)
	try:
		response=col.remove(data)
		if response['n']==1:
			return jsonify({"response":"Success !!"})
		else:
			return jsonify({"response":" Subscription deletion failed !!"})

	except Exception as e:
		print e
		
if __name__ == '__main__':
    app.run(debug = True)