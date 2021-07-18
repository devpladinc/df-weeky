from flask import Flask, request, render_template
import os
import sys
import random
import spiels
import json
import utterances
import convo_template
from logs.utils import logging as log
from helpers.payload_handler import Payload_API
from helpers.api_handlers import Wiki_API as wiki

payload = json.load(convo_template.payload)


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

def force_text_orient(topic):
    if topic in utterances.force_terms:
        return topic.upper()
    else:
        return topic.title()    


def extract_ds_menus(topic):
    try:  
        # get menu
        topic = topic.lower()
        menu = utterances.menu.get(topic)
        print('MENU HERE:', menu)
        print('menu type:', type(menu))

    except Exception as e:
        log.info('unable to get topic %s', e)
    
    # force text convention
    ftopic = force_text_orient(topic)

    # payload = {
    #     "fulfillmentMessages": [{
    #     "text": {
    #       "text": [
    #         random.choice(spiels.menu_handler).replace("<topic>", ftopic)
    #       ]}
    #   },{
    #     "text": {
    #       "text": 
    #         menu 
    #       }
    #   }
    # ],
    # "source" : 'webhook'
    # }


    # payload = {
    #     "fulfillmentMessages": [{
    #     "text": {
    #       "text": [
    #         random.choice(spiels.menu_handler).replace("<topic>", ftopic)
    #       ]}
    #   },{
    #     "payload": {
    #         "richContent": [
    #             [{
    #                 "subtitle": "Azure subtitle",
    #                 "image": {
    #                     "src": {
    #                         "rawUrl": "https://example.com/images/logo.png"
    #                     }
    #                 },
    #                 "actionLink": "https://wikipedia.org/wiki/azure",
    #                 "title": menu[0],
    #                 "type": "info"
    #             }]
    #         ]
    #     }
    # }
    # ],
    # "source" : 'webhook'
    # }

    
    rich_payload = payload.get('base_temp')
    print('PAYLOAD TEMP LANG:', payload)
    update_payload = Payload_API.add_payload(rich_payload, 'text')
    print('PAYLOAD SAMPLE WITH TEXT:', update_payload)
   

    return update_payload





   