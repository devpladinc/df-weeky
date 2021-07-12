from flask import Flask, request
import os
import sys
import random
import spiels

def check_intent(action):
    # take query and get action key as toggle
    intent_dict = {
        'input.welcome' : send_greetings
    }

    return intent_dict[action]()
    
def send_greetings():
    payload = {
        "fulfillmentText": random.choice(spiels.greetings),
        "source": 'webhook'
    }
    return payload