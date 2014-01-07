import os, sys
from __future__ import print_function
'''
A script for getting rid of those annoying renamed files Ubuntu One creates when it thinks there was a conflict...
'''

# we'll check for each possibly renamed file with these numbers
max_rename_number = 10

def rename_files(path_to_walk):
    # find every file in the current directory recursively
    for root, dirs, files in os.walk(path_to_walk):
        # walk through all possible numbers U1 would add to the filename
        for i in range(0,max_rename_number):
            for f in files:
                toreplace = '.%d.' % i
                if toreplace in f:
                    oldname = os.path.join(root, f)
                    newname = oldname.replace(toreplace, '.')
                    os.rename(oldname, newname)
            

if __name__ == '__main__':
    if len(sys.argv) > 1:
        rename_files(sys.argv[1])
    else:
        rename_files(os.getcwd())
