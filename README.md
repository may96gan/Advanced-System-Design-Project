

# Advanced-System-Design-Project

An example package. See [full documentation](https://advanced-system-design-foobar.readthedocs.io/en/latest/).

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone https://github.com/may96gan/cortex
    ...
    $ cd cortex/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [cortex] $ # you're good to go!
    ```
 
3. Run dockers:
    ```sh
    $ docker run -d -p 5672:5672 rabbitmq
    ...
    $ docker run -d -p 27017:27017 mongo 

## Usage

First, run the following commands:
```pycon
import json, pika
from cortex.parsers import run_parser
from cortex.saver import Saver
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='snapshots', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='snapshots',queue=queue_name)#channel.queue_declare('current_snapshots')

def callback(channel,method,properties,body):
    print("start snap")
    saver = Saver('mongodb://localhost:27017/')
    f = run_parser('feelings',body)
    if f:
        saver.save('feelings',f)
    p=run_parser('pose',body)
    if p:
        saver.save('pose',p)
    print("done snap")


channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)

channel.start_consuming()
```

The `cortex` packages provides the following packages:

- `server`

    The server listen on host:port and pass received messages to message queue.
    (Run server at another shell).

    ```pycon
    >>> from cortex.server import run_server
    >>> run_server(host='127.0.0.1', port=8000, publish=print_message)
    ```
 
- `client`

    This package provides the upload_sample function, 
    which accepts host, port and a path,
    reads the sample in path and uploads it to host:port.
    (Run client at another shell).

    ```pycon
    >>> from cortex.client import upload_sample
    >>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
    ```
    
 - `parsers`

    This package provides the run_parser function, 
    which accepts parser name and a raw data - as consumed from the message queue,
    parse it, returns the result and publishes it to a dedicated topic.
    Available parsers: 
    Pose: Collects the translation and the rotation of the user's head at a given timestamp, and publishes the result to a dedicated               topic.
    Feelings: Collects the feelings the user was experiencing at any timestamp, and publishes the result to a dedicated topic.

    ```pycon
    >>> from cortex.parsers import run_parser
    >>> data = <body of message queue's callback>
    >>> result = run_parser(<parser_name>, data)
    ```
    
 - `saver`
 
    This package connects to a database, accepts a topic name and some data, as consumed from the message queue, and saves it to the         database.
    
    ```pycon
    >>> from cortex.saver import Saver
    >>> saver = Saver(database_url)
    >>> data = …
    >>> saver.save('pose', data)
    ```
- `api`

    listen on host:port and serve data from database_url.
    
    ```pycon
    >>> from cortex.api import run_api_server
    >>> run_api_server(
    ...     host = '127.0.0.1',
    ...     port = 5000,
    ...     database_url = 'mongodb://localhost:27017/',
    ... )
    ```    
    
  Api is consumed and reflected by CLI:
  ```sh
  $ python -m cortex.cli get-users
  $ python -m cortex.cli get-user <user_id>
  $ python -m cortex.cli get-snapshots <user_id>
  $ python -m cortex.cli get-snapshot <user_id> <snapshot_id>
  $ python -m cortex.cli get-result <user_id> <snapshot_id> <parser's name>
  ```

The `cortex` package also provides a command-line interface:

The CLI provides the following subcommands:

```sh
$ python -m cortex.client upload-sample \
      -h/--host (default='127.0.0.1')             \
      -p/--port (default=8000)                    \
      <path_to_sample_file>

```


```sh
$ python -m cortex.server run-server \
      -h/--host (default='127.0.0.1')          \
      -p/--port (default=8000)                 \
      '<URL to a message queue> (default=rabbitmq://127.0.0.1:5672/')

```

```sh
$ python -m cortex.api run-server
```

The `cortex` package also provides a graphical user interface:
(You can also run this command with no arguments. Those are the default arguments.)

```sh
>>> from cortex.gui import run_server
>>> run_server(
...     host = '127.0.0.1',
...     port = 8080,
...     database_url = 'mongodb://localhost:27017/',
... )
```



