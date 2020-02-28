import click
import json
import pika

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
                        tx = json_snap_t.get('x',0),
                        ty = json_snap_t.get('y',0),
                        tz = json_snap_t.get('z',0),
                        rx = json_snap_r.get('x',0),
                        ry = json_snap_r.get('y',0),
                        rz = json_snap_r.get('z',0),
                        rw = json_snap_r.get('w',0),
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
        hunger = json_snap.get('hunger',0),
        thirst = json_snap.get('thirst',0),
        exhaustion = json_snap.get('exhaustion',0),
        happiness = json_snap.get('happiness',0),
    ))
#parse_feelings.field = 'feelings'


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

