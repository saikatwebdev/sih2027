
from collections import deque


class TemporalBuffer:
    def __init__(self, max_size=10):
        self.buffer = deque(
            maxlen = max_size
        )
    
    def add(self, frame):
        self.buffer.append(frame)

    def latest(self):
        if not self.buffer:
            return None
        
        return self.buffer[-1]
    
    def previous(self):
        if len(self.buffer) < 2:
            return None
        return self.buffer[-2]
    
    def get_all(self):
        return list(self.buffer)

    def size(self):
        return len(self.buffer)
    

