"""
Routines and classes to assist in inspecting/debugging variables.
Created by: Tony Held tony.held@gmail.com
Created on: 2021-02-10
Copyright © 2021 Tony Held.  All rights reserved.
"""

def values(var, mode='plain-text', exclude_starting_with='_'):
    """Show a variable's attributes and values for diagnostic debugging purposes.

    Parameters
    -----------
    var :
        variable to inspect using the dir and getattr functions

    mode : str ("plain-text" | "html")
        mode determines what characters are used for line separation.
            plain-text '\n' is used
            otherwise html is used

    exclude_starting_with : str
        Pattern to exclude from inspection of dir output.
        ''   -  turns off filtering (zero length string)
        '_'  - excludes all attributes starting with a single underscore
        '__' - excludes all attributes starting with a double underscore
    """

    mytype = strip_single_tag(type(var))

    if mode == 'plain-text':
        print(f'Variable type: {mytype}')
    else:
        print(f'Variable type: {mytype}<br>')

    if exclude_starting_with:
        attrs = [i for i in dir(var) if not i.startswith(exclude_starting_with)]
    else:
        attrs = [i for i in dir(var)]

    for i in attrs:
        if mode == 'plain-text':
            print(f'\n{i}:\n{"-" * 20}\n'
                  f'{getattr(var, i)}')
        else:
            print(f'<hr>{i}:<br>{"-" * 20}<br>'
                  f'{strip_single_tag(getattr(var, i))}')


def strip_single_tag(text):
    """Remove starting '<' and ending '>' from a string
    that is appears to be a single html tag.

    This will avoid confusing text of the form <text> with html.

    Parameters
    ------------
    text : str
        text that potentially has html text
    """

    # if the argument is not a string, try to make it one
    if not isinstance(text, str):
        text = str(text)

    # if the string starts with '<' and ends with '>'
    # but there are no additional tags in the string, then
    # assume the input text is not really html
    # but rather output that looks like a single tag

    if text.startswith('<') and text.endswith('>'):
        # strip the outer tag
        text_inner = text[1:-1]
        # check if there are any additional tags
        if '<' not in text_inner:
            text = text_inner

    return text
