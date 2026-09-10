# pyrefly: ignore [missing-import]
from collections import deque, Counter

class ActivitySmoother:
    def __init__(self, window_size=5, min_occurences=3):
        self.history = deque(maxlen=window_size)
        self.min_occurences = min_occurences

    def update(self, activity):
        self.history.append(activity)

        counts = Counter(self.history)

        activity, count = counts.most_common(1)[0]

        if count >= self.min_occurences:
            return activity
        
        return None
        