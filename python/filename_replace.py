#!/usr/bin/python
from __future__ import print_function

usage = '''
Usage: filename_replace.py from to [dir]
Walks through the possibly specified directory ($PWD by default), dir, recursively and replaces occurrences of 'from' in the filenames/dirnames with the string 'to'.
Useful for changing file extensions.
'''

import os, sys

def rename_files(from_pattern, to_pattern, path_to_walk):
    # find every file in the current directory recursively
    for root, dirs, files in os.walk(path_to_walk):
        # walk through all possible numbers U1 would add to the filename
        for f in files + dirs:
            if from_pattern in f:
                newname = os.path.join(root, f.replace(from_pattern, to_pattern))
                os.rename(os.path.join(root, f), newname)

                if not os.path.exists(newname):
                    print('error renaming file!')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Not enough arguments!\n%s' % usage)
    elif len(sys.argv) > 3:
        rename_files(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        rename_files(sys.argv[1], sys.argv[2], os.getcwd())
