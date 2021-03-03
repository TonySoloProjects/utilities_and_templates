"""
Collection of utilities to assist in learning how to use
introspection of the python stack and other coding techniques.

Created by: Tony Held tony.held@gmail.com
Created on: 2020-08-13
Copyright © 2020 Tony Held.  All rights reserved.
"""

import traceback
import os
import sys


def stack_info(stack_print=True, short_filename=True):
    """Inspect the call stack to learn how a methods are invoked.

    Parameters
    ----------
    stack_print : boolean
        Flag to print full contents of the stack.
    short_filename : boolean
        Option to use simple file names rather than the full path
    Returns
    -------
    filenames : []
        File names associated call stack
    linenums : []
        Line number of associated file names
    function_names : []
        Enclosed function that statement was made from
    statements : []
        Statement added to the call stack

    Notes
    -------
    The stack is organized such that index 0 is the first call (likely at a module level)
    The last index will be the location of the line traceback.extract_stack() in this function
    You will likely want stack_index -2 or -3 to see your line of code of interest
    """
    # Find the current callback stack
    stack_calls = traceback.extract_stack()

    # Initialize lists to store callback information
    filenames = []
    linenums = []
    function_names = []
    statements = []

    if stack_print:
        print(f"Stack Length = {len(stack_calls)}")
        print(f"Stack Index, File Name, Line Number, Function, Statement")

    for i, call in enumerate(stack_calls):
        filename, linenum, function_name, statement = call

        if short_filename:
            _, filename = os.path.split(filename)

        filenames.append(filename)
        linenums.append(linenum)
        function_names.append(function_name)
        statements.append(statement)

        if stack_print:
            my_list = [i, filename, linenum, function_name, statement]
            my_string = ', '.join(map(str, my_list))
            print(my_string)

    return filenames, linenums, function_names, statements


def my_calling_statement(stack_index=-3):
    """Inspect the call stack to see what statement was issued
        that resulted in this function being called.

    Parameters
    ----------
    stack_index : int
        Index of stack call of interest
    Returns
    -------
    statement : str
        Statement added to the call stack at the stack_index
    Notes
    -------
    You will likely want stack_index -2 or -3 to see your line of code of interest
    See stack_info for details
    """
    filename, linenum, function_name, statement = traceback.extract_stack()[stack_index]
    return statement


def function_arguments(func_call):
    """Find the arguments of a string representation of a function call.

    Parameters
    ----------
    func_call : str
        Function call in the format function(arg1, arg2 ...)
    Returns
    -------
    arguments : str
        text between the parentheses in the function call as a single string
    """
    first = func_call.find('(')
    last = func_call.rfind(')')
    str_args = func_call[first+1:last]
    # remove all whitespace and separate on comma
    str_args = str_args.replace(" ", "")
    str_args = str_args.split(',')
    # print(str_args)
    return str_args


def get_max_char(x, max_char=500):
    """Trim a string to a maximum number of characters to avoid printing excessive text.

    Parameters
    ----------
    x : str
        string that will be potentially trimmed
    max_char : int
        Maximum number of characters to print
    Returns
    -------
    y : str
        original string if len(x) < max_char or truncated string
    """
    x_len = len(x)
    y = x[:max_char]
    if x_len > max_char:
        y = f"{y} ... <1st {max_char} shown, {x_len-max_char} suppressed>"
    return y


def func1(arg1='mytext1'):
    func2('Simple String Argument')


def func2(arg2='mytext1'):
    x = stack_info()
    print(x)
    y = my_calling_statement()
    print(y)
    z = function_arguments(y)
    print(z)


def print_all(*args, output_mode='!s'):
    """Diagnostic to output a list of variables and their values each on their own line.
     This helps to make debugging print statements faster to type.

    Parameters
    ----------
    *args :
        Arguments you want diagnostic information for
    output_mode : str
        Selects whether the __str__ or __repr__ function will be invoke in string conversion.
        Can be either '!r' for repr or '!s' for str
    Returns
    -------
    """
    # get variable names from the stack call
    mcs = my_calling_statement()
    fa = function_arguments(mcs)
    # Always print the variable names with !s, but use the output_mode to for variable content
    for i, j in zip(fa, args):
        if output_mode == '!s':
            print('--- {!s} ---\n{!s}'.format(i, j))
        elif output_mode == '!r':
            print('--- {!s} ---\n{!r}'.format(i, j))

# Based on: https://stackoverflow.com/questions/4664850/how-to-find-all-occurrences-of-a-substring


def findall(p, s):
    """Yields all the positions of the pattern p in the string s."""
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)


def update_pip():
    """
    Routine to update or share your pip installation configurations.

    Created by: Tony Held tony.held@gmail.com
    Created on: 2021/03/XX
    Copyright © 2021 Tony Held.  All rights reserved.

    Notes
    --------
    1) Now that I use anaconda, so I don't often have to pip install packages.
    2) Approach inspired by:
            https://stackoverflow.com/questions/2720014/how-to-upgrade-all-python-packages-with-pip/33667992#33667992
    """
    fn_before_update = 'testing_files/pip_versions_before.txt'
    fn_requirements = 'testing_files/pip_requirements.txt'

    os.system(f'pip freeze > {fn_before_update}')
    # This will create a file with the head of
    # altgraph==0.17
    # argon2-cffi==20.1.0
    # ...

    # parse the output file and find all version names
    with open(fn_before_update, "r") as f_in, open(fn_requirements, "w") as f_out:
        for line in f_in:
            line_out = line.replace("==", ">=")
            f_out.write(line_out)
    exit()

    # I actually ran this from the command line to see the output rather than the line below
    # pip install -r requirements_file_name.txt --upgrade
    os.system(f'pip install -r {fn_requirements} --upgrade')


def display_python_version():
    """Display python version and related info."""
    print(f"Python version: {sys.version}")
    print(f"Version info: {sys.version_info}")


def print_header(str, char='*'):
    """Print a header to help separate print output.

    Parameters
    ----------
    str:
        Text to print in header.
    char:
        The character repeated on next line for pizzaz
    """
    print(f"{str}\n{char*len(str)}\n")


if __name__ == '__main__':
    """Diagnostic of utilities in this module"""
    func1()

    print(get_max_char('~' * 50, 100))
    print(get_max_char('~' * 125, 100))

    a = "test"
    b = 10
    c = list([1, 2, 3])

    print_all(a, b, c)

    print_all(c, b, a, output_mode='!r')

    update_pip()


