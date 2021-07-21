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
    
    # check topic before fetch summary and sections
    parsed_topic = utterances.topics.get(topic_str.lower())
    if parsed_topic is not None:
        summary = send_summary(parsed_topic)
        sections = get_sections(parsed_topic)
    else:
        try:
            summary = send_summary(topic_str.lower())
            sections = get_sections(topic_str.lower())
        except Exception as err:
            log.info('Unable to fetch summary: %s', err)
            # place error handling
    
    # parse sections
    # section_str = "- ".join(sections)
    section_chip = create_chip(3)
    print('SECTION CHIP:', section_chip)

    # finalize payload
    payload = {
        "fulfillmentMessages": [{
        "text": {
          "text": [
            random.choice(spiels.topics).replace("<topic>", force_text_orient(topic_str))
          ]}
      },{
        "text": {
          "text": [
            random.choice(spiels.summary_spiel) + summary
          ]}
      }
    #   ,{
    #     "text": {
    #       "text": [
    #         random.choice(spiels.sections_spiel).replace("<topic>", force_text_orient(topic_str)) + "\n\n" + "- " + section_str
    #       ]}
    #   }
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

def get_sections(topic):
    wiki_bot = wiki('en')
    page = wiki_bot.page(topic)

    try:
        section_list = []
        sections = page.sections
        for section in sections:
            if section.title in utterances.exclude_sections:
                log.info('Excluding %s in section list', section)
                break
            else:
                section_list.append(section.title + "\n")
        return section_list
    except Exception as e:
        log.info('Unable to fetch sections: %s', e)
        # error handling here

def force_text_orient(topic):                                                          
    if topic in utterances.force_match:
        return utterances.force_match.get(topic)
    else:
        return topic.title()    

def create_chip(chip_count=0):
    chip_base = {
        "richContent": [
                []
            ]
        }
    
    for ctr in range(len(chip_count)):
        chip_payload = {
            "text": "sample button text",
            "type": "button",
            "link": "https://example.org",
            "event": {
                "languageCode": "en",
                "parameters": {},
                "name": ""
            },
            "icon": {
                "color": "#FF9800",
                "type": "chevron_right"
            }
            }
        rich_content_list = chip_base.get('richContent')
        print('rich_content_list', rich_content_list, type(rich_content_list))
        
        return chip_base


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





