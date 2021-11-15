import datetime

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

    return Response(response='true', status=201)

@surv.route('/send_video', methods=['POST'])
def send_video():
    try:
        video = request.files['file']
    except KeyError:
        return Response(status=403)
    current_date = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
    video_name = f'{current_date}.mp4'
    video_path = f'./database_data/{video_name}'
    video.save(video_path)
    DatabaseHandler('./database_data/videos.db').push_video(video_name)
    return Response(response='true', status=201)
    
    
