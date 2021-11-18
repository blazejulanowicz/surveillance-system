import argparse
import requests
import os

from frame_handler import FrameHandler
import cv2 as cv

def get_path(filename):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)

def run(model, backend_url, width, height, num_threads, threshold, video):
    video_capture = None
    if video != '':
        video_capture = cv.VideoCapture(video)
    else:
        video_capture = cv.VideoCapture(0)
        video_capture.set(cv.CAP_PROP_FRAME_WIDTH, width)
        video_capture.set(cv.CAP_PROP_FRAME_HEIGHT, height)

    fh = FrameHandler(video_capture)

    while(True):
        alert_frame = fh.alert(get_path(model), num_threads, threshold)
        FrameHandler.save_frame(alert_frame, get_path('tmp.jpg'))
        with open(get_path('tmp.jpg'), 'rb') as img:
            response = requests.post(f'{backend_url}/surv/detected', files={'file': ('tmp.jpg', img, 'image/jpeg')})
        if response.json()['armed'] == True:
            fh.record_raw(get_path('output.mp4'))
            with open(get_path('output.mp4'), 'rb') as video:
                requests.post(f'{backend_url}/surv/send_video?detection_id={response.json()["detection_id"]}', files={'file': ('output.mp4', video, 'video/x-msvideo')})



def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--model',
        required=True)
    parser.add_argument(
        '--backend_url',
        required=True
    )
    parser.add_argument(
        '--video',
        required=False,
        default='')
    parser.add_argument(
        '--frameWidth',
        help='Width of frame to capture from camera.',
        required=False,
        type=int,
        default=800)
    parser.add_argument(
        '--frameHeight',
        help='Height of frame to capture from camera.',
        required=False,
        type=int,
        default=600)
    parser.add_argument(
        '--numThreads',
        help='Number of CPU threads to run the model.',
        required=False,
        type=int,
        default=4)
    parser.add_argument(
        '--threshold',
        required=False,
        type=float,
        default=0.6
    )
    args = parser.parse_args()

    run(args.model, args.backend_url, args.frameWidth, args.frameHeight,
        int(args.numThreads), float(args.threshold), args.video)


if __name__ == '__main__':
  main()
