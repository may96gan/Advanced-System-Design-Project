#!/usr/bin/python

import datetime
import flask
#from flask import request
#import requests
#from bson.objectid import ObjectId
import click
import pymongo

@click.group()
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    pass



@main.command('run-server')
@click.option('-h','--host', default='127.0.0.1')
@click.option('-p','--port', default=8080)
@click.option('-d','--database', default='mongodb://localhost:27017/')
def run_server(host='127.0.0.1', port=8080, database='mongodb://localhost:27017/'):
    client = pymongo.MongoClient(database)
    db = client.db
    
    app = flask.Flask(__name__)

    @app.route('/')
    def index():
        return flask.render_template('index.html')
    @app.route('/users', methods = ['GET'])
    def getUsers():
        users = list(db.users.find({}, {'user_id': True, 'username':True, '_id': False}))
        return flask.render_template('users.html', users=users)


    @app.route('/users/<int:user_id>', methods = ['GET'])
    def getUser(user_id):
        user = db.users.find_one({'user_id':str(user_id)},{'_id':False})
        if not user:
            return flask.render_template('notFound.html', error='user')
        user['birthday'] = datetime.datetime.fromtimestamp(user['birthday']/1000)
        g = user['gender']
        print(f"BEFORE user gender = {user['gender']}")
        if g == 0:
            user['gender'] = 'male'
        elif g == 1:
            user['gender'] = 'female'
        else:
            print("inside other")
            user['gender'] = 'other'
        print(f"AFTER user gender = {user['gender']}")
        return flask.render_template('user.html', user=user)
    
    @app.route('/users/<int:user_id>/snapshots', methods = ['GET'])
    def getUserSnapshots(user_id):
        user = db.users.find_one({'user_id':str(user_id)})
        if not user:
            return flask.render_template('notFound.html', error='user')
        snapshots = list(db.snapshots.find({'user_id':str(user_id)},{str('_id'):True,'datetime':True}))
        for s in snapshots:
            print(s['datetime'])
            s['datetime'] = datetime.datetime.fromtimestamp(int(s['datetime'])/1000)
        return flask.render_template('snapshots.html', user=user, snapshots=snapshots)
    
    @app.route('/users/<int:user_id>/snapshots/<snapshot_id>', methods = ['GET'])
    def getUserSnapshot(user_id, snapshot_id):
        user = db.users.find_one({'user_id':str(user_id)})
        if not user:
            return flask.render_template('notFound.html', error='user')
        snapshot = db.snapshots.find_one({'user_id':str(user_id),'_id':snapshot_id})
        if not snapshot:
            return flask.render_template('notFound.html', error='snapshot')
        res = []
        if 'pose' in snapshot:
            res.append('pose')
        if 'feelings' in snapshot:
            res.append('feelings')
        return flask.render_template('snapshot.html',user=user,id=snapshot['_id'], datetime=datetime.datetime.fromtimestamp(int(snapshot['datetime'])/1000),results=res)

    @app.route('/users/<int:user_id>/snapshots/<snapshot_id>/<result_name>', methods = ['GET'])
    def getSnapshotResult(user_id, snapshot_id, result_name):
        user = db.users.find_one({'user_id':str(user_id)})
        if not user:
            return flask.render_template('notFound.html', error='user')
        snapshot = db.snapshots.find_one({'user_id':str(user_id),'_id':snapshot_id})
        if not snapshot:
            return flask.render_template('notFound.html', error='snapshot')
        if result_name not in snapshot:
            return flask.render_template('notFound.html', error='result')
        return flask.render_template('result.html',name=result_name, results=[(k,v) for k,v in snapshot[result_name].items()])



    app.run(host = host,port = port,threaded=True)
    

if __name__ == '__main__':
    main()
