#!/usr/bin/env python2

from HTMLParser import HTMLParser
from entry_types import get_entry_type

# create a subclass and override the handler methods
class DocsetHtmlParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        self.tag = tag

    def handle_data(self, data):
        data = data.strip()
        if hasattr(self, 'tag') and data != '':
            if not hasattr(self, 'elements'):
                self.elements = []

            entry_type = get_entry_type(self.tag)
            if entry_type != None:
                self.elements.append(
                    [
                        # name
                        data,
                        # type
                        entry_type
                    ]
                )
