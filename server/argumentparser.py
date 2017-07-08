import argparse
import os.path
import sys

class ArgumentParser(object):
  def __init__(self):
    self.parser=argparse.ArgumentParser()
    self.parser.add_argument("-b", "--black-cards",help="the amount of black cards used per game", type=int, default=-1)
    self.parser.add_argument("-d", "--database", help="path to the database file", type=str, default="cards.db")
    self.parser.add_argument("-p","--port",help="port to start server on",type=int, default=11337)

  def execute(self):
    args=self.parser.parse_args()

    self.port = args.port

    if args.black_cards<=0:
      args.black_cards = -1
    elif args.black_cards <10 and args.black_cards >=0:
      print 'wrong amount of black cards supplied'
      print 'each game must at least run with 10 black cards'
      sys.exit()

    self.black_cards = args.black_cards

    if not os.path.exists(args.database):
      print 'cannot find %s'%(args.database)
      print 'consider creating a new card database, take one from the sample-databases folder,'
      print 'or get one from the internet.'
      print 'you can specify the path to the file with the --database argument.'
      sys.exit()

    self.database = args.database
