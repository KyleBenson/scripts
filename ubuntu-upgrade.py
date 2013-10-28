#!/usr/bin/python
from __future__ import print_function
from shutil import copy2

files_to_backup = ['/etc/gnome/defaults.list',
                   '/etc/default/rcS',
                   ]

for f in files_to_backup:
    print("backing up %s" % f)
    copy2(f, f + '.bak')
