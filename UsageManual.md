Dependencies - MongoDB setup with replica set enabled(Atleast single node replica)
             - Python (2.7.x)
             - Anaconda (Python)
             - Python Flask with httpauth
             
1) Installing MongoDB
```
    https://docs.mongodb.com/manual/administration/install-on-linux/
```
2) Setting up replica set for oplog
```
#stop running instance
sudo service mongod stop
#start new instance with --replSet
sudo mkdir -p /data/db
sudo chown -R $USER_NAME /data/db
mongod --replSet myDevReplSet &
#connect to mongo
mongo
>rs.initiate()
#you can now start doing operations in mongo and should see oplog getting populated.
```

3) Installing Anaconda and configure for python2.7
```
https://docs.continuum.io/anaconda/install#linux-
http://conda.pydata.org/docs/py2or3.html
http://conda.pydata.org/docs/get-started.html
http://conda.pydata.org/docs/_downloads/conda-cheatsheet.pdf
```

4) Installing PYMONGO
```
https://anaconda.org/anaconda/pymongo
conda install -c anaconda pymongo=3.3.0
```

5) Installing Flask
````
https://anaconda.org/anaconda/flask
conda install -c anaconda flask=0.11.1
conda install -c melund flask-httpauth=2.3.0
````



