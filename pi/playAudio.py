import pygame
import os
pygame.mixer.init()

def playOne(filename):
    #audio file for saying hey
    # play sounds using this instead https://raspberrypi.stackexchange.com/questions/7088/playing-audio-files-with-python 
    
    pygame.mixer.init()
    pygame.mixer.music.load(filename + ".mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

def playMultiple(filedir):
    #audio file for saying hey
    # play sounds using this instead https://raspberrypi.stackexchange.com/questions/7088/playing-audio-files-with-python 
    files = []
    file_index = 0
    for filename in os.listdir(filedir):
        if filename.endswith(".mp3"):
            files.append(filename)

    pygame.mixer.init()

    for audfile in files:
        pygame.mixer.music.load(filedir + audfile)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

  
    