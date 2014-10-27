#!/usr/bin/env python

from gevent import monkey
from gevent.server import _tcp_listener
monkey.patch_all()

from gevent_thrift import server, monkey as tmonkey
tmonkey.patch_thrift()

from multiprocessing import Process, cpu_count

import sys
sys.path.append('gen-py')

from juwai import PropertyService
from juwai.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from schema import Base, Property

import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(msg)s")

class PropertyServiceHandler():
	def __init__(self):
		self.log = logging.getLogger(__file__)
		self.engine = create_engine('mysql+mysqlconnector://localhost/db')
		Base.metadata.bind = self.engine

	def getProperty(self, id):
		tProp = TProperty()

		DBSession = sessionmaker()
		DBSession.bind = self.engine
		session = DBSession()

		try:
			prop = session.query(Property).filter(Property.id == id).one()
			for (key, val) in vars(tProp).iteritems():
				setattr(tProp, key, getattr(prop, key))
			session.commit()
			#self.engine.execute('select sleep(1)')
		except NoResultFound as e:
			session.rollback()
			print e
			raise NoSuchObject('No property with id ' + str(id))
		except Exception as e:
			session.rollback()
			print e
			raise SelectFailed('Could not select property')
		finally:
			session.close()

		return tProp

	def addProperty(self, tProp):
		try:
			prop = Property()

			for (key, val) in vars(tProp).iteritems():
				setattr(prop, key, val)

			self.session.add(prop)
			self.session.commit()
		except:
			raise InsertFailed('Could not save property')

def serve_forever(listener):
	print 'starting server'
	handler = PropertyServiceHandler()
	processor = PropertyService.Processor(handler)
	tserver = server.ThriftServer(logging.getLogger(__file__), listener, processor)
	tserver.serve_forever()

def main():
	print 'Starting Python server...'
	listener = _tcp_listener(('',9090))

	number_of_processes = cpu_count() - 1
	print 'Starting %s processes' % number_of_processes
	for i in range(number_of_processes):
		Process(target=serve_forever, args=(listener,)).start()

	serve_forever(listener)

if __name__ == "__main__":
	main()
