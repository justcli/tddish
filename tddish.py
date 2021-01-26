#!/usr/bin/env python3

import os
import sys

_insert_code2 = "\n\
from __future__ import print_function\n\
import sys\n\
global __name__\n\
global tdd_stderr\n\
__name__ = '__tdd__'\n\
tdd_stderr=sys.stderr\n\
global __name__\n\
def tdd(name, condition):\n\
    space = '.' * 64\n\
    space = space.replace('.', 'Test : ' + name, 1)[:64]\n\
    #print('Test : ' + name, end='..........', file=tdd_stderr)\n\
    print(space, end='', file=tdd_stderr)\n\
    if not condition:\n\
        if tdd_stderr.isatty():\n\
            print('\\033[91m' + 'failed' + '\\033[0m', file=tdd_stderr)\n\
        else:\n\
            print('failed', file=tdd_stderr)\n\
        exit(1)\n\
    if tdd_err.isatty():\n\
        print('\\033[92m' + 'passed' + '\\033[0m', file=tdd_stderr)\n\
    else:\n\
        print('passed', file=tdd_stderr)\n\
\n\
def tddump(s:str):\n\
    print(s, file=tdd_stderr)\n\
\n\n"

_insert_code3 = "\n\
import sys\n\
global __name__\n\
global tdd_stderr\n\
__name__ = '__tdd__'\n\
tdd_stderr=sys.stderr\n\
def tdd(name, condition):\n\
    space = '.' * 64\n\
    space = space.replace('.', 'Test : ' + name, 1)[:64]\n\
    #print('Test : ' + name, end='..........', file=tdd_stderr)\n\
    print(space, end='', file=tdd_stderr)\n\
    if not condition:\n\
        if tdd_stderr.isatty():\n\
            print('\\033[91m' + 'failed' + '\\033[0m', file=tdd_stderr)\n\
        else:\n\
            print('failed', file=tdd_stderr)\n\
        exit(1)\n\
    if tdd_stderr.isatty():\n\
        print('\\033[92m' + 'passed' + '\\033[0m', file=tdd_stderr)\n\
    else:\n\
        print('passed', file=tdd_stderr)\n\
\n\
def tddump(s:str):\n\
    print(s, file=tdd_stderr)\n\
\n\n"

global tdd_stderr
def main():
    '''
    The tddish tool does the followings:
    1. Create a temporary file .<your source filename> in the source directory
    2. Copy the source file to the temp file
    3. Remove all commeented tdd code
    4. Change the __name__ to __tdd__ to avoid running main
    Usage:
    tddish {source file to test} [space seperated args in key=val format]
    tddish {source file to test} [gaps=0 touches=2]
    '''
    import stat
    import sys
    from shutil import copyfile
    _insert_code = ''
    if  sys.version_info.major == 2:
        _insert_code = _insert_code2
    else:
        _insert_code = _insert_code3

    if len(sys.argv) < 2:
        print("Target python filename missing.")
        exit(1)
    src_file = sys.argv[1]
    src_dir = os.path.dirname(src_file)
    src_file = os.path.basename(src_file)
    tdd_file = os.path.join(src_dir, '.' + src_file)
    src_file = os.path.join(src_dir, src_file)

    src_fp = tdd_fp = None
    try:
        #copyfile(src_file, tdd_file)
        #src_fp = open(src_file, 'R')
        tdd_fp = open(tdd_file, 'w+')
    except Exception as e:
        print('Can not create file (temporary) in ' + src_dir + ' folder.', file=sys.stderr)
        exit(1)

    flag = 0
    # pass all the user args to the code in terms of args[]
    i = 2
    _insert_code += "args = {}\n"
    while i < len(sys.argv):
        key = sys.argv[i].split('=')
        value = key[1]
        key = key[0]
        code = "args['" + key + "'] = " + str(value) + '\n'
        _insert_code += code
        i += 1
    # emit code to mask stderr
    code = "sys.stdout = open('" + tdd_file + ".stdout', 'w')\n"
    _insert_code += code
    code = "sys.stderr = open('" + tdd_file + ".stderr', 'w')\n"
    _insert_code += code
    tdd_fp.write(_insert_code)

    with open(src_file) as src_fp:
        for line in src_fp:
            if line.startswith('#!'):
                continue
            if line == "'''tddish\n":
                flag = 1
                continue
            elif line == "'''\n" and flag == 1:
                flag = 0
                continue
            tdd_fp.write(line)
        tdd_fp.flush()

    # the .<> file is ready...run it.
    import subprocess
    if  sys.version_info.major == 2:
        cmd = ['python', tdd_file]
    else:
        cmd = ['python3', tdd_file]

    proc = subprocess.Popen(cmd, universal_newlines=True)
    while True:
        if proc.poll() is not None:
            break
if __name__ == '__main__':
    main()
else:
    #__name__ = '__tdd__'
    tdd_stderr=sys.stderr

def tdd(name, condition):
    global tdd_stderr
    print('Test : ' + name, end='..........', file=tdd_stderr)
    if not condition:
        if tdd_stderr.isatty():
            print('\\033[91m' + 'failed' + '\\033[0m', file=tdd_stderr)
        else:
            print('failed', file=tdd_stderr)
        exit(1)
    if tdd_stderr.isatty():
        print('\\033[92m' + 'passed' + '\\033[0m', file=tdd_stderr)
    else:
        print('passed', file=tdd_stderr)

def tddump(s:str):
    global tdd_stderr
    print(s, file=tdd_stderr)











