#!/usr/bin/env python3

import os
import sys
import shutil
from get_plist_text import get_plist_text
import sqlite3
import re
import lxml
import json
from pyquery import PyQuery as pq

class docset_from_html:

    def __init__(self, docset_name, html_src_dir, config_filename):
        self.docset_name = docset_name
        self.html_src_dir = html_src_dir
        self.config_file = open(config_filename, 'r')

        self.config_selections = json.loads(self.config_file.read())

    def __del__(self):
        self.config_file.close()

    def __make_docset_folder(self):
        os.makedirs(os.path.join(self.docset_name + '.docset', 'Contents',
            'Resources'))

    def __create_info_plist_file(self):
        with open(os.path.join(self.docset_name + '.docset', 'Contents',
            'Info.plist'), 'w') as fp:
            fp.write(get_plist_text(cf_bundler_identifier=self.docset_name,
                cf_bundle_name=self.docset_name,
                docset_platform_family=None))

    def __create_sqlite_index(self):
        self.conn = sqlite3.connect(
            os.path.join(self.docset_name + 
                '.docset','Contents','Resources','docSet.dsidx'))
        self.db_cursor = self.conn.cursor()
        self.db_cursor.execute('CREATE TABLE searchIndex ' +
            '(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
        self.db_cursor.execute('CREATE UNIQUE INDEX anchor ON searchIndex' +
            '(name, type, path);')

    # TODO - refactor, split out into more separate methods
    def __population_sqlite_index(self, html_dst_dir):
        fileregex = re.compile('^.*\.html')
        # For every file in the destination directory...
        for dirpath, dnames, fnames in os.walk(html_dst_dir):
            for fname in fnames:

                # If the file is not an html file, go to the next one.
                if not fileregex.match(fname):
                    continue

                # Open the file and process it
                fq_fname = os.path.join(dirpath, fname)
                with open(fq_fname) as fp:
                    try:
                       filetext = fp.read()
                    except:
                       filetext = ""

                    # Get a DOM object from the text.
                    try:
                        dom = pq(filetext)
                        print("Processing " + fq_fname)
                    except ValueError as e:
                        print("WARN: ignoring {fname}, error: {error}".format(
                            fname=fq_fname, error=e))
                        continue
                    except lxml.etree.XMLSyntaxError as e:
                        print("WARN: ignoring {fname}, error: {error}".format(
                            fname=fq_fname, error=e))
                        continue

                    # Collect all the elements in the DOM we care about based
                    # on the selection configuration, and craft our search index
                    # data from it.
                    search_index_data = []
                    for key in self.config_selections.keys():
                        config_selection = self.config_selections[key]

                        # Get all the elements that match in the DOM.
                        elements = dom(key)
                        for element in elements:
                            # The optional reference to the page section, using
                            # the HTML name attribute.
                            section_reference = ""
                            # TODO: check that its an <a> element too.
                            # TODO: support HTML 5 id attribute
                            if 'name' in element.attrib.keys():
                                section_reference = "#" + element.attrib['name']

                            # Set the search text to the element's text, or
                            # what the config wants it set to.
                            element_text = element.text
                            if 'text_sub_element' in config_selection.keys():
                                sub_element = element.find(
                                    config_selection['text_sub_element'])
                                element_text = sub_element.text if \
                                    sub_element != None else ""

                            search_index_data.append(
                                [
                                    # name
                                    element_text,
                                    # type
                                    config_selection['entry_type'],
                                    #path
                                    # TODO: need to add # name reference so
                                    # clicking on the index will go to the
                                    # page section (if html name attr is
                                    # set). User element.attrib.
                                    os.path.join(dirpath, fname).replace(
                                        html_dst_dir + os.sep, ''
                                        ) + section_reference
                                ]
                            )

                    self.db_cursor.executemany(
                        'INSERT OR IGNORE INTO searchIndex' +
                            '(name, type, path) VALUES (?,?,?)',
                        search_index_data)
        self.conn.commit()

    def run(self):
        html_dst_dir = os.path.join(
            self.docset_name + '.docset', 'Contents', 'Resources', 'Documents')

        # 1. Create the Docset Folder
        self.__make_docset_folder()

        # 2. Copy the HTML Documents
        shutil.copytree(self.html_src_dir, html_dst_dir)

        # 3. Create the Info.plist File
        self.__create_info_plist_file()

        # 4. Create the SQLite Index
        self.__create_sqlite_index()

        # 5. Populate the SQLite Index
        self.__population_sqlite_index(html_dst_dir)

        # 6. Table of Contents Support (optional)
        # TODO

        # Cleanup
        self.conn.close()

if __name__ == "__main__":
    # Simple cheesy options handling.
    if len(sys.argv) != 4:
        print(
            'Usage: docset_from_html.py <docset name> ' + 
                '<source html directory> <selection config file>')
        sys.exit(1)

    dfh = docset_from_html(sys.argv[1], sys.argv[2], sys.argv[3])
    dfh.run()
