#!/usr/bin/env python3

import os
import shutil
from gep_plist_text import get_plist_text

class docset_from_html:

    def __init__(self):
        pass

    def run(self, docset_name, html_src_dir):
        # 1. Create the Docset Folder
        os.mkdirs(os.path.join(docset_name + '.docset', 'Contents',
            'Resources'))

        # 2. Copy the HTML Documentation
        shutil.copytree(html_src_dir,
            os.path.join(docset_name + '.docset', 'Contents', 'Resources',
                'Documentation'))

        # 3. Create the Info.plist File
        with open(os.path.join(docset_name + '.docset', 'Contents',
            'Info.plist')) as fp:
            fp.write(get_plist_text(cf_bundler_identifier=,
                cf_bundle_name=docset_name,
                docset_platform_family=None))

        # 4. Create the SQLite Index
        # 5. Populate the SQLite Index
        # 5.1. Supported Entry Types
        # 6. Table of Contents Support (optional)