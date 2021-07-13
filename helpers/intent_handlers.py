from flask import Flask, request
import os
import sys
import random
import spiels

def check_intent(action):
    # take query and get action key as toggle
    intent_dict = {
        'input.welcome' : send_greetings,
        'check.topic' : select_topic
    }

    return intent_dict[action]()
    
def send_greetings():
    payload = {
        "fulfillmentText": random.choice(spiels.greetings),
        "source": 'webhook'
    }
    return payload

def select_topic():
    payload = {
        "fulfillmentText": random.choice(spiels.topics),
        "source": 'webhook'
    }
    return payload    