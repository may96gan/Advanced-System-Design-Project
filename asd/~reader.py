class Reader:
    def __init__(self, path):
        self.path = path
    def read(self):
        self._fp = open(self.path, 'rb')
	while not self._eof():
	    yield self._next_chunk()
    def _eof(self):
        
