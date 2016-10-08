Dependencies - MongoDB setup with replica set enabled(Atleast single node replica)
             - Python (2.7.x)

1. Installing MongoDB

```
    https://docs.mongodb.com/manual/administration/install-on-linux/
```
2. Setting up replica set for oplog

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
