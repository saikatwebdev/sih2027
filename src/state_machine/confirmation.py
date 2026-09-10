from collections import deque

class StateConfirmation:
    def __init__(self, required_frames=3):
        self.required_frames = (required_frames)
        self.history = deque(maxlen=required_frames)

    def update(self, state):
        self.history.append(state)

        if len(self.history) < self.required_frames:
            return False
            
        return all(item == state for item in self.history)

            
