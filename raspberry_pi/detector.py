import cv2
import numpy
import zipfile
from tflite_runtime.interpreter import Interpreter
from tflite_runtime.interpreter import load_delegate

class ModelException(Exception):
    """There was an error with TFLite model."""

class Detection:

    def __init__(self):
        self._top = 0
        self._right = 0
        self._bottom = 0
        self._left = 0
        self.score = 0
        self.label = ''
        self.class_id = 0

    def set_bounding_box(self, top, right, bottom, left):
        self._top = top
        self._right = right
        self._bottom = bottom
        self._left = left

    def get_start_point(self):
        return self._left, self._top,
        
    def get_end_point(self):
        return self._right, self._bottom

class ObjectDetector:
    
    _MEAN = 127.5
    _STD = 127.5

    def __init__(self, num_threads, threshold):
        self._threshold = threshold
        self._num_threads = num_threads
        self._interpreter = None
        self._label_list = []
        self._output_indices = {}
        self._input_size = ()
        self._is_quantized = True


    def load_model(self, model_path):
        self._load_label_file(model_path)
        self._create_interpreter(model_path)
        self._map_output_indices(self._interpreter.get_output_details())
        self._init_start_params(self._interpreter.get_input_details()[0])

    def _init_start_params(self, input_details):
        self._input_size = input_details['shape'][2], input_details['shape'][1]
        self._is_quantized = input_details['dtype'] == numpy.uint8

    def _create_interpreter(self, model_path):
        self._interpreter = Interpreter(model_path, num_threads=self._num_threads)
        self._interpreter.allocate_tensors()

    def _map_output_indices(self, output_details):
        sorted_indices = sorted([out['index'] for out in output_details])
        self._output_indices = {
            'location': sorted_indices[0],
            'category': sorted_indices[1],
            'score': sorted_indices[2],
            'detections': sorted_indices[3],
        }

    def _load_label_file(self, model_path):
        try:
            with zipfile.ZipFile(model_path) as loaded_model:
                if not loaded_model.namelist():
                    raise ModelException('Label not found!')

                filename = loaded_model.namelist()[0]
                with loaded_model.open(filename) as label_file:
                    label_list= label_file.read().splitlines()
                    self._label_list = [label.decode('ascii') for label in label_list]
                    print(self._label_list)
        except zipfile.BadZipFile:
            raise ModelException('Unknown type of TFLite model: metadata was not found.')

    def detect(self, frame):

        height, width, _ = frame.shape

        tensor_index = self._interpreter.get_input_details()[0]['index']
        self._interpreter.set_tensor(tensor_index, self._get_tensor_from_frame(frame))
        self._interpreter.invoke()

        return self._process_final_frame(width, height)

    def _process_final_frame(self, width, height):
        return sorted(self._get_all_detections(width, height), key=lambda detection: detection.score, reverse=True)
    
    def _get_all_detections(self, frame_width, frame_height):
        detections = []

        boxes = self._get_output_tensor('location')
        classes = self._get_output_tensor('category')
        scores = self._get_output_tensor('score')
        detections_num = int(self._get_output_tensor('detections'))
        
        for det_index in range(detections_num):
            if scores[det_index] >= self._threshold:
                class_id = int(classes[det_index])
                detections.append(self._create_detection(frame_width, frame_height, boxes[det_index], scores[det_index], class_id))
        
        return detections

    def _create_detection(self, frame_width, frame_height, coordinates, score, class_id):
        y_min, x_min, y_max, x_max = coordinates
        det = Detection()
        det.set_bounding_box(int(y_min * frame_height), int(x_min * frame_width), int(y_max * frame_height), int(x_max * frame_width))
        det.score = score

        det.label = self._label_list[class_id]
        det.class_id = class_id

        return det

    def _get_output_tensor(self, name):
        return numpy.squeeze(self._interpreter.get_tensor(self._output_indices[name]))

    def _get_tensor_from_frame(self, frame):

        tensor = cv2.resize(frame, self._input_size)
        if not self._is_quantized:
            tensor = (numpy.float(tensor) - self._MEAN) / self._STD

        return numpy.expand_dims(tensor, 0)

def draw_detections(frame, detections, text_color=(0, 0, 255)):

    MARGIN = 10
    ROW_SIZE = 10
    FONT_SIZE = 1
    FONT_THICK = 1

    for detection in detections:
        cv2.rectangle(frame, detection.get_start_point(), detection.get_end_point(), text_color)
        
        description = f'{detection.label} ({str(round(detection.score, 2))})'
        left, top = detection.get_start_point()
        text_location = (MARGIN + left, MARGIN + ROW_SIZE + top)
        cv2.putText(frame, description, text_location, cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, text_color, FONT_THICK)

    return frame
