from flask import Flask, request
import os
import sys
import random
import spiels
import json
from logs.utils import logging as log
import wikipedia as wiki


class Wiki_API():

    def __init__():
        pass

    def get_menu(query):
        # returns list/menu available with the query
        print('inside get menu')
        menu_list = wiki.search(query)
        print(menu_list)
        return menu_list