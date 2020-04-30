#! /usr/bin/python
from __future__ import print_function
NEW_SCRIPT_DESCRIPTION = '''Description that will appear when help is printed.'''

# @author: Kyle Benson
# (c) Kyle Benson 2016

import argparse
import logging as log
#from os.path import isdir
#from os import listdir
#from getpass import getpass
#password = getpass('Enter password: ')

def parse_args(args):
##################################################################################
#################      ARGUMENTS       ###########################################
# ArgumentParser.add_argument(name or flags...[, action][, nargs][, const][, default][, type][, choices][, required][, help][, metavar][, dest])
# action is one of: store[_const,_true,_false], append[_const], count
# nargs is one of: N, ?(defaults to const when no args), *, +, argparse.REMAINDER
# help supports %(var)s: help='default value is %(default)s'
# Mutually exclusive arguments:
# group = parser.add_mutually_exclusive_group()
# group.add_argument(...)
##################################################################################

    parser = argparse.ArgumentParser(description=NEW_SCRIPT_DESCRIPTION,
                                     #formatter_class=argparse.RawTextHelpFormatter,
                                     #epilog='Text to display at the end of the help print',
                                     #parents=[parent1,...], # add parser args from these ArgumentParsers
                                     # NOTE: for multiple levels of arg
                                     # scripts, will have to use add_help=False
                                     # or may consider using parse_known_args()
                                     )

    parser.add_argument('--files', '-f', type=str, nargs='+',
                        help='''files from which to read trace data''')

    # joins logging facility with argparse
    parser.add_argument('--debug', '-d', type=str, default='info', nargs='?', const='debug',
                        help='''set debug level for logging facility (default=%(default)s, %(const)s when specified with no arg)''')


    return parser.parse_args(args)

# NOTE: using argparse with class constructors can be tricky.  While you may be
# tempted to simply 'unzip' the vars(args) dict into the __init__ args, this
# can cause some difficult situations.  For one, you sometimes need to do more
# than simply store self.arg1 = arg1 (e.g. set logging level from debug).
# You also will run into more issues with using the 'parents' option as one
# constructor won't be able to understand args introduced by the other(s).
# Lastly, this unzipping approach doesn't well-document the class attributes.

# Main
if __name__ == "__main__":

    import sys

    args = parse_args(sys.argv[1:])

    # enables logging for all classes
    log_level = log.getLevelName(args.debug.upper())
    log.basicConfig(format='%(levelname)s:%(message)s', level=log_level)
