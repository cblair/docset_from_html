#!/usr/bin/env python3

import os
import shutil
from get_plist_text import get_plist_text
import sqlite3

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
        # 5.1. Supported Entry Types
        # 6. Table of Contents Support (optional)

if __name__ == "__main__":
    print('foo')
    dfh = docset_from_html('foo', 'fake_html')
    dfh.run()