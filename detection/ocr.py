from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from detection.distort import negative_barrel
processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-printed')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-printed')
# model.to("cuda:0")
import numpy as np
from PIL import Image
import cv2

def get_text(image):
    image = image.convert("RGB")
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text

def bypass_captcha(image):
    im_np = np.asarray(image)
    # image = image.convert("RGB")
    output = negative_barrel(im_np)
    img = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img)
    pixel_values = processor(images=im_pil, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to("cuda:0")
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text.lower()
