#!/usr/bin/env python2

import os
import shutil
from get_plist_text import get_plist_text
import sqlite3
from DocsetHtmlParser import DocsetHtmlParser

class docset_from_html:

    def __init__(self, docset_name, html_src_dir):
        self.docset_name = docset_name
        self.html_src_dir = html_src_dir

    def run(self):
        # 1. Create the Docset Folder
        os.makedirs(os.path.join(self.docset_name + '.docset', 'Contents',
            'Resources'))

        # 2. Copy the HTML Documentation
        shutil.copytree(self.html_src_dir,
            os.path.join(self.docset_name + '.docset', 'Contents', 'Resources',
                'Documentation'))

        # 3. Create the Info.plist File
        with open(os.path.join(self.docset_name + '.docset', 'Contents',
            'Info.plist'), 'w') as fp:
            fp.write(get_plist_text(cf_bundler_identifier=self.docset_name,
                cf_bundle_name=self.docset_name,
                docset_platform_family=None))

        # 4. Create the SQLite Index
        self.conn = sqlite3.connect(os.path.join(self.docset_name + '.docset','Contents','Resources','docSet.dsidx'))
        self.db_cursor = self.conn.cursor()
        self.db_cursor.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
        self.db_cursor.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

        # 5. Populate the SQLite Index
        for dirpath, dnames, fnames in os.walk(self.html_src_dir):
            for fname in fnames:
                fq_fname = os.path.join(dirpath, fname)
                with open(fq_fname) as fp:
                    docset_html_parser = DocsetHtmlParser()
                    docset_html_parser.feed(fp.read())
                    
                    elements_with_path = docset_html_parser.elements
                    for element in elements_with_path:
                        element.append(fq_fname)

                    self.db_cursor.executemany(
                        'INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)',
                        elements_with_path)

        # 6. Table of Contents Support (optional)
        # TODO

if __name__ == "__main__":
    print('foo')
    dfh = docset_from_html('foo', 'fake_html')
    dfh.run()