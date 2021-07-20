from flask import Flask, request, render_template
import os
import sys
import random
import spiels
import json
import utterances
from convo_template import payload
from logs.utils import logging as log
from wikipediaapi import Wikipedia as wiki


def check_intent(action, params=''):
    # take query and get action key 
    intent_dict = {
        'input.welcome' : send_greetings,
        'check.topic' : select_topic
    }
    try:
        return intent_dict[action]()
    except Exception as e:
        return intent_dict[action](params)
        

def send_greetings():
    payload = {
        "fulfillmentText": random.choice(spiels.greetings),
        "source": 'webhook'
    }
    return payload

def select_topic(topic):
    # parse topic query
    if len(topic) > 1:
        topic_str = " ".join(topic)
    else:
        topic_str = topic[0]
    
    # check topic before fetch summary
    try:
        parsed_topic = utterances.topics.get(topic_str.lower())
        summary = send_summary(parsed_topic)
    except Exception as e:
        log.info('not in the keyword mapping', e)
        try:
            summary = send_summary(topic_str.lower())
        except Exception as err:
            log.info('Unable to fetch summary: %s', err)
            # place error handling

    payload = {
        "fulfillmentMessages": [{
        "text": {
          "text": [
            random.choice(spiels.topics).replace("<topic>", topic_str.title())
          ]}
      },{
        "text": {
          "text": [
            random.choice(spiels.summary_spiel) + summary
          ]}
      }
    ],
    "source" : 'webhook'
    }

    return payload

def send_summary(topic):
    wiki_bot = wiki('en')

    try: 
        page = wiki_bot.page(topic)
        summary_data = page.summary
        summary = summary_data.replace(".\n", ".\n\n")

        return summary
       
    except Exception as e:
        log.info('Fetch summary error: %s', e)
        return e


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





