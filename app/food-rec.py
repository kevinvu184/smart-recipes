from clarifai.rest import ClarifaiApp
import os

app = ClarifaiApp(api_key="14e719029ce04f1ea05d1c6d01d05d56")

def getPrediction():
    model = app.models.get('food-items-v1.0')
    response = model.predict_by_bytes('/home/user/image.jpeg')