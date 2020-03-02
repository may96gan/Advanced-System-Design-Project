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
        print("USER ID = ")
        print(user_id)
        print(f'top name = {topicName}')
        datetime = (json.loads(data))['snap_datetime']
        curUser = self.users.find_one({'user_id':user_id})
        if curUser: #and curUser.count() > 0:  user already exists in out users db, need to update
            #objectId = curUser['ObjectId']
            print("CUR USER EXISTS")
            curSnap = self.snapshots.find_one({'user_id':user_id, 'datetime':datetime})
            if curSnap: #curSnap.count() > 0: snapshot already exists in out snapshots db, need to update
                print("CUR SNAP EXISTS")
                addVal = {topicName:(json.loads(data))[topicName]}
                curSnap = {**curSnap, **addVal}
                print("in saver after cur snap, its now:")
                print(curSnap)
            else:
                print("CUR SNAP NOT EXISTS")
                curSnap = {'_id':str(ObjectId()),
                           'user_id':user_id,
                           'datetime':datetime,
                           topicName:(json.loads(data))[topicName],
                           }
            print("before res")
            result = self.snapshots.save(curSnap)
            print(result)
        else: # first insert user, then insert snapshot
            print("CUR USER NOT EXISTS")
            userJ = json.loads(data)
            result = self.users.insert_one({
                'user_id': user_id,
                'username': userJ['user_name'],
                'birthday': userJ['user_bday'],
                'gender': userJ['user_gender'],
            })
            print(result)
            result = self.snapshots.insert_one({
                'user_id': user_id,
                'datetime': datetime,
                topicName: userJ[topicName],
            })
            print(result)
        print("End of save. result:")
        print(self.users.find_one({'user_id':user_id}))
