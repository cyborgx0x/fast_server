import os
from twilio.rest import Client
from dotenv import load_dotenv
from fastapi import FastAPI
load_dotenv()
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
import twilio.rest
from pydantic import BaseModel
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
api_key = os.environ['TWILIO_API_KEY']
api_secret = os.environ['TWILIO_API_KEY_SECRET']

app = FastAPI()
class Participant(BaseModel):
    user_identity: str
    room_name: str | None = None



@app.post("/token")
def tradie_token(participant: Participant):
    try:
        room = client.video.rooms(unique_name=participant.room_name).fetch()
    except twilio.base.exceptions.TwilioRestException:
        room = client.video.rooms.create(
            type='group',
            record_participants_on_connect=True,
            unique_name=participant.room_name,
            max_participants=3,
            # VideoCodecs="H264"
        )
    access_token = AccessToken(
            account_sid,
            api_key,
            api_secret,
            identity=participant.user_identity
        )
    video_grant = VideoGrant(room=room.sid)
    access_token.add_grant(video_grant)
    return access_token.to_jwt()