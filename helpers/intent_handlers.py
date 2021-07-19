from flask import Flask, request, render_template
import os
import sys
import random
import spiels
import json
import utterances
from convo_template import payload
from logs.utils import logging as log
from helpers.api_handlers import Wiki_API as wiki


def check_intent(action, params=''):
    # take query and get action key
    intent_dict = {
        'input.welcome' : send_greetings,
        'check.topic' : select_topic
        # 'check.topic.ds' : extract_ds_menus,
        # 'check.topic.programming' : extract_ds_menus
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

def send_summary(topic):
    try: 
        page_name = wiki.get_page(topic)
        print('PAGE NAME:', page_name)

        summary = wiki.get_summary(page_name)
        print('SUMMARY:', summary)
    except Exception as e:
        log.info('Fetch summary error:', e)   


def force_text_orient(topic):
    if topic in utterances.force_terms:
        return topic.upper()
    else:
        return topic.title()    


# def extract_ds_menus(topic):
#     try:  
#         # get menu
#         topic = topic.lower()
#         menu = utterances.menu.get(topic)
#         # print('MENU HERE:', menu)
#         # print('menu type:', type(menu))

#     except Exception as e:
#         log.info('unable to get topic %s', e)
    
#     # force text convention
#     ftopic = force_text_orient(topic)

#     button_list = []
#     for item in menu:
#         button = {
#             "payload": {
#                 "richContent": [
#                     [{
#                         "subtitle": "Azure subtitle",
#                         "image": {
#                             "src": {
#                                 "rawUrl": "https://example.com/images/logo.png"
#                             }
#                         },
#                         "actionLink": "https://wikipedia.org/wiki/azure",
#                         "title": item,
#                         "type": "info"
#                     }]
#                 ]
#             }
#         }
#         button_list.append(button)

#     payload = {
#         "fulfillmentMessages": [{
#         "text": {
#           "text": [
#             random.choice(spiels.menu_handler).replace("<topic>", ftopic)
#           ]}
#       },
#     button_list[0],
#     button_list[1],
#     button_list[2]
#     ],
#     "source" : 'webhook'
#     }

#     return payload





   