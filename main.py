from fastapi import FastAPI
from detection import game_detection, get_text
from PIL import Image
from fastapi import FastAPI, File, UploadFile


app = FastAPI()


@app.post("/detect/")
async def detection(file: UploadFile):
    im = Image.open(file.file)
    result = get_text(image=im)
    return result

@app.post("/fiber_detection/")
async def fiber_detection(file: UploadFile):
    im = Image.open(file.file)
    return game_detection(image=im)
    
