import pymongo

class Saver:
    def __init__(self, database_url):
        self.database_url = database_url
        self.client = pymongo.MongoClient(database_url)
        self.db = self.client.db
        self.users = self.db.users
        self.snapshots = self.db.snapshots
    def save(topicName, data):
        user_id = (json.loads(data))['user_id']
        datetime = (json.loads(data))['datetime']
        curUser = self.users.find_one({'user_id':user_id})
        if curUser.count() > 0:
            objectId = curUser['ObjectId']
            curSnap = self.snapshots.find_one({'user_id':user_id, 'datetime':datetime})
            if curSnap.count() > 0:
                addVal = {topicName:data[topicName]}
                curSnap = {**curSnap, **addVal}
            else:
                curSnap = {'user_id':user_id,'datetime':datetime,topicName:data[topicName]}
            self.snapshots.save(curSnap)
         else:
            userJ = json.loads(data)
            result = self.users.insert_one({
                'user_id': user_id,
                'username': userJ['user_name'],
                'birthday': userJ['user_bday'],
                'gender': userJ['user_gender'],
            })
