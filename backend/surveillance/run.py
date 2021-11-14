import argparse
import sys
import time

from frame_handler import FrameHandler
from mailer import MailService
import cv2 as cv

def run(model, width, height, num_threads, threshold, video):
    video_capture = None
    if video != '':
        video_capture = cv.VideoCapture(video)
    else:
        video_capture = cv.VideoCapture(0)
        video_capture.set(cv.CAP_PROP_FRAME_WIDTH, width)
        video_capture.set(cv.CAP_PROP_FRAME_HEIGHT, height)

    fh = FrameHandler(video_capture)
    mailer = MailService('testmailblazej@gmail.com', 'Hom3Aut0m@tion#997', 'imnotfreeman@gmail.com')

    alert_frame = fh.alert(model, num_threads, threshold)
    FrameHandler.save_frame(alert_frame)
    mailer.send_alert('tmp.jpg')



def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--model',
        required=True)
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

    run(args.model, args.frameWidth, args.frameHeight,
        int(args.numThreads), float(args.threshold), args.video)


if __name__ == '__main__':
  main()
