from listen import captureSpeech 
from playAudio import playOne, playMultiple
from makeAudioFiles import getAudioFile
import requests
import zipfile 
import io

#add function to read put amount of any ingredients later 
def main():
#     #listen on socket audio files
#     print("Waiting to recive audio files.")
    #makeTestFiles()
#     loadAudioFiles()
#     #play audio file called ingredients 
#     playOne("./audio/intro")
#    # playMultiple("./audio/ing/")
#     #Method set to 0 
    step = 0
    # need to set max steps sowmhere so it knows when to end the loop
    #keyword = "hey pie"
    
    flag = False
    keyword = "hey pie"
    recipeNo = 0

    while flag == False:
        ## for PI, light up the LED's to know when to speak
        capture = captureSpeech()
        try:
            if keyword in capture:
                print("picked up hey pi")

            if "start cooking" in capture:
                test = capture.split("start cooking recipe ")[1]
                try:
                    print(test)
                    playOne("./audio/download")
                    recipeNo = test
                    requestAudioFiles(test)
                    playOne("./audio/start")
                    playMultiple("./audio/"+ recipeNo + "/ing")
                    playOne("./audio/"+ recipeNo + "/method/1")
                    #say the frirst step here

                except AssertionError as error:
                    print(error)
                    playOne('./audio/error')

                # playOne('./audio/hi')
                # step += 1
                # playOne('./audio/method/'+str(step))

            elif "next step" in capture or "nextstep" in capture:
                print("Step: " ,step)
                if step <= maxStep:
                    step += 1
                    playOne('./audio/' + recipeNo+ 'method/'+str(step))
                else:
                    playOne("./audio/bye")
                    flag = True

            elif "repeat" in capture:
                playOne('./audio/' + recipeNo+ 'method/'+str(step))

            elif "how much" in capture:
                print(capture)
                test = capture.split("how much ")[1]
                print("Test", test)
                try:
                    playOne('./audio/'+ recipeNo +'ing/'+test)
                except:
                    playOne('./audio/error')

            elif "goodbye" in capture:
                playOne("./audio/bye")

        except AssertionError as error:
            print(error)
            playOne('./audio/error')

        
            
            
   


    #wait for user to speak "Hey Pi"
    #if "Hey Pi", play the next instruction audio file
    #repeat until end of audio files 
    #if end of recipe (and audio files) say goodbye to the user. 

def makeTestFiles():
    # ings = [
    #     {'ingName': "self raising flour", 'amount': "1 1/2 cups "},
    #     {'ingName': "baking powder", 'amount': "1 teaspoon" },
    #     {'ingName': "unsalted butter", 'amount': "115 grams"},
    #     {'ingName': "sultanas", 'amount': "115 grams"},
    #     {'ingName': "mixed peel", 'amount': "50 grams" },
    #     {'ingName': "caster sugar", 'amount': "75 grams" },
    #     {'ingName': "orange", 'amount': "Grated zest of 1"},
    #     {'ingName': "eggs", 'amount': "2" }
    # ]
    # method = [
    #     {"step":"Sift flour and baking powder into a large bowl", "no":"1"},
    #     {"step":"Rub in the butter until it resembles breadcrumbs", "no":"2"},
    #     {"step":"Stir in fruit, sugar and zest", "no":"3"},
    #     {"step":"Add eggs, stirring together, until you have a stiff dough.", "no":"4"},
    #     {"step":"Place walnut-sized mounds of the mixture on a greased baking tray, leaving space for spreading between each one.", "no":"5"},
    #     {"step":"Bake for 15-20 minutes until golden brown. Cool on a wire rack.", "no":"6"}
    # ]
    
    # for val in ings:
    #     print(val)
    #     getAudioFile(val['amount'] + val['ingName'], "./audio/ing/" + val['ingName'])

    # for val in method:
    #     getAudioFile(val['step'], "./audio/method/" + val['no'])

    # recipeName = "Rock Cakes"
    # intro = "Lets make " + recipeName +". I'll start with the ingredients. After that, say 'Hey Pi', 'Lets start cooking.'"
    # getAudioFile(intro, "./audio/intro")
    download = "okay, let me download the recipe."
    start = "okay, lets start cooking. Here are the ingredients. "
    getAudioFile(download, './audio/download')
    getAudioFile(start, './audio/start')
    
def loadAudioFiles():
    getAudioFile("Hey! here is the first step.", "./audio/hi")
    getAudioFile("Sorry, I didnt undertstand, please try again", "./audio/error")

def requestAudioFiles(recipeNo):
    print("in da function")
    url = "http://127.0.0.1:5000/play-recipe/" + recipeNo
    print(url)
    try:
        r = requests.get(url)
        print(r)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall('./audio/'+ recipeNo)
        print("done")
    except AssertionError as error:
        print(error)
   


if __name__ == "__main__":
    main()