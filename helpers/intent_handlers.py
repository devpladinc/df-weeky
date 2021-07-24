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
from flask_redis import FlaskRedis

def check_intent(action, params=''):
    # take query and get action key 
    intent_dict = {
        'input.welcome' : send_greetings,
        'check.topic' : select_topic,
        'check.see.more' : send_see_more
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
    
    # parse summary chops
    primary_spiel_list = summary[0]
    print(len(primary_spiel_list))
    summary_parse = " ".join(primary_spiel_list)
    
    # see more button front-end
    see_more_btn = create_see_more_button()
    log.info('See more btn %s', see_more_btn)

    # generate dynamic chip
    section_chip = create_chip(sections, 3)
    log.info('Section chip: %s', section_chip)

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
            random.choice(spiels.summary_spiel) + summary_parse + "..."
          ]}
      }
    #   ,{
    #     "text": {
    #       "text": [
    #         random.choice(spiels.sections_spiel).replace("<topic>", force_text_orient(topic_str))
    #       ]}
    #   }
    #   ,section_chip
        ,see_more_btn
    ],
    "source" : 'webhook'
    }

    return payload

def send_summary(topic):
    wiki_bot = wiki('en')

    try: 
        page = wiki_bot.page(topic)
        summary_data = page.summary
        summaries = []

        # parsing summary for 'see more'
        summary_chop_list = summary_data.split(". ")

        if len(summary_chop_list) < 8:    
            primary_summary = summary_chop_list[:2]
            secondary_summary = summary_chop_list[3:]

        elif len(summary_chop_list) > 8 and len(summary_chop_list) < 15:
            primary_summary = summary_chop_list[:5]
            secondary_summary = summary_chop_list[6:]

        else:
            primary_summary = summary_chop_list[:4]
            secondary_summary = summary_chop_list[5:]

        summaries.append(primary_summary)
        summaries.append(secondary_summary)
        # for see more send
        # summaries.append(topic)
        return summaries
        
       
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
                section_list.append(section.title)
        return section_list
    except Exception as e:
        log.info('Unable to fetch sections: %s', e)
        # error handling here

def force_text_orient(topic):                                                          
    if topic in utterances.force_match:
        return utterances.force_match.get(topic)
    else:
        return topic.title()    

def create_chip(section_list, chip_count=0):
    
    sections = section_list
    
    chip_base = {
        "payload" :{
        "richContent": [
                []
            ]
        }}


    main_menu_payload = {
            "text": "Back to Main Menu",
            "type": "button",
            "link": "https://example.org",
            "event": {
                "languageCode": "en",
                "parameters": {},
                "name": "WELCOME"
            },
            "icon": {
                "color": "#FF9800",
                "type": "chevron_right"
            }
            }    
    
    ctr = 0
    for ctr in range(chip_count):
        chip_payload = {
            "text": sections[ctr],
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
        rich_content_list = chip_base.get('payload').get('richContent')[0]
        rich_content_list.append(chip_payload)
        ctr += 1

    # add menu payload
    rich_content_list = chip_base.get('payload').get('richContent')[0]
    rich_content_list.append(main_menu_payload)
    
    return chip_base

def create_see_more_button():
    button_payload = {
        "payload" : {
            "richContent": [
            [
            {
                "type": "button",
                "icon": {
                "type": "check_circle",
                "color": "#f252ad"
                },
                "text": "See more description",
                "event": {
                    "name": "see-more",
                    "languageCode": "en-US",
                }
            }
            ]
        ]
        }
    }

    return button_payload

def send_see_more(topic):
    payload = {
        "fulfillmentMessages": [
      {
        "text": {
          "text": [
          ]}
      }
    ],
    "source" : 'webhook'
    }

    return payload

