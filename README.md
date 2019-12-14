

# Advanced-System-Design-Project

An example package. See [full documentation](https://advanced-system-design-foobar.readthedocs.io/en/latest/).

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:may96gan/Advanced-System-Design-Project.git
    ...
    $ cd Advanced-System-Design-Project/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [Advanced-System-Design-Project] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:


    ```sh
    $ pytest tests/
    ...
    ```

## Usage

The `asd` packages provides the following classes:

- `Foo`

    This class encapsulates the concept of `foo`, and returns `"foo"` when run.

    In addition, it provides the `inc` method to increment integers, and the
    `add` method to sum them.

    ```pycon
    >>> from foobar import Foo
    >>> foo = Foo()
    >>> foo.run()
    'foo'
    >>> foo.inc(1)
    2
    >>> foo.add(1, 2)
    3
    ```

- `Bar`

    This class encapsulates the concept of `bar`; it's very similar to `Foo`,
    except it returns `"bar"` when run.

    ```pycon
    >>> from foobar import Bar
    >>> bar = Bar()
    >>> bar.run()
    'bar'
    ```

The `asd` package also provides a command-line interface:

```sh
$ python -m asd
foobar, version 0.1.0
```

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

The CLI provides the `client` command, with the `upload' subcommand:

```sh
$ python -m asd client upload <host:port> <user_id> <thought>

```

The CLI further provides the `server` command, with the `run` subcommand.

```sh
$ python -m asd server run <host:port> <path to data_dir>
```


