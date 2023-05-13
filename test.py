from detection.object_detection import game_detection
from PIL import Image

file = open("2023-04-23 (1).png", "rb")
image = Image.open(file)

results = game_detection(image)
print(results)