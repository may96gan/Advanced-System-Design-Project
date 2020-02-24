import os
import sys
import traceback

import click

import cortex


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


@click.group()
@click.version_option(cortex.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback


@main.group()
@click.pass_context
def client(context):
    context.obj['client'] = cortex.client


@client.command('upload')
@click.argument('host', type=str)
@click.argument('port', type=int)
@click.argument('path', type=str)
@click.pass_obj
def client_upload(obj, host, port, path):
    client = obj['client']
    log(client.upload_sample(host, port, path))



@main.group()
@click.pass_context
def server(context):
    context.obj['server'] = cortex.server


@server.command('run')
@click.argument('host', type=str)
@click.argument('port', type=int)
@click.argument('publish', type=str)
@click.pass_obj
def server_run(obj, host, port, publish):
    server = obj['server']
    log(server.run_server(host, port,print))




if __name__ == '__main__':
    try:
        main(prog_name='asd', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
