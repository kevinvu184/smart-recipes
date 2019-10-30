import speech_recognition as sr
import subprocess
from google.cloud import texttospeech
import os
import zipfile

class Audio:
    hasAudioFiles = False

    def createZip(self, filePath):
        recipeZip = zipfile.ZipFile(filePath, 'w')
        print("in here")
        for folder, subfolders, files in os.walk(filePath):
            for file in files:
                print(file)
                if file.endswith('.mp3'):
                    recipeZip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), filePath), compress_type = zipfile.ZIP_DEFLATED)
    
        recipeZip.close()
        hasAudioFiles = True
        return True

    def createAudioFiles(self, text, name):
        # Instantiates a client
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.types.SynthesisInput(text=text)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")

        voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-AU',
            name='en-AU-Wavenet-D',
            #ssml_gender=texttospeech.enums.SsmlVoiceGender.FEM
            )

        # Select the type of audio file you want returned
        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(synthesis_input, voice, audio_config)

        # The response's audio_content is binary.
        with open(name +'.mp3', 'wb') as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to file ' + name)

    
