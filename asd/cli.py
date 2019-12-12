#!/usr/bin/python
import functools
from inspect import getfullargspec
import sys


class CommandLineInterface:
    def __init__(self):
        self.func_and_args = {}

    def command(self, f):
        f_arguments = getfullargspec(f)
        self.func_and_args[f.__name__] = [f, f_arguments]
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper

    def main(self):
        if len(sys.argv) < 2:
            print(f'USAGE: python {sys.argv[0]} <command> [<key>=<value>]*')
            exit(1)
        try:
            f_name = sys.argv[1]
            f, all_args = self.func_and_args[f_name]
        except Exception:
            print(f'USAGE: python {sys.argv[0]} <command> [<key>=<value>]*')
            exit(1)
        names_and_values = [kw.split("=") for kw in sys.argv[2:]]
        if any(len(nv) != 2 for nv in names_and_values):
            print(f'USAGE: python {sys.argv[0]} <command> [<key>=<value>]*')
            exit(1)
        nv = {kw.split("=")[0]: kw.split("=")[1] for kw in sys.argv[2:]}
        for n in nv:
            if n not in all_args[0] and n not in all_args[4]:
                print(f'USAGE: python {sys.argv[0]} \
                        <command> [<key>=<value>]*')
                exit(1)
        if f_name != 'upload':
            return f(**nv)
        try:
            return f(**nv)
        finally:
            print('done')
