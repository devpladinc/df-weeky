from flask import Flask, request
import os
import sys
import random
import spiels

from logs.utils import logging as log

def check_intent(action, params=''):
    # take query and get action key
    intent_dict = {
        'input.welcome' : send_greetings,
        'check.topic' : select_topic
    }
    try:
        # log.info
        return intent_dict[action]()
    except Exception as e:
        # log.info
        return intent_dict[action](params)

def send_greetings():
    payload = {
        "fulfillmentText": random.choice(spiels.greetings),
        "source": 'webhook'
    }
    return payload

def select_topic(topic):
    print('select topic here')
    print('params here:', topic)
    
    payload = {
        "fulfillmentText": random.choice(spiels.topics).replace("<topic>", topic),
        "source": 'webhook'
    }
    return payload    