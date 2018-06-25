import luis
import ccxt
import string
import requests
import json
import time
import os


app_key = "e6fb4176-a08b-41ba-9b99-d6afc52414f5"
sub_key = "9763c3dafa1c40319c88a91d354759e7"



def train():

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": sub_key#"5edc4020a60a475d90b45020d5f8fc00"
    }

    url = "https://westus.api.cognitive.microsoft.com/luis/api/v2.0/apps/" + str(app_key) + "/versions/0.1/train"

    r = requests.post(url, headers=headers)
    # print(r.content)


    print("Trained Data: " + str(r.content))



def add_intent_utterence(utterance, intent):

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": sub_key#5edc4020a60a475d90b45020d5f8fc00"
    }

    url = "https://westus.api.cognitive.microsoft.com/luis/api/v2.0/apps/" + str(app_key) + "/versions/0.1/examples"

    # POST the request


    data = [
	{
		"text": utterance,
		"intentName": intent
	}
    ]

    r = requests.post(url, data=json.dumps(data), headers=headers)
    # print(r.content)


    print("added new utterance with response: " + str(r.content) + "... training now")
    train()


def find_entity_key(entities_array, key):
    entities = entities_array
    # start_index = None
    for entity in entities:
        if str(entity.type) == "builtin.currency":
            start_index = entity.start_index
            end_index = entity.end_index

            for entity2 in entities:
                if str(entity2.type) == "builtin.number" and (int(entity2.start_index) == int(start_index) or int(entity2.end_index) == int(end_index)):
                    del entities[entities.index(entity2)]


        if str(entity.type) == "builtin.percentage":
            start_index = entity.start_index
            end_index = entity.end_index

            for entity2 in entities:
                if str(entity2.type) == "builtin.number" and (int(entity2.start_index) == int(start_index) or int(entity2.end_index) == int(end_index)):
                    del entities[entities.index(entity2)]





    for entity in entities:
        if str(entity.type) == str(key):
            # print(entity.resolution["values"])

            if key == "builtin.number" or key == "builtin.currency" or key == "builtin.percentage":
                return entity.resolution["value"]
            else:
                if entity.resolution is None:
                    return entity.entity
                else:
                    return entity.resolution["values"][0]
        if entity == entities[-1]:
            return "Not found"

    return "Not found"


def analyze_text(query):
    l = luis.Luis(url='https://eastus.api.cognitive.microsoft.com/luis/v2.0/apps/' + str(app_key) + '?subscription-key=' + str(sub_key) + '&verbose=true&timezoneOffset=0&q=')

    user_request = query#input("What do you want to do? ")
    r = l.analyze(user_request)


    return r
    #
    # if r.best_intent().intent == "None":
    #     add_to = "No strong corrolation, highest found: " + str(r.best_intent().intent) + " for query: '" + str(user_request) + "'. Press enter, or say cancel to ignore this")
    #
    #     if add_to == "cancel":
    #         pass
    #
    #     elif len(add_to) < 1:
    #         add_intent_utterence(user_request, str(r.best_intent().intent))
    #     else:
    #         add_intent_utterence(user_request, add_to)
