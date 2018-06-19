import http.client, urllib.parse, json
from xml.etree import ElementTree
import pygame
import time



def speak_text(text_to_say):

    apiKey = "73efbc137b324049b5ad9b4eca584531"

    params = ""
    headers = {"Ocp-Apim-Subscription-Key": apiKey}

    #AccessTokenUri = "https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken";
    AccessTokenHost = "api.cognitive.microsoft.com"
    path = "/sts/v1.0/issueToken"

    # Connect to server to get the Access Token
    print ("Connect to server to get the Access Token")
    conn = http.client.HTTPSConnection(AccessTokenHost)
    conn.request("POST", path, params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)

    data = response.read()
    conn.close()

    accesstoken = data.decode("UTF-8")
    print ("Access Token: " + accesstoken)

    body = ElementTree.Element('speak', version='1.0')
    body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
    voice = ElementTree.SubElement(body, 'voice')
    voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
    voice.set('{http://www.w3.org/XML/1998/namespace}gender', 'Male')
    voice.set('name', 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)')
    voice.text = text_to_say

    headers = {"Content-type": "application/ssml+xml",
    			"X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
    			"Authorization": "Bearer " + accesstoken,
    			"X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
    			"X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
    			"User-Agent": "TTSForPython"}

    #Connect to server to synthesize the wave
    print ("\nConnect to server to synthesize the wave")
    conn = http.client.HTTPSConnection("speech.platform.bing.com")
    conn.request("POST", "/synthesize", ElementTree.tostring(body), headers)
    response = conn.getresponse()
    print(response.status, response.reason)

    data = response.read()

    with open('data/recording.wav','wb') as output:
      output.write(data)

    # time.sleep(5)
    conn.close()

    pygame.mixer.init()
    pygame.mixer.music.load("data/recording.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

    print("Spoke text...")
    return "done"

speak_text("Hey Azman")