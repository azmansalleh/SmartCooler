#Cognative
from SpeechAndVoice import client
from SpeechAndVoice import listen
from SpeechAndVoice import voice


#import FetchDrinks Speach Understanding
from LanguageProcess import text_analysis

#pip/native python libraries
from datetime import datetime
from datetime import timedelta
from Twillio import Twillio
import dateutil.parser as parser
import math
import threading
import time
import os
import pygame
import wolframalpha
import requests
import importlib
import json
import pandas
import Speaker
import FetchDrinks
import bingSpeech
import myluis
import recordWorking as Record

sms = Twillio()

class Call():
    def __init__(self):
        self.reset()

    def reset(self):
        #self.request_history = []
        self.speakerFlag = 0
        self.threadFlag= False
        
    def playedOnce(self):
        self.speakerFlag = 1

    def retSpeakerFlag(self):
        return self.speakerFlag

    def wolfram_query(self,query):

        print("Getting answer to odd question...")
        wolfram_client = wolframalpha.Client("443H9U-THX3TLEJPY")

        res = wolfram_client.query(query)
        print(res)
        try:
            for pod in res.pods:

                if pod["@title"] == "Result":
                    return str(pod["subpod"]["img"]["@alt"]).replace("(", "").replace(")", "")
        except:
            try:
                for pod in res.pods:
                    if pod["@title"] == "Basic information":
                        return str(pod["subpod"]["img"]["@alt"]).replace("(", "").replace(")", "")

            except:

                try:

                    return str(res.pods[0]["subpod"]["img"]["@alt"]).replace("(", "").replace(")", "")

                except:
                    return "I honestly do not have an answer for that"

    def checkInteger(self,number):
        try: 
            int(number)
            return True
        except ValueError:
            return False

    def startSmartCooler(self,name):

        ################################------- Verification -------################################

        #Decision of verification type
        voice.speak_text("What's up " + name + ", I'm Frostttt, the smart cooler. Before restocking, Please choose your method of authentication, Voice recognition or mobile?")
        Record.startListening()
        foundIntent = str(myluis.findIntent()["topScoringIntent"]["intent"])

        #Voice verification
        if foundIntent == "Voice Recognition": 
            voice.speak_text("Please say the following quote for verification. My voice is my password, verify me")
            person = Speaker.initiate_hearing(name)
            Speaker.stop_listening()
        #OTP verification
        else:
            voice.speak_text("A one time password has been sent to your mobile number")
            sms.message()
            Record.startListening()
            OTP = str(sms.getOTP())
            print("Your OTP:", OTP)
            if str(myluis.findIntent()["query"]) == OTP:
                pass

        #User is verified, thank user
        voice.speak_text("Thank you" + str(name))

        ################################------- Topping up of drinks -------################################

        #Retrieve current drinks database
        totalItems = FetchDrinks.FetchDrinks()

        #Order dictionary to be made
        final_order = {}

        # Bot starts asking for each drink to be restocked
        for obj in totalItems.keys():
            voice.speak_text(obj + " has a quantity of " + str(totalItems[obj]) + ", how many would you like to restock?")
            print( str(obj) + " has a quantity of 1, how many would you like to restock?")

            Record.startListening()

            isInt = self.checkInteger(myluis.findIntent()["query"])
            print (isInt)
           
            while isInt != True:
                voice.speak_text("Please provide a value of a number.")
                Record.startListening()
                isInt = self.checkInteger(myluis.findIntent()["query"])


            quantity = myluis.findIntent()["query"]
            final_order[obj] = int(quantity)
            print (final_order)

        FetchDrinks.connectDB_InsertRestockDrinks(final_order)
        voice.speak_text("Okay great! Now let's place your order.")

        #Trigger RPA process
        self.triggerRPA()

        voice.speak_text("Once the order information is completed, a bot will be triggered to create a sales order in Salesforce.com. As you are observing the creation of sales order, I would like to share with you some information about this process. The technologies used for this process are: Face Verification, Voice Verification, Virtual Assistant and Robotic Process Automation. For Face Verification and Voice Verification, we are using the Microsoft Face API and Speech Recognition that is hosted in Azure Cloud. The virtual assistant is developed using the LUIS AI and Bing Speech API hosted in Azure Cloud.The Robotic Process Automation process is developed using Automation Anywhere.")

    def speak(text):
        translator = Translator('73efbc137b324049b5ad9b4eca584531')
        output = translator.speak(text, "en-IE", "Sean", "riff-16khz-16bit-mono-pcm")
        with open("data/output.wav", "wb") as f:
            f.write(output)
        pygame.mixer.pre_init(16000, -16, 2, 2048) # setup mixer to avoid sound lag
        pygame.mixer.init()
        pygame.mixer.music.load("data/output.wav")
        pygame.mixer.music.play()


    def triggerRPA(self):
        self.threadFlag = False
        tokenReq = requests.post('http://13.67.89.146/v1/authentication', headers = {'Content-Type': 'application/json'},
        data = json.dumps({'Username':'admin', 'Password': 'Accenture1'}))
        print(tokenReq.status_code)
        response = json.loads(tokenReq.text)
        print(response["token"])

        token = response["token"]

        time.sleep(2)


        triggerReq = requests.post('http://13.67.89.146/v1/schedule/automations/deploy', headers = {'Content-Type': 'application/json',
        'X-Authorization': token},
        data = json.dumps({ "taskRelativePath": "My Tasks\\SmartCoolerRPA.atmx",
        "botRunners": [{
        "client": "LSsmartcooler1",
        "user": "botrunner"}]
        })
        )

        print(triggerReq.status_code)

        if triggerReq.status_code == 200:
            print('\nDEPLOYED SUCCESSFULLY!\n')
        else:
            print('\nFAILED\n')
            response2 = json.loads(triggerReq.text)

