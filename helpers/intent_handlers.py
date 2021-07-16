from flask import Flask, request, render_template
import os
import sys
import random
import spiels
import json
from utterances import utterance
from logs.utils import logging as log
from helpers.api_handlers import Wiki_API as wiki

def check_intent(action, params=''):
    # take query and get action key
    intent_dict = {
        'input.welcome' : send_greetings,
        'check.topic' : select_topic,
        'check.topic.ds' : extract_ds_menus,
        'check.topic.programming' : extract_ds_menus
    }
    try:
        return intent_dict[action]()
    except Exception as e:
        return intent_dict[action](params)

def send_greetings():
    # send dynamic greeting
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
    try:
        wiki_menu = wiki.get_menu(topic)
        print('OLD MENU try:', wiki_menu)
        
    except Exception as e:
        # if failed to get menu, get from utterances
        log.info('Error in fetching menu: %s', e)
        menu = utterance.get(topic)
        print('OLD MENU:', menu)
    
    # menu = "\n -".join(wiki_menu)
    
    # menu filtering
    # excludes = utterance.get()
    for item in menu:
        if item in utterance.get(topic):
            menu.pop(item)

    print('NEW MENU:', menu)        

    payload = {
        "fulfillmentMessages": [{
        "text": {
          "text": [
            random.choice(spiels.menu_handler).replace("<topic>", topic)
          ]}
      },{
        "text": {
          "text": [
            menu
          ]}
      }
    ],
    "source" : 'webhook'
    }
    return payload

   