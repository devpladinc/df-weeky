from flask import Flask, request
import os
import sys


def check_intent(action):
    # take query and get action key as toggle
    intent_dict = {
        'input.welcome' : send_greetings
    }

    return intent_dict[action]()
    
def send_greetings():
    print('send greetings')
    payload = {
        "fulfillmentText": 'This is from the replit webhook',
        "source": 'webhook'
    }
    return payload