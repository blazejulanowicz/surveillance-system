import cv2 as cv
import time
from detector import ObjectDetector, draw_detections
from utils import Counter
class CameraException(Exception):
    """Something went wrong with camera."""

class FrameHandler:

    @staticmethod
    def save_frame(frame, path='tmp.jpg'):
        cv.imwrite(path, frame)

    def __init__(self, video_capture: cv.VideoCapture):
        self._vc = video_capture
        self._detector = None

    def _get_next(self):
        retval, frame = self._vc.read()
        if not retval:
            raise CameraException()
        return frame

    def _is_next(self):
        return self._vc.isOpened()

    def record_raw(self, filename='output.avi', duration=30):

        fourcc = cv.VideoWriter_fourcc(*'XVID')
        out = cv.VideoWriter('output.avi',fourcc, 20.0, (800,600))

        start_time = time.time()
        while(int(time.time() - start_time) < duration and self._is_next()):
            out.write(self._get_next())

    def preview(self, model_path, num_threads, threshold, show_fps=False):
        self._detector = ObjectDetector(num_threads, threshold)
        self._detector.load_model(model_path)
        counter, fps = 0, 0
        start_time = time.time()
        while self._is_next():
            frame = self._get_next()
            counter += 1
            new_frame = draw_detections(*self._run_detection(frame))
            if show_fps:
                if counter % 10 == 0:
                    end_time = time.time()
                    fps = 10 / (end_time - start_time)
                    start_time = time.time()
                new_frame = self._add_fps(new_frame, fps)
            if cv.waitKey(1) == 27:
                break
            cv.imshow('object_detector', new_frame)
        cv.destroyAllWindows()

    def alert(self, model_path, num_threads, threshold):
        self._detector = ObjectDetector(num_threads, threshold)
        self._detector.load_model(model_path)
        counter = Counter()
        fps_counter, fps = 0, 0
        start_time = time.time()
        while self._is_next():
            frame = self._get_next()
            frame, detections = self._run_detection(frame)
            is_person_detected = False
            for detection in detections:
                if detection.label == 'person' and detection.score > threshold:
                    counter.detected()
                    is_person_detected = True
                    if counter.is_correct():
                        print('Person detected!!!')
                        return draw_detections(frame, detections)
            if not is_person_detected:
                counter.empty()
            fps_counter += 1
            if fps_counter % 20 == 0:
                    end_time = time.time()
                    fps = 20 / (end_time - start_time)
                    start_time = time.time()
                    print(fps)

            
    def _add_fps(self, frame, fps):
        row_size = 20  # pixels
        left_margin = 24  # pixels
        text_color = (0, 0, 255)  # red
        font_size = 1
        font_thickness = 1

        fps_text = 'FPS = {:.1f}'.format(fps)
        text_location = (left_margin, row_size)
        cv.putText(frame, fps_text, text_location, cv.FONT_HERSHEY_PLAIN, font_size, text_color, font_thickness)
        return frame

    def _run_detection(self, frame):
        frame = cv.flip(frame, -1)
        detections = self._detector.detect(frame)
        return frame, detections


