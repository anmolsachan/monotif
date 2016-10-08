"""
Test script to test Http flask server

"""

import requests
from requests.auth import HTTPBasicAuth
import json
from random import randint


def get():
		client={
   "client_name": "anmol",
   "client_email": "anmol13694@gmail.com",
}
		r=requests.get('http://localhost:5000/',data=json.dumps(client), auth=HTTPBasicAuth('monotif', 'python'))
		print r.json()

def post():
	subscription={
   "client_name":"xyz",
   "client_email": "xyz@gmail.com",
   "subscription": [
     {
       "artist_name": [
         "jimmy",str(randint(0,100))
      ],
       "fields": [
         "all" 
      ] 
    },
     {
       "artist_name": [
         "randy" 
      ],
       "fields": [
         "address",
         "children" 
      ] 
    } 
  ] 
}
	r=requests.post('http://localhost:5000/',data=json.dumps(subscription), auth=HTTPBasicAuth('monotif', 'python'))
	print r.json()

def put():
	subscription={
   "client_name": "anmol",
   "client_email": "anmol13694@gmail.com",
   "subscription": [
     {
       "artist_name": [
         "johny",str(randint(0,100))
      ],
       "fields": [
         "all" 
      ] 
    },
     {
       "artist_name": [
         "randy" 
      ],
       "fields": [
         "address",
         "children" 
      ] 
    } 
  ] 
}
	r=requests.put('http://localhost:5000/',data=json.dumps(subscription), auth=HTTPBasicAuth('monotif', 'python'))
	print r.json()

def delete():
	client={
   "client_name": "xyz",
   "client_email": "xyz@gmail.com"
}

	r=requests.delete('http://localhost:5000/',data=json.dumps(client), auth=HTTPBasicAuth('monotif', 'python'))
	print r.json()



if __name__ == '__main__':
	get()
	post()
	put()
	delete()