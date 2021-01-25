#!/usr/bin/env python3
import sys
import os

insert_code2 = "\n\
from __future__ import print_function\n\
import sys\n\
global __name__\n\
global twc_stderr\n\
twc_stderr=sys.stderr\n\
global __name__\n\
def twc(name, condition):\n\
    global twc_stderr\n\
    __name__ = '__twc__'\n\
    print('Test : ' + name, end='..........', file=twc_stderr)\n\
    if not condition:\n\
        if twc_stderr.isatty():\n\
            print('\\033[91m' + 'failed' + '\\033[0m', file=twc_stderr)\n\
        else:\n\
            print('failed', file=twc_stderr)\n\
        exit(1)\n\
    if twc_err.isatty():\n\
        print('\\033[92m' + 'passed' + '\\033[0m', file=twc_stderr)\n\
    else:\n\
        print('passed', file=twc_stderr)\n\
    return True\n\n"

insert_code3 = "\n\
import sys\n\
global __name__\n\
global twc_stderr\n\
twc_stderr=sys.stderr\n\
def twc(name, condition):\n\
    global twc_stderr\n\
    __name__ = '__twc__'\n\
    print('Test : ' + name, end='..........', file=twc_stderr)\n\
    if not condition:\n\
        if twc_stderr.isatty():\n\
            print('\\033[91m' + 'failed' + '\\033[0m', file=twc_stderr)\n\
        else:\n\
            print('failed', file=twc_stderr)\n\
        exit(1)\n\
    if twc_stderr.isatty():\n\
        print('\\033[92m' + 'passed' + '\\033[0m', file=twc_stderr)\n\
    else:\n\
        print('passed', file=twc_stderr)\n\
    return True\n\n"

if __name__ == '__main__':
    '''
    The pytwc tool does the followings:
    1. Create a temporary file .<your source filename> in the source directory
    2. Copy the source file to the temp file
    3. Remove all commeented twc code
    4. Change the __name__ to __twc__ to avoid running main
    Usage:
    pytwc {source file to test} [space seperated args in key=val format]
    pytwc {source file to test} [gaps=0 touches=2]
    '''
    import stat
    import sys
    from shutil import copyfile
    insert_code = ''
    if  sys.version_info.major == 2:
        insert_code = insert_code2
    else:
        insert_code = insert_code3

    src_file = sys.argv[1]
    src_dir = os.path.dirname(src_file)
    src_file = os.path.basename(src_file)
    twc_file = os.path.join(src_dir, '.' + src_file)
    src_file = os.path.join(src_dir, src_file)

    src_fp = twc_fp = None
    try:
        #copyfile(src_file, twc_file)
        #src_fp = open(src_file, 'R')
        twc_fp = open(twc_file, 'w+')
    except Exception as e:
        print('Can not create file (temporary) in ' + src_dir + ' folder.', file=sys.stderr)
        exit(1)

    flag = 0
    # pass all the user args to the code in terms of args[]
    i = 2
    insert_code += "args = {}\n"
    while i < len(sys.argv):
        key = sys.argv[i].split('=')
        value = key[1]
        key = key[0]
        code = "args['" + key + "'] = " + str(value) + '\n'
        insert_code += code
        i += 1
    # emit code to mask stderr
    code = "sys.stdout = open('" + twc_file + ".stdout', 'w')\n"
    insert_code += code
    code = "sys.stderr = open('" + twc_file + ".stderr', 'w')\n"
    insert_code += code
    twc_fp.write(insert_code)

    with open(src_file) as src_fp:
        for line in src_fp:
            if line.startswith('#!'):
                continue
            if line == "'''twc\n":
                flag = 1
                continue
            elif line == "'''\n" and flag == 1:
                flag = 0
                continue
            twc_fp.write(line)
        twc_fp.flush()

    # the .<> file is ready...run it.
    import subprocess
    if  sys.version_info.major == 2:
        cmd = ['python', twc_file]
    else:
        cmd = ['python3', twc_file]

    proc = subprocess.Popen(cmd, universal_newlines=True)
    while True:
        if proc.poll() is not None:
            break








