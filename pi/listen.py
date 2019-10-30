
from playAudio import playOne, playMultiple
from makeAudioFiles import getAudioFile
import speech_recognition as sr
import subprocess

def captureSpeech():
    #MIC_NAME = "Microsoft® LifeCam HD-3000: USB Audio (hw:1,0)"
    MIC_NAME = "Built-in Microphone"
    keyword = "hey pie"
    # Set the device ID of the mic that we specifically want to use to avoid ambiguity
    for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
        if(microphone_name == MIC_NAME):
            device_id = i
            break

    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone(device_index = device_id) as source:
        # clear console of errors
        #subprocess.run("clear")

        # wait for a second to let the recognizer adjust the
        # energy threshold based on the surrounding noise level
        r.adjust_for_ambient_noise(source)

        print("Say something!")
        try:
            audio = r.listen(source)
        except sr.WaitTimeoutError:
            print("Listening timed out whilst waiting for phrase to start")
            quit()

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        speech = r.recognize_google(audio)
        print(speech)
        return speech
      
        #print("Google Speech Recognition thinks you said '{}'".format(r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")))
       
        # print("Google Speech Recognition thinks you said '{}'".format(r.recognize_google(audio)))
        # return format(r.recognize_google(audio))
        # #getAudioFile(speech)

        #os.system("mpg321 ./output.mp3")

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


