#!/usr/bin/python

from os import *
import sys
import subprocess

def extract(target_dir):
    
    #for root, dirs, files in walk('sources/'):
    files = listdir(target_dir)

    #for all the full filenames
    for f in [path.join(target_dir, fname) for fname in files]:
        if path.isdir(f):
            continue

        #do this first to get just UCINetID
        new_filename = f.split('_')[0] + '.' + f.split('.')[-1]
        rename(f, new_filename)
        f = new_filename

        if f.endswith('.zip'):
            command = 'unzip %s -d %s' % (f, f.split('.')[0])
            print command
            subprocess.call(command, shell=True)

extract('sources')
