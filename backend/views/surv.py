import datetime
import json

from flask import Blueprint, current_app, request
from flask.wrappers import Response

from utils.database import DatabaseHandler
from utils.mailer import MailService


surv = Blueprint('surv', __name__)

@surv.route('/detected', methods=['POST'])
def detected():
    try:
        img = request.files['file']
    except KeyError:
        return Response(status=403)
    conf = current_app.config['MAIL_SERVICE']
    mailer = MailService(conf['sender_email'], conf['sender_password'], conf['receiver_mail'])
    mailer.send_alert(img.read())

    response = {'armed': False}
    if current_app.config['ALARM_ARMED'] and (datetime.datetime.now().time() >= current_app.config['ALARM_TIME'][0] and datetime.datetime.now().time() <= current_app.config['ALARM_TIME'][1]):
        detection_id = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
        image_name = f'{detection_id}.jpg'
        image_path = f'./database_data/{image_name}'
        img.save(image_path)
        response = {'armed': True, 'detection_id': detection_id}
    return Response(response=json.dumps(response), status=201)

@surv.route('/send_video', methods=['POST'])
def send_video():
    try:
        video = request.files['file']
        detection_id = request.args['detection_id']
    except KeyError:
        return Response(status=403)
    video_name = f'{detection_id}.mp4'
    video_path = f'./database_data/{video_name}'
    video.save(video_path)
    DatabaseHandler('./database_data/videos.db').push_video(detection_id)
    return Response(response='true', status=201)
    
    
