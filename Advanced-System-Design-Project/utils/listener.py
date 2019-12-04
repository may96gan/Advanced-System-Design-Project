from connection import Connection
import socket
class Listener:
	def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
		self.port = port
		self.host = host
		self.server = socket.socket()
		self.backlog = backlog
		self.reuseaddr = reuseaddr
		self.client = None
		if reuseaddr:
			self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.host,self.port))
	def __repr__(self):
		return f'Listener(port={self.port!r}, host={self.host!r}, backlog={self.backlog!r}, reuseaddr={self.reuseaddr!r})'
	def start(self):
		self.server.listen(self.backlog)
	def stop(self):
		if self.client:
			self.client.close()
		self.server.close()
	def accept(self):
		self.client, client_address = self.server.accept()
		return Connection(self.client)
	def __enter__(self):
		self.start()
	def __exit__(self,exception,error,traceback):
		self.stop()
