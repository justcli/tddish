#!/usr/bin/env python3

import os
import sys

_insert_code2 = "\n\
from __future__ import print_function\n\
def _tdd_excepthook(ex, msg, bt):\n\
    global tdd_stderr\n\
    sys.stderr = tdd_stderr\n\
    src = bt.tb_frame.f_code.co_filename\n\
    line = str(bt.tb_lineno)\n\
    m = ex.__name__ + ' exception at line ' + line + ' (Hint :  ' + str(msg) + ' )\\n'\n\
    print(m, file=tdd_stderr)\n\
    exit(1)\n\n\
def tdd(name, condition):\n\
    space = '.' * 64\n\
    space = space.replace('.', 'Test : ' + name, 1)[:64]\n\
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
def err_line(n):\n\
    import os\n\
    global tdd_stderr\n\
    line_nr = 0\n\
    src_file = sys.argv[0]\n\
    src_dir = os.path.dirname(src_file)\n\
    src_file = os.path.basename(src_file)\n\
    tdd_file = src_file\n\
    #src_file = src_file\n\
    src_file = src_file[1:]\n\
    tdd_file = os.path.join(src_dir, tdd_file)\n\
    src_file = os.path.join(src_dir, src_file)\n\
    srch_line = ''\n\
    with open(tdd_file, 'r') as fp:\n\
        while srch_line := fp.readline():\n\
            line_nr += 1\n\
            if line_nr == n:\n\
                break\n\
        if n != line_nr:\n\
            return 0\n\
    line_nr = 0\n\
    with open(src_file, 'r') as fp:\n\
        while line := fp.readline():\n\
            line_nr += 1\n\
            if line.strip() == srch_line.strip():\n\
                return line_nr\n\
    return 0\n\n\
def _tdd_excepthook(ex, msg, bt):\n\
    global tdd_stderr\n\
    sys.stderr = tdd_stderr\n\
    src = bt.tb_frame.f_code.co_filename\n\
    line = str(bt.tb_lineno)\n\
    line = err_line(int(line))\n\
    m = ex.__name__ + ' exception at line ' + str(line) + ' (Hint :  ' + str(msg) + ' )\\n'\n\
    print(m, file=tdd_stderr)\n\
    exit(1)\n\
def tdd(name, condition):\n\
    global tdd_stderr\n\
    space = '.' * 64\n\
    space = space.replace('.', 'Test : ' + name, 1)[:64]\n\
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
    global tdd_stderr\n\
    print(s, file=tdd_stderr)\n\
\n\n"



def _tdd_excepthook(ex, msg, bt):
    global tdd_stderr
    sys.stderr = tdd_stderr
    src = bt.tb_frame.f_code.co_filename
    line = str(bt.tb_lineno)
    m = ex.__name__ + " exception at line " + str(line) +\
        " (Hint :  " + str(msg) + " )\n"
    print(m, file=tdd_stderr)
    exit(1)



if __name__ != '__main__':
    global tdd_stderr
    tdd_stderr = sys.stderr
    sys.stdout = open('.' + os.path.basename(__file__) + '.stdout', 'w')
    sys.stderr = open('.' + os.path.basename(__file__) + '.stderr', 'w')
    sys.excepthook = _tdd_excepthook



def _tddmain():
    """
    The tddish tool does the followings:
    1. Create a temporary file .<your source filename> in the source directory
    2. Copy the source file to the temp file
    3. Remove all commeented tdd code
    4. Change the __name__ to __tdd__ to avoid running main
    Usage:
    tddish {source file to test} [space seperated args in key=val format]
    """
    global tdd_stderr
    _insert_code = ''
    if sys.version_info.major == 2:
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
        tdd_fp = open(tdd_file, 'w+')
    except Exception:
        print('Can not create file (temporary) in ' + src_dir + ' folder.',
              file=sys.stderr)
        exit(1)

    flag = 0
    # pass all the user args to the code in terms of args[]
    i = 2
    code = "import sys\n" +\
            "global __name__\n" +\
            "global tdd_stderr\n" +\
            "__name__ = '__tdd__'\n" +\
            "tdd_stderr = sys.stderr\n" +\
            "args = {}\n"
    code += "sys.stdout = open('" + tdd_file + ".stdout', 'w')\n"
    code += "sys.stderr = open('" + tdd_file + ".stderr', 'w')\n"
    tdd_fp.write(code)
    while i < len(sys.argv):
        key = sys.argv[i].split('=')
        value = key[1]
        key = key[0]
        code = "args['" + key + "'] = " + str(value) + '\n'
        _insert_code += code
        i += 1
    _insert_code += "sys.excepthook = _tdd_excepthook\n"
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
            elif 'from' in  line and 'tddish' in line:
                continue
            elif 'import' in  line and 'tddish' in line:
                continue
            tdd_fp.write(line)
        tdd_fp.flush()

    # the .<> file is ready...run it.
    import subprocess
    if sys.version_info.major == 2:
        cmd = ['python', tdd_file]
    else:
        cmd = ['python3', tdd_file]

    proc = subprocess.Popen(cmd, universal_newlines=True)
    while True:
        if proc.poll() is not None:
            break



if __name__ == '__main__':
    _tddmain()



def tdd(name, condition):
    global tdd_stderr
    space = '.' * 64
    space = space.replace('.', 'Test : ' + name, 1)[:64]
    print(space, end='', file=tdd_stderr)
    if not condition:
        if tdd_stderr.isatty():
            print('\033[91m' + 'failed' + '\033[0m', file=tdd_stderr)
        else:
            print('failed', file=tdd_stderr)
        exit(1)
    if tdd_stderr.isatty():
        print('\033[92m' + 'passed' + '\033[0m', file=tdd_stderr)
    else:
        print('passed', file=tdd_stderr)




def tddump(s:str):
    global tdd_stderr
    print(s, file=tdd_stderr)

