from flask import Blueprint,jsonify

login = Blueprint('login',__name__)

@login.route('/loginTest')
def loginTest():
    return jsonify(user='fz')

