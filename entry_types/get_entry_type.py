#!/usr/bin/env python3

def get_entry_type(entry):
    """
    Get the entry type.

    TODO - doesn't do anything for now, always returns 'Structure'.

    Params:
        * entry - TODO

    """
    entry_type = None
    if entry in ['h1', 'h2', 'h3', 'h4', 'h5']:
        entry_type = 'Structure'

    return entry_type