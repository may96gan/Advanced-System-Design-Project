

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

The `cortex` packages provides the following packages:

- `server`

    The server listen on host:port and pass received messages to message queue.

    ```pycon
    >>> from cortex.server import run_server
    >>> run_server(host='127.0.0.1', port=8000, publish=print_message)
    ```
 
- `client`

    This package provides the upload_sample function, 
    which accepts host, port and a path,
    reads the sample in path and uploads it to host:port.

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

    listen on host:port and serve data from database_url
    
    ```pycon
    >>> from cortex.api import run_api_server
    >>> run_api_server(
    ...     host = '127.0.0.1',
    ...     port = 5000,
    ...     database_url = 'postgresql://127.0.0.1:5432',
    ... )
    ```
listen on host:port and serve data from database_url



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


