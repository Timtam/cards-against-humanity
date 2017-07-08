import argparse

class ArgumentParser(object):
  def __init__(self):
    self.parser=argparse.ArgumentParser()
    self.parser.add_argument("-p","--port",help="port to start server on",type=int, default=11337)
  def execute(self):
    args=self.parser.parse_args()

    self.port = args.port
