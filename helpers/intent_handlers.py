from flask import Flask, request
import os
import sys
import random
import spiels
import json
from logs.utils import logging as log
from helpers.api_handlers import Wiki_API as wiki

def check_intent(action, params=''):
    # take query and get action key
    intent_dict = {
        'input.welcome' : send_greetings,
        'check.topic' : select_topic,
        'check.topic.ds' : extract_ds_menus
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
    print("get menu topic first", topic)

    if len(topic) > 1:
        topic_str = " ".join(topic)
    else:
        topic_str = topic[0]

    # wiki_menu = wiki.get_menu(topic)
    # log.info('wiki menu %s', wiki_menu)

    payload = {
        "fulfillmentText": random.choice(spiels.menu_handler).replace("<topic>", topic_str),
        "source": 'webhook'
    }
    return payload



   