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

    def get_page(self, query):
        page = wiki.page(query)
        self.page = page
        return page

    def get_title(self):
        page = self.page
        title = wiki.title(page)
        return title
    
    def get_summary(page):
        # returns str summary
        title = wiki.title(page)
        summary = title.summary(page)
        return summary

    def get_sections(self, query, sections, level=0):
        page = self.get_page(query)

        for s in sections:
                print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
