import time
import struct
from datetime import datetime


class Thought:
    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        s = f'Thought(user_id={self.user_id!r},'
        s1 = f'timestamp={self.timestamp!r},'
        s2 = f'thought={self.thought!r})'
        return s+s1+s2

    def __str__(self):
        s = f'[{self.timestamp:%Y-%m-%d %H:%M:%S}]'
        s1 = f'user {self.user_id}: {self.thought}'
        return s+s1

    def __eq__(self, other):
        return isinstance(other, Thought) and self.user_id == other.user_id \
            and self.timestamp == other.timestamp \
            and self.thought == other.thought

    def serialize(self):
        return struct.pack('LLI',
                           (int)(self.user_id),
                           (int)(time.mktime(self.timestamp.timetuple())
                                 + self.timestamp.microsecond/1E6),
                           len(self.thought)) + bytes(self.thought, 'utf-8')

    def deserialize(data):
        s = struct.Struct('LL')
        unpacked_data = s.unpack(data[:16])
        user_id = unpacked_data[0]
        timestamp = datetime.fromtimestamp(unpacked_data[1])
        thought = data[20:].decode("utf-8")
        return Thought(user_id, timestamp, thought)
