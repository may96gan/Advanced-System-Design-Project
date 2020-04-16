import click
import json
import pika
from PIL import Image as PIL

def parse_pose(snapshot):
    json_user = (json.loads(snapshot))
    json_snap = (json.loads(snapshot))['pose']
    if not json_snap:
        return
    json_snap_t = json_snap['translation']
    json_snap_r = json_snap['rotation']
    if not json_snap_t or not json_snap_r:
        return 
    return json.dumps(dict( 
                        user_id = json_user['userId'],
                        user_name = json_user['username'],
                        user_bday = json_user['birthday'],
                        user_gender = json_user.get('gender',2),
                        snap_datetime = json_user.get('datetime'),
                        pose = dict(
                            tx = json_snap_t.get('x',0),
                            ty = json_snap_t.get('y',0),
                            tz = json_snap_t.get('z',0),
                            rx = json_snap_r.get('x',0),
                            ry = json_snap_r.get('y',0),
                            rz = json_snap_r.get('z',0),
                            rw = json_snap_r.get('w',0),
                        ),
    ))
#parse_pose.field = 'pose'

def parse_feelings(snapshot):
    json_user = (json.loads(snapshot))
    json_snap = (json.loads(snapshot))['feelings']
    if not json_snap:
        return
    return json.dumps(dict(
        user_id = json_user['userId'],
        user_name = json_user['username'],
        user_bday = json_user['birthday'],
        user_gender = json_user.get('gender',2),
        snap_datetime = json_user.get('datetime'),
        feelings = dict(
            hunger = json_snap.get('hunger',0),
            thirst = json_snap.get('thirst',0),
            exhaustion = json_snap.get('exhaustion',0),
            happiness = json_snap.get('happiness',0),
            ),
    ))
#parse_feelings.field = 'feelings'


def parse_color_image(snapshot):
    json_user = (json.loads(snapshot))
    json_snap = (json.loads(snapshot))['color_image']
    if not json_snap:
        return
    # path = context.path('color_image.jpg')
    size = snapshot.color_image.width, snapshot.color_image.height
    # image = PIL.new('RGB', size)
    # image.putdata(snapshot.color_image.data)
    # image.save(path)
    return json.dumps(dict(
        user_id = json_user['userId'],
        user_name = json_user['username'],
        user_bday = json_user['birthday'],
        user_gender = json_user.get('gender',2),
        snap_datetime = json_user.get('datetime'),
        color_image = dict(
            path = path,
            height = json_snap.get('height',0),
            width = json_snap.get('width',0),
        ),
    ))

def parse_depth_image(snapshot):
    json_user = (json.loads(snapshot))
    json_snap = (json.loads(snapshot))['depth_image']
    if not json_snap:
        return
    # path = context.path('color_image.jpg')
    size = snapshot.depth_image.width, snapshot.depth_image.height
    # image = PIL.new('RGB', size)
    # image.putdata(snapshot.color_image.data)
    # image.save(path)
    return json.dumps(dict(
        user_id = json_user['userId'],
        user_name = json_user['username'],
        user_bday = json_user['birthday'],
        user_gender = json_user.get('gender',2),
        snap_datetime = json_user.get('datetime'),
        color_image = dict(
            path = path,
            height = json_snap.get('height',0),
            width = json_snap.get('width',0),
        ),
    ))




def run_parser(parserName, data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='topic_results',exchange_type='topic')
    if parserName=='pose':
        poseJ = parse_pose(data)
        channel.basic_publish(exchange='topic_results',
                              routing_key='parser_results',
                              body=json.dumps(poseJ))
        return poseJ
    if parserName=='feelings':
        poseF = parse_feelings(data)
        channel.basic_publish(exchange='topic_results',
                              routing_key='parser_results',
                              body=json.dumps(poseF))
        return parse_feelings(data)
    if parserName=='color_image':
        poseC = parse_color_image(data)
        channel.basic_publish(exchange='topic_results',
                              routing_key='parser_results',
                              body=json.dumps(poseC))
        return parse_color_image(data)
    if parserName=='depth_image':
        poseD = parse_depth_image(data)
        channel.basic_publish(exchange='topic_results,
                              routing_key='parser_results',
                              body=json.dumps(poseD))
        return parse_depth_image(data)
