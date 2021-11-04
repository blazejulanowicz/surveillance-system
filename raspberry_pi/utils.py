

class Counter:

    def __init__(self, detection_threshold=6, max_frames=8):
        self._last_frames = []
        self._max_frames = max_frames
        self._threshold = detection_threshold

    def _append(self, item):
        if len(self._last_frames) == self._max_frames:
            self._last_frames.pop(0)
        self._last_frames.append(item)

    def detected(self):
        self._append(True)
        print(f'Frames: {self._last_frames}')

    def empty(self):
        self._append(False)
        print(f'Frames: {self._last_frames}')
    
    def is_correct(self):
        counter = 0
        for item in self._last_frames:
            if item:
                counter += 1
        return counter >= self._threshold
