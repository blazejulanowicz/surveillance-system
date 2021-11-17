import datetime
import json
import os

from flask import Blueprint, current_app, request, send_from_directory
from flask.wrappers import Response

from utils.database import DatabaseHandler


api = Blueprint('api', __name__)

@api.route('/set_alarm_time', methods=['POST'])
def set_alarm_time():
    start_time = request.args['start_time'].split(':')
    end_time = request.args['end_time'].split(':')
    current_app.config['ALARM_TIME'] = (datetime.time(int(start_time[0]), int(start_time[1])), datetime.time(int(end_time[0]), int(end_time[1])))
    return Response(response='time set', status=200)


@api.route('/get_alarm_info', methods=['GET'])
def get_alarm_time():
    alarm_time = {
        'start_time': current_app.config['ALARM_TIME'][0].strftime('%H:%M'),
        'end_time': current_app.config['ALARM_TIME'][1].strftime('%H:%M'),
        'status': 'armed' if current_app.config['ALARM_ARMED'] else 'disarmed'
    }
    return Response(response=json.dumps(alarm_time), status=200)

@api.route('/set_alarm_info', methods=['POST'])
def set_alarm_info():
    new_info = request.get_json()
    current_app.config['ALARM_ARMED'] = new_info['status'] == 'armed'
    start_time = new_info['start_time'].split(':')
    end_time = new_info['end_time'].split(':')
    current_app.config['ALARM_TIME'] = (datetime.time(int(start_time[0]), int(start_time[1])), datetime.time(int(end_time[0]), int(end_time[1])))
    return Response(status=200)

@api.route('/set_alarm_status', methods=['POST'])
def set_alarm_status():
    new_status = request.args['status']
    current_app.config['ALARM_ARMED'] = int(new_status) == 1
    return Response(response='armed' if current_app.config['ALARM_ARMED'] else 'disarmed', status=200)
    
@api.route('/get_video_data', methods=['GET'])
def get_video_data():
    db_path = os.path.join(current_app.root_path, current_app.config['DATABASE_PATH'])
    tmp = DatabaseHandler(db_path).get_videos()
    video_data = []
    for video in tmp:
        video_data.append({'creation_date': video[0], 'detection_id': video[1]})
    return Response(response=json.dumps(video_data))

@api.route('/get_thumbnail/<detection_id>', methods=['GET'])
def get_thumbnail(detection_id):
    db_path = os.path.join(current_app.root_path, current_app.config['DATABASE_PATH'])
    return send_from_directory(db_path, f'{detection_id}.jpg')

@api.route('/download_video/<detection_id>', methods=['GET'])
def download_video(detection_id):
    db_path = os.path.join(current_app.root_path, current_app.config['DATABASE_PATH'])
    return send_from_directory(db_path, f'{detection_id}.mp4', as_attachment=True)

