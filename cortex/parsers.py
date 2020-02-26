import click
import json

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
    json_snap = (json.loads(snapshot))['pose']
    if not json_snap:
        return
    json_snap_t = json_snap['translation']
    json_snap_r = son_snap['rotation']
    if not json_snap_t or not json_snap_r:
        return 
    return json.dumps(dict( 
                        tx = json_snap_t.get('x',0),
                        ty = json_snap_t.get('y',0),
                        tz = json_snap_t.get('z',0),
                        rx = json_snap_r.get('x',0),
                        ry = json_snap_r('y',0),
                        rz = json_snap_r('z',0),
                        rw = json_snap_r('w',0),
    ))
#parse_pose.field = 'pose'

def parse_feelings(snapshot):
    json_snap = (json.loads(snapshot))['feelings']
    if not json_snap:
        return
    return json.dumps(dict(
        hunger = json_snap.get('hunger',0),
        thirst = json_snap.get('thirst',0),
        exhaustion = json_snap.get('exhaustion',0),
        happiness = json_snap.get('happiness',0),
    ))
#parse_feelings.field = 'feelings'


def run_parser(parserName, data):
    if parserName=='pose':
        return parse_pose(data)
    if parserName=='feelings':
        return parse_feelings(data)

