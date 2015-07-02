docset_from_html
================

Generates Dash docsets from HTML files. Docsets are the packaging of API
documentation, which can be viewed in docset viewers like Dash or Zeal. Docsets
are super awesome tools for quickly browsing API documentation. For more
information, see [https://kapeli.com/dash](https://kapeli.com/dash).

See http://kapeli.com/docsets for the methods, and http://kapeli.com/dash for
information about tools like Dash that use docsets.

## Usage

    docset_from_html.py <docset name> <source html directory>
        <selection config file>

### Arguments

#### docset name

The name you'd like to display for the docset. Usually the name of the language
or API, etc. Examples are python3, postgresql, jquery.

#### source html directory

The directory that holds the HTML to index. This HTML will be indexed according
to the `selection config file`, and used as the docset documentation.

#### selection config file

The file that tells docset_from_HTML how to index the HTML files. It uses
`pyquery` to select which HTML elements to index.

For example:

    {
        "a.section" : {
            "entry_type": "Structure",
            "text_sub_element": "h3"
        },
        ...
    }

The file is a JSON dictionary of dictionaries. The keys are the HTML element
to select. The value dictonary defines what attributes to assign to the
HTML selection. The element in the HTML document *must have an &lt;a&gt; name
attribute* for docset_from_html to reference the element, otherwise it will
only reference the page (not optimal).

The `entry_type` is the docset entry type to label the selection as (see
[supported entry types](https://kapeli.com/docsets#supportedentrytypes) for
more information).

The `text_sub_element` [OPTIONAL] tells docset_from_html which
sub-element/child element of the selection has the text to be used for the
search index. For example, considering the above selection config file
and this `foo.html`:

    <a name="section1" class="section">
        <h3>os.walk</h3>
    </a>

~docset_from_html will create an index entry:

text    | entry type    | path
------- | ------------- | -----------------
os.walk | Structure     | foo.html#section1