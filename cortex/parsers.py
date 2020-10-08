import click
import json
import pika
from pathlib import Path
from PIL import Image
#from PIL import Image as PIL
import numpy as np
import matplotlib.pyplot as plt
import seaborn
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
    print("start parse_color_image")
    json_user = (json.loads(snapshot))
    json_snap = (json.loads(snapshot))['colorImage']
    if not json_snap:
        return
    path = snapPath(json_user, 'color_image.jpg')
    mypath = (json.loads(snapshot))['colorPath']
    print(f' COLOR PATH = {mypath}')
    #color_path = path(mypath)
    with open(mypath, 'rb') as con1:
        img_bytes = con1.read()
    size = json_snap.get('width',0), json_snap.get('height',0)
    img1 = Image.frombytes('RGB', size,img_bytes)
    img1.save(path)
    print(f'color image path = {path}')
    print(f'color image size = {size}')
    print("color image saved!")
    return json.dumps(dict(
        user_id = json_user['userId'],
        user_name = json_user['username'],
        user_bday = json_user['birthday'],
        user_gender = json_user.get('gender',2),
        snap_datetime = json_user.get('datetime'),
        color_image = dict(
            path = path[path.find('/static'):],
            height = json_snap.get('height',0),
            width = json_snap.get('width',0),
        ),
    ))

def parse_depth_image(snapshot):
    json_user = (json.loads(snapshot))
    json_snap = (json.loads(snapshot))['depthImage']
    if not json_snap:
        return
    path = snapPath(json_user,'depth_image.jpg')
    size = json_snap.get('height',0), json_snap.get('width',0)
    #image = PIL.new('RGB', size)
    #data = json_snap.get('data',0)
    a = type(json_snap.get('data',0))
    #print(f'DATA TYPE IS {a}')
    #print(f'SIZE TYPE IS {type(size)}')
    data = np.array(list(json_snap.get('data',0))).reshape([json_snap.get('height',0), json_snap.get('width',0)])
    plt.imshow(data, cmap='hot', interpolation='nearest')
    plt.savefig(path)
    #plt.show()
    #plt.figure()
    #ax = seaborn.heatmap(data)
    #ax.get_figure().savefig(path)
    #print(data[:100])
    #image.putdata(data)
    #image.show()
    #image.save(path)
    return json.dumps(dict(
        user_id = json_user['userId'],
        user_name = json_user['username'],
        user_bday = json_user['birthday'],
        user_gender = json_user.get('gender',2),
        snap_datetime = json_user.get('datetime'),
        depth_image = dict(
            path = path[path.find('/static'):],
            height = json_snap.get('height',0),
            width = json_snap.get('width',0),
        ),
    ))



def snapPath(json_user, fileType):
    print("in snapPath")
    datet = json_user.get('datetime')
    curDir = Path.cwd() / 'cortex'
    guiDir = curDir / 'gui' / 'static'
    userDir = guiDir / json_user['userId'] / datet
    print(f'**********************userDir IS {userDir}**********************')
    if not userDir.exists():
        userDir.mkdir(parents=True, exist_ok=True)

    # p = Path('snapshots_data') / json_user['userId'] / datet
    # if not p.exists():
    #     p.mkdir(parents=True, exist_ok=True)
        # fn = p / f'{timestamp:%Y-%m-%d_%H-%M-%S}'
    fn = userDir / fileType
    return str(fn.absolute())
        # with open(fn, 'a') as out:
        #         if (out.tell() != 0):
        #             thought = '\n' + thought
        #         out.write(thought)



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
        print("before ")
        # print(poseC)
        channel.basic_publish(exchange='topic_results',
                              routing_key='parser_results',
                              body=json.dumps(poseC))
        print("after ")
        # print(poseC)
        return parse_color_image(data)
    if parserName=='depth_image':
        poseD = parse_depth_image(data)
        channel.basic_publish(exchange='topic_results',
                              routing_key='parser_results',
                              body=json.dumps(poseD))
        return parse_depth_image(data)
