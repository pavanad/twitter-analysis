
# -*- coding: utf-8 -*-

import re

def remove_url(text):
    """
    Remove url from text

    Args:
        text:   string with text
    
    Return:
        string without the url
    """
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", text).split())    