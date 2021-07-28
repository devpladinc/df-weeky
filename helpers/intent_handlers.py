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
from app import redis_client as rc

def check_intent(action, params=''):
    # take query and get action key 
    intent_dict = {
        'input.welcome' : send_greetings,
        'input.unknown' : send_fallback_greetings,
        'check.topic' : select_topic,
        'check.topic-yes' : send_section_chips,
        'check.topic-no' : ask_back_menu,
        'check-topic-backmenu' : send_greetings,
        'check.topic-stay' : send_stay_topic,
        'check.see.more' : send_see_more,
        'check.data.science' : select_topic,
        'check.machine.learning' : select_topic,
        'check.programming' : select_topic,
        'check.ds-yes' : send_section_chips,
        'check.ml-yes' : send_section_chips,
        'check.pl-yes' : send_section_chips,
        'check.ds-no' : ask_back_menu,
        'check.ml-no' : ask_back_menu,
        'check.pl-no' : ask_back_menu,

    }
    try:
        return intent_dict[action]()
    except Exception as e:
        return intent_dict[action](params)
        

def send_greetings():
    # create main chips
    # create new session redis
    main_chip = create_main_chips()

    payload = {
        "fulfillmentMessages": [{
        "text": {
          "text": [
           random.choice(spiels.greetings)
          ]}
      }
      ,main_chip
    ],
    "source" : 'webhook'
    }
    return payload


def send_fallback_greetings():
    # create main chips
    # create new session redis
    main_chip = create_main_chips()

    payload = {
        "fulfillmentMessages": [{
        "text": {
          "text": [
           random.choice(spiels.greetings_fallback)
          ]}
      }
      ,main_chip
    ],
    "source" : 'webhook'
    }
    return payload


def select_topic(topic):
    
    if len(topic) > 1:
        # dynamic handling
        # suggestion spiel - send topic as list
        # topic_str = " ".join(topic)
        suggested_chips = suggest_topics(topic)
        return suggested_chips
    else:
        topic_str = topic[0]

    # check topic text orient before fetch summary
    parsed_topic = utterances.topics.get(topic_str.lower())
    if parsed_topic is not None:
        summary = send_summary(parsed_topic)
        # cache save topic
        rc.set("topic", parsed_topic)
    else:
        try:
            summary = send_summary(topic_str.title())
            rc.set("topic", topic_str.lower())
        except Exception as err:
            log.info('Unable to fetch summary: %s', err)
            # place error handling
    
    # parse summary (list) chops
    primary_spiel_list = summary[0]
    summary_parse = " ".join(primary_spiel_list)
    
    # see more button front-end
    see_more_btn = create_see_more_button()
    log.info('See more btn %s', see_more_btn)

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
            random.choice(spiels.summary_spiel) + summary_parse + " ..."
          ]}
      },see_more_btn
      ,{
        "text": {
          "text": [
           "Do you want to know more about " + force_text_orient(topic_str) + "?"
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
        summaries = []

        # parsing summary for 'see more'
        summary_chop_list = summary_data.split(". ")

        if len(summary_chop_list) < 8:    
            primary_summary = summary_chop_list[:2]
            secondary_summary = summary_chop_list[3:]

        elif len(summary_chop_list) > 8 and len(summary_chop_list) < 15:
            primary_summary = summary_chop_list[:5]
            secondary_summary = summary_chop_list[6:10]

        else:
            primary_summary = summary_chop_list[:4]
            secondary_summary = summary_chop_list[4:8]

        summaries.append(primary_summary)
        summaries.append(secondary_summary)
        log.info('summaries saved: %s', len(summaries))
        return summaries
    
    except Exception as e:
        log.info('Fetch summary error: %s', e)
        return e

def get_sections(topic):
    # sections title saving
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
    #  chip list of suggestion after summary
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
            "event": {
                "languageCode": "en-US",
                "parameters": {},
                "name": ""
            },
            "icon": {
                "color": "#f252ad",
                "type": "menu"
            }
            }
    
    ctr = 0
    for ctr in range(chip_count):
        chip_payload = {
            "text": sections[ctr],
            "type": "button",
            "event": {
                "languageCode": "en-US",
                "parameters": {},
                "name": ""
            },
            "icon": {
                "color": "#f252ad",
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
    # see more FE
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

def send_see_more():
    # put conditional that should be matching session
    # use redis cached topic to call see more summary
    # see more - summary list [0]
    topic = rc.get("topic")
    summary = " ".join(send_summary(topic)[1])
    log.info('See more: %s', summary)
    
    payload = {
        "fulfillmentMessages": [
      {
        "text": {
          "text": [ summary + "."
          ]}
      }
    ],
    "source" : 'webhook'
    }
    return payload

def create_main_chips():
    sections = [str(sec) for sec in utterances.main_chips.keys()]
    section_actions = [str(sec) for sec in utterances.main_chips.values()]

    chip_base = {
        "payload" :{
        "richContent": [
                []
            ]
        }
    }
    
    ctr = 0
    for ctr in range(len(sections)):
        chip_payload = {
            "text": sections[ctr],
            "type": "button",
            "event": {
                "languageCode": "en-US",
                "parameters": {},
                "name": section_actions[ctr]
            },
            "icon": {
                "color": "#f252ad",
                "type": "trending_up"
            }
            }
        rich_content_list = chip_base.get('payload').get('richContent')[0]
        rich_content_list.append(chip_payload)
        ctr += 1

    log.info('Main chips sent: %s', chip_base)
    return chip_base

def send_section_chips():
    # trimmed from select topics to independent trigger via see-topic follow-up
    # generate dynamic chip
    log.info('PASOK DITO SA follow up yes')
    topic_str = rc.get("topic")

    if topic_str is not None:
        sections = get_sections(topic_str)

    section_chip = create_chip(sections, 3)
    log.info('Section chip: %s', section_chip)

    payload = {
        "fulfillmentMessages": [
            section_chip
    ],
    "source" : 'webhook'
    }
    return payload

def ask_back_menu():

    payload = {
        "fulfillmentMessages": [{
        "text": {
          "text": [
           "Would you like to go back to main menu?"
          ]}
      }
    ],
    "source" : 'webhook'
    }
    return payload

def send_stay_topic():

    payload = {
        "fulfillmentMessages": [{
        "text": {
          "text": [
               random.choice(spiels.stay_topic_spiel)
          ]}
      }
    ],
    "source" : 'webhook'
    }
    return payload

def suggest_topics(topic_list):
    # multiple topics detected
    # do not forget about count of chips
    # FE
    suggestion_chips = create_chip(topic_list, len(topic_list))
    log.info('Suggestion chips: %s', suggestion_chips)
    # BE

    for topic in topic_list:
        summary_list = send_summary(topic)
        log.info("summary lists %s", summary_list)
        
    topic_list_str = " and ".join(topic_list)
    payload = {
        "fulfillmentMessages": [{
        "text": {
          "text": [
               (random.choice(spiels.suggest_topics_spiel)).replace("<topics>", topic_list_str)
          ]}
      },
            suggestion_chips
    ],
    "source" : 'webhook'
    }
    return payload