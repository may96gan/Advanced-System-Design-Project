![build status](https://travis-ci.org/dan-gittik/foobar.svg?branch=master)
![coverage](https://codecov.io/gh/dan-gittik/foobar/branch/master/graph/badge.svg)

#  Advanced-System-Design-Project

An example package. See [full documentation](https://advanced-system-design-foobar.readthedocs.io/en/latest/).

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:may96gan/Advanced-System-Design-Project.git
    ...
    $ cd  Advanced-System-Design-Project/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [ Advanced-System-Design-Project] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:


    ```sh
    $ pytest tests/
    ...
    ```

## Usage

The ` Advanced-System-Design-Project` packages provides the following classes:

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

The `foobar` package also provides a command-line interface:

```sh
$ python -m foobar
foobar, version 0.1.0
```

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

The CLI provides the `foo` command, with the `run`, `add` and `inc`
subcommands:

```sh
$ python -m foobar foo run
foo
$ python -m foobar foo inc 1
2
$ python -m foobar foo add 1 2
3
```

The CLI further provides the `bar` command, with the `run` and `error`
subcommands.

Curiously enough, `bar`'s `run` subcommand accepts the `-o` or `--output`
option to write its output to a file rather than the standard output, and the
`-u` or `--uppercase` option to do so in uppercase letters.

```sh
$ python -m foobar bar run
bar
$ python -m foobar bar run -u
BAR
$ python -m foobar bar run -o output.txt
$ cat output.txt
BAR
```

Do note that each command's options should be passed to *that* command, so for
example the `-q` and `-t` options should be passed to `foobar`, not `foo` or
`bar`.

```sh
$ python -m foobar bar run -q # this doesn't work
ERROR: no such option: -q
$ python -m foobar -q bar run # this does work
```

To showcase these options, consider `bar`'s `error` subcommand, which raises an
exception:

```sh
$ python -m foobar bar error
ERROR: something went terribly wrong :[
$ python -m foobar -q bar error # suppress output
$ python -m foobar -t bar error # show full traceback
ERROR: something went terribly wrong :[
Traceback (most recent call last):
    ...
RuntimeError: something went terrible wrong :[
```


Installation
Clone the repository and enter it:

$ git clone git@github.com:may96gan/Advanced-System-Design-Project.git
...
$ cd Advanced-System-Design-Project/

Run the installation script and activate the virtual environment:

$ ./scripts/install.sh
...
$ source .env/bin/activate
[Advanced-System-Design-Project] $ # you're good to go!
To check that everything is working as expected, run the tests:

$ pytest tests/
...
Usage
The Advanced-System-Design-Project packages provides the following classes:

Foo

This class encapsulates the concept of foo, and returns "foo" when run.

In addition, it provides the inc method to increment integers, and the add method to sum them.

>>> from foobar import Foo
>>> foo = Foo()
>>> foo.run()
'foo'
>>> foo.inc(1)
2
>>> foo.add(1, 2)
3
Bar

This class encapsulates the concept of bar; it's very similar to Foo, except it returns "bar" when run.

>>> from foobar import Bar
>>> bar = Bar()
>>> bar.run()
'bar'
The foobar package also provides a command-line interface:

$ python -m foobar
foobar, version 0.1.0
All commands accept the -q or --quiet flag to suppress output, and the -t or --traceback flag to show the full traceback when an exception is raised (by default, only the error message is printed, and the program exits with a non-zero code).

The CLI provides the foo command, with the run, add and inc subcommands:

$ python -m foobar foo run
foo
$ python -m foobar foo inc 1
2
$ python -m foobar foo add 1 2
3
The CLI further provides the bar command, with the run and error subcommands.

Curiously enough, bar's run subcommand accepts the -o or --output option to write its output to a file rather than the standard output, and the -u or --uppercase option to do so in uppercase letters.

$ python -m foobar bar run
bar
$ python -m foobar bar run -u
BAR
$ python -m foobar bar run -o output.txt
$ cat output.txt
BAR
Do note that each command's options should be passed to that command, so for example the -q and -t options should be passed to foobar, not foo or bar.

$ python -m foobar bar run -q # this doesn't work
ERROR: no such option: -q
$ python -m foobar -q bar run # this does work
To showcase these options, consider bar's error subcommand, which raises an exception:

$ python -m foobar bar error
ERROR: something went terribly wrong :[
$ python -m foobar -q bar error # suppress output
$ python -m foobar -t bar error # show full traceback
ERROR: something went terribly wrong :[
Traceback (most recent call last):
    ...
RuntimeError: something went terrible wrong :[
