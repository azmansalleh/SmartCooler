########### Python 3.6 #############
import requests
import bingSpeech

def findIntent():
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '0eab200592454b9db971643a2f787f9c',
    }

    params ={
        # Query parameter
        # 'q': 'tell me about liquid',
        'q': bingSpeech.getText(),
        # Optional request parameters, set to default values
        'timezoneOffset': '0',
        'verbose': 'false',
        'spellCheck': 'false',
        'staging': 'false',
    }

    try:
        r = requests.get('https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/446e292b-1e92-4612-afa9-b4a74d5290c3',headers=headers, params=params)
        print(r.json())
        return r.json()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################