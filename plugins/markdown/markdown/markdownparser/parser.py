# -*- coding: UTF-8 -*-

from libs.markdown import markdown


class Parser (object):
    def __init__(self):
        pass

    def convert(self, text):
        result = markdown(text)
        return result
