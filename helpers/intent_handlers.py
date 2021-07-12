from flask import Flask, request
import os
import sys

class Integrator():

    def __init__(self):
        pass

    def check_intent(action):
        # take query and get action key as toggle
        intent_dict = {
            'input.welcome' : send_greetings
        }

        intent_dict[action]()
        
    def send_greetings():
        return {
            "fulfillmentText": 'Greetings! from function',
            "source": 'webhook'
        }