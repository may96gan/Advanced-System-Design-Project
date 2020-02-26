#import os
#import sys
#import traceback

#import click

#import cortex


#class Log:

 #   def __init__(self):
  #      self.quiet = False
   #     self.traceback = False

    #def __call__(self, message):
     #   if self.quiet:
      #      return
       # if self.traceback and sys.exc_info(): # there's an active exception
        #    message += os.linesep + traceback.format_exc().strip()
        #click.echo(message)


#log = Log()





#if __name__ == '__main__':
 #   try:
  #      main(prog_name='asd', obj={})
   # except Exception as error:
    #    log(f'ERROR: {error}')
     #   sys.exit(1)
