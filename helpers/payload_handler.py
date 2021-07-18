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

class Payload_API():

    def __init__():
        pass

    def add_payload(base, type):
        # add text payload
        if type == 'text':
            text_payload = payload.get('text_temp')
            print('GET payload:', text_payload)
            # return text_payload
            base['fulfillmentMessages'] = text_payload
            return base
        # add button payload
        if type == 'button':
            button_payload = payload.get('button_temp')
            print('GET payload:', button_payload)
            return button_payload