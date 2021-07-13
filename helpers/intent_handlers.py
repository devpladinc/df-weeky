from flask import Flask, request
import os
import sys
import random
import spiels
import json
from logs.utils import logging as log

def check_intent(action, params=''):
    # take query and get action key
    intent_dict = {
        'input.welcome' : send_greetings,
        'check.topic' : select_topic,
        'check.topic.ds' : 
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
    # topic extracted from df queryresult
    if len(topic) > 1:
        topic_str = " ".join(topic)
    else:
        topic_str = topic[0]

    payload = {
        "fulfillmentText": random.choice(spiels.topics).replace("<topic>", topic_str),
        "source": 'webhook'
    }
    return payload


def extract_ds_menus(topic):
    # # topic extracted from df queryresult
    # if len(topic) > 1:
    #     topic_str = " ".join(topic)
    # else:
    #     topic_str = topic[0]

    print('DS MENUS here')
    print('data science topic:', topic)
    
    payload = {
        "fulfillmentText": 'payload from data science',
        "source": 'webhook'
    }
    return payload



   