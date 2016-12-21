#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Context(object):
    """
    This class contains tuple (text,date) representing 
    for context part in the query
    """
    def __init__(self, text=None, date=None):
        self.text = text
        self.date = date

class Query(object):
    """
    The implementation of query object
    """
    def __init__(self, entity, context):
        self.entity = entity
        self.context = context
