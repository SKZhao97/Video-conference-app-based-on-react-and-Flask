import os
from dotenv import load_dotenv
import time
from flask import Flask, render_template, request, abort
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

load_dotenv()
FLASK_APP=os.environ.get('FLASK_APP')
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/time')
def get_current_time():
	return {'time':time.time()}


@app.route('/login', methods=['POST'])
def login():
    print(request.get_json(force=True).get('identity'))
    username = request.get_json(force=True).get('identity')
    if not username:
        abort(401)

    token = AccessToken(twilio_account_sid, twilio_api_key_sid,
                        twilio_api_key_secret, identity=username)
    token.add_grant(VideoGrant(room='My Room'))
    print(token)
    return {'token': token.to_jwt().decode()}

# @app.route('/login', methods=['POST'])
# def login():
#     username = request.get_json(force=True).get('username')
#     if not username:
#         abort(401)

#     token = AccessToken(twilio_account_sid, twilio_api_key_sid,
#                         twilio_api_key_secret, identity=username)
#     token.add_grant(VideoGrant(room='My Room'))

#     return {'token': token.to_jwt().decode()}


if __name__ == '__main__':
    app.run(host='0.0.0.0')
