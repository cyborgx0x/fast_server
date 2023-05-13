from typing import Union

from fastapi import FastAPI
from detection import game_detection, get_text, spam_detection
from pydantic import BaseModel
from io import BytesIO
from PIL import Image

import os
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
import twilio.rest

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
api_key = os.environ['TWILIO_API_KEY']
api_secret = os.environ['TWILIO_API_KEY_SECRET']
from fastapi import FastAPI, File, UploadFile
app = FastAPI()
from typing import Annotated

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):

    return {"filename": file.filename}


class SMS(BaseModel):
    content: str

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
            max_participants=2,
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
    


@app.post("/detect/")
async def detection(file: UploadFile):
    im = Image.open(file.file)
    result = get_text(image=im)
    return result


@app.post("/spam_detection/")
async def detect_sms(sms:SMS):
    return spam_detection(sms.content)



@app.post("/fiber_detection/")
async def fiber_detection(file: UploadFile):
    im = Image.open(file.file)
    result = game_detection(image=im)
    return {
        "test": "done"
    }


def detection_queue():
    '''
    take request and put it to the queue
    '''
    return None

def sample_ocr():

    pass


