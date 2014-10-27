import sys, time

sys.path.append('gen-py')
from juwai import PropertyService
from juwai.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from locust import Locust, events, task, TaskSet

class ThriftClient():
	def get_property(self):
		start_time = time.time()
		socket = TSocket.TSocket('localhost', 9090)
		socket.setTimeout(10000);
		#transport = TTransport.TBufferedTransport(socket)
		transport = TTransport.TFramedTransport(socket)
		protocol = TBinaryProtocol.TBinaryProtocol(transport)
		client = PropertyService.Client(protocol)

		try:
			transport.open()
			prop = client.getProperty(326912)
			total_time = int((time.time() - start_time) * 1000)
			events.request_success.fire(request_type='thrift', name='get_property',
										response_time=total_time, response_length=0)
		except Exception as e:
			total_time = int((time.time() - start_time) * 1000)
			print e
			events.request_failure.fire(request_type='thrift', name='get_property',
										response_time=total_time, exception=e)
		transport.close()

class ThriftUser(Locust):
	min_wait = 1000
	max_Wait = 1000

	client = ThriftClient()

	class task_set(TaskSet):
		@task(1)
		def get_property(self):
			self.client.get_property()
