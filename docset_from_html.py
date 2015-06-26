#!/usr/bin/env python3

import os
import sys
import shutil
from get_plist_text import get_plist_text
import sqlite3
#from DocsetHtmlParser import DocsetHtmlParser
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

    def __population_sqlite_index(self, html_dst_dir):
        for dirpath, dnames, fnames in os.walk(html_dst_dir):
            for fname in fnames:
                fq_fname = os.path.join(dirpath, fname)
                with open(fq_fname) as fp:
                    filetext = fp.read()

                    dom = pq(filetext)

                    elements_with_path = []
                    for selection_text, entry_type in self.config_selections.items():
                        selections = dom(selection_text)
                        for selection in selections:
                            print(selection_text + ':' + selection.text)
                            elements_with_path.append(
                                    [
                                        # name
                                        selection.text,
                                        # type
                                        entry_type,
                                        #path
                                        # TODO: need to add # name reference so
                                        # clicking on the index will go to the
                                        # page section (if html name attr is
                                        # set). User selection.attrib.
                                        os.path.join(dirpath, fname).replace(
                                            html_dst_dir + os.sep, '')
                                    ]
                                )

                    self.db_cursor.executemany(
                        'INSERT OR IGNORE INTO searchIndex' +
                            '(name, type, path) VALUES (?,?,?)',
                        elements_with_path)
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
    # Simple options handling.
    if len(sys.argv) != 4:
        print(
            'Usage: docset_from_html.py <docset name> ' + 
                '<source html directory> <selection config file>')
        sys.exit(1)

    dfh = docset_from_html(sys.argv[1], sys.argv[2], sys.argv[3])
    dfh.run()
