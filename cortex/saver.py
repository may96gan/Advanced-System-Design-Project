import pymongo
import json 
from bson.objectid import ObjectId

class Saver:
    def __init__(self, database_url):
        self.database_url = database_url
        self.client = pymongo.MongoClient(database_url)
        self.db = self.client.db
        self.users = self.db.users
        self.snapshots = self.db.snapshots
    def save(self, topicName, data):
        user_id = (json.loads(data))['user_id']
        datetime = (json.loads(data))['snap_datetime']
        curUser = self.users.find_one({'user_id':user_id})
        if curUser: # user already exists in out users db, need to update
            curSnap = self.snapshots.find_one({'user_id':user_id, 'datetime':datetime})
            if curSnap: # snapshot already exists in out snapshots db, need to update
                addVal = {topicName:(json.loads(data))[topicName]}
                curSnap = {**curSnap, **addVal}
            else:
                curSnap = {'_id':str(ObjectId()),
                           'user_id':user_id,
                           'datetime':datetime,
                           topicName:(json.loads(data))[topicName],
                           }
            result = self.snapshots.save(curSnap)
        else: # first insert user, then insert snapshot
            userJ = json.loads(data)
            result = self.users.insert_one({
                'user_id': user_id,
                'username': userJ['user_name'],
                'birthday': userJ['user_bday'],
                'gender': userJ['user_gender'],
            })
            result = self.snapshots.insert_one({
                'user_id': user_id,
                'datetime': datetime,
                topicName: userJ[topicName],
            })

