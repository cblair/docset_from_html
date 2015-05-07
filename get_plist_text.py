#!/usr/bin/env python3

def get_plist_text(cf_bundler_identifier, cf_bundle_name=None,
    docset_platform_family=None):
    """TODO"""

    cf_bundle_name = cf_bundle_name or cf_bundler_identifier.upper()
    docset_platform_family = docset_platform_family or cf_bundle_name.upper()

    return """
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>CFBundleIdentifier</key>
        <string>{cf_bundler_identifier}</string>
        <key>CFBundleName</key>
        <string>{cf_bundle_name}</string>
        <key>DocSetPlatformFamily</key>
        <string>{docset_platform_family}</string>
        <key>isDashDocset</key>
        <true/>
    </dict>
    </plist>""".format(cf_bundler_identifier=cf_bundler_identifier,
        cf_bundle_name=cf_bundle_name,
        docset_platform_family=docset_platform_family)