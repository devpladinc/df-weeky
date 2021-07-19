from flask import Flask, request
import os
import sys
import random
import spiels
import json
from logs.utils import logging as log
from wikipediaapi import Wikipedia as wiki


class Wiki_API():

    def __init__(self):
        pass

    def get_page(query):
        page = wiki.page(query)
        return page

    def get_menu(query):
        # returns list/menu available with the query
        menu_list = wiki.search(query)
        return menu_list

    def get_summary(self, page):
        # returns str summary
        title = wiki.title(page)
        summary = title.summary(page)
        return summary

    def get_title(query):
        title = wiki.title()    
        return title

    def get_sections(self, query, sections, level=0):
        page = self.get_page(query)

        for s in sections:
                print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
