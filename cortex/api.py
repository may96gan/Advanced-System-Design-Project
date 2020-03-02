#!/usr/bin/python

from flask import Flask
from flask import request
from bson.objectid import ObjectId
import click
import pymongo

class Log:
    
    def __init__(self):
        self.quiet = False
        self.traceback = False

    def __call__(self, message):
        if self.quiet:
            return
        if self.traceback and sys.exc_info(): # there's an active exception
            message += os.linesep + traceback.format_exc().strip()
        click.echo(message)


log = Log()

@click.group()
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback




@main.command('run-server')
@click.option('-h','--host', default='127.0.0.1')
@click.option('-p','--port', default=5000)
@click.option('-d', '--database', default='mongodb://localhost:27017/')
def run_api_server(host='127.0.0.1', port=5000, database='mongodb://localhost:27017/'):
    client = pymongo.MongoClient(database)
    db = client.db

    app = Flask(__name__)

    @app.route('/users', methods = ['GET'])
    def getUsers():
        return {'currentUsers':list(db.users.find({}, {'user_id': True, 'username':True, '_id': False}))}, 200

    @app.route('/users/<int:user_id>', methods = ['GET'])
    def getUser(user_id):
        user = db.users.find_one({'user_id':str(user_id)},{'_id':False})
        if not user:
            return 'User Not Found', 404
        return user, 200
    
    @app.route('/users/<int:user_id>/snapshots', methods = ['GET'])
    def getUserSnapshots(user_id):
        if not db.users.find_one({'user_id':str(user_id)}):
            return 'User Not Found', 404
        return {'currentSnapshots':list(db.snapshots.find({'user_id':str(user_id)},{str('_id'):True,'datetime':True}))}, 200
    
    @app.route('/users/<int:user_id>/snapshots/<snapshot_id>', methods = ['GET'])
    def getUserSnapshot(user_id, snapshot_id):
        if not db.users.find_one({'user_id':str(user_id)}):
            return 'User Not Found', 404
        snapshot = db.snapshots.find_one({'user_id':str(user_id),'_id':snapshot_id})
        print("AAAAAAAAAAAAAAAAAAAAA")
        print(snapshot_id)
        if not snapshot:
            return 'Snapshot Not Found For This User', 404
        res = []
        if 'pose' in snapshot:
            res.append('pose')
        if 'feelings' in snapshot:
            res.append('feelings')
        return {'_id':snapshot['_id'], 'datetime':snapshot['datetime'],'results':res}, 200

    @app.route('/users/<int:user_id>/snapshots/<snapshot_id>/<result_name>', methods = ['GET'])
    def getSnapshotResult(user_id, snapshot_id, result_name):
        if not db.users.find_one({'user_id':str(user_id)}):
            return 'User Not Found', 404
        snapshot = db.snapshots.find_one({'user_id':str(user_id),'_id':snapshot_id})
        if not snapshot:
            return 'Snapshot Not Found For This User', 404
        if result_name not in snapshot:
            return 'Result Is not Available', 404
        return snapshot[result_name], 200


    app.run(host = host,port = port,threaded=True)
    

if __name__ == '__main__':
    main()
