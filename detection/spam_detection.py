from transformers import pipeline

classifier = pipeline("text-classification", model="khanhthuan1995/autotrain-sms-spam-vietnamese-51799122495")


def spam_detection(text):
    return classifier(text)[0]