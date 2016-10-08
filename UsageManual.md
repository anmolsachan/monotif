Dependencies 
```
             - MongoDB setup with replica set enabled(Atleast single node replica)
             - Python (2.7.x)(Already present in linux)
             - Anaconda (Python)
             - Python Flask with httpauth
```
             
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
```

6) Installing git and configurations
```
https://guides.github.com/
https://www.atlassian.com/git/tutorials/
```

7) Cloning the app Repository
````
git clone https://github.com/anmolsachan/monotif
````

8) Making changes to configurations(According to users choice)
```
Move to src directory in cloned repo.
Edit file - global_config.
Set watch_db to the database name on which monitoring has to be setup.
Set watch_collection to the collection name on which monitoring has to be setup.
Set the email from which the notifications have to be sent.
Set the password for email from which the notifications have to be sent.
```

9) Running the app
```
From the cloned rep run the make the file run.sh executable
  chmod +x run.sh
Execute the file run.sh from terminal
  ./run.sh
```
