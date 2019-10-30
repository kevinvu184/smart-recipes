# SmartRecipes

RMIT - CC Semester 2 2019

© Kevin Vu 2019. Disclaimer: This repo is an asset of Kevin Vu and is being developed as part of a School of Science Cloud Computing course at RMIT University in Melbourne, Australia. Any plagiarism act will be reported.

- Link: https://lunardo-cinemas.appspot.com/

## Team member
- Kevin Vu
- Avital Miskela

## Project Brief
Smart Recipes is a place to store your own recipes in the cloud. It offers advanced capabilities to streamline the process of adding your recipes. With an intelligent “Smart Add” you are able to input ingredients with a single image. To streamline the process of cooking, a user can “play” a recipe using a raspberry pi to create an interactive cooking experience. Log in as your user, store your own recipes safely in the cloud, and reference them on any device. 

## Stack
- Front end: **HTML/CSS/JS - Bootstrap**
- Back end: **Python Flask**
- DB: **Google Cloud SQL** + **SQLAlchemy**
- Deploy Platform: **GAE (Google App Engine)**
- API: **Clarifai API (Food regconition)**, **Google Vision API (Object Detection)**
- Other Cloud Services:
  - **Dialogflow** + **Google Action**: Chatbot and Google Home system extension
  - **Firebase**: Authentication
  - **Cloud Source Repo** + **Cloud Build**: Deploy pipeline
  - **Cloud Storage**: Store and Retrieve Object (Images)
  - **Cloud Function**: Validate Images, Get Data for Google Action
  - **Cloud Speech to Text** + **Cloud Text to Speech** + **Rasberry Pi**: IoT device
  - **Cloud Logging**: Monitoring
  
## Model
![Model](https://user-images.githubusercontent.com/43775190/67828512-c8a40700-fb27-11e9-81ea-b921239dc3df.png)
