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
@click.argument('address', type=str)
@click.argument('user', type=int)
@click.argument('thought', type=str)
@click.pass_obj
def client_upload(obj, address, user, thought):
    client = obj['client']
    log(client.upload_thought(address, user, thought))



@main.group()
@click.pass_context
def server(context):
    context.obj['server'] = cortex.server


@server.command('run')
@click.argument('address', type=str)
@click.argument('data_dir', type=str)
@click.pass_obj
def server_run(obj, address, data_dir):
    server = obj['server']
    log(server.run_server(address, data_dir))




if __name__ == '__main__':
    try:
        main(prog_name='asd', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
