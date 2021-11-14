
from flask import Blueprint, request

surv = Blueprint('surv', __name__)

@surv.route('/detected', methods=['POST'])
def detected():
    img = request.files['file']
    return "siema"
    
