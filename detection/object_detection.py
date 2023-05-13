from ultralytics import YOLO


model = YOLO('yolov8n.pt')
model = YOLO('model/albion/fiber.pt')

# results = model.predict('screen 1920 0 1920 1080', stream=True, vid_stride=True)

'''
stream:
'rtsp://example.com/media.mp4'
'''

def game_detection(image):
    results = model(image)
    return results

