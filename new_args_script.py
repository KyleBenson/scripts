#! /usr/bin/python
RON_TRACE_ANALYZER_DESCRIPTION = '''A helper script for analyzing NS3 Resilient Overlay Network simulation traces and visualizing the data.'''
#
# (c) University of California Irvine 2012
# @author: Kyle Benson

import argparse
from os.path import isdir
from os import listdir

##################################################################################
#################      ARGUMENTS       ###########################################
# ArgumentParser.add_argument(name or flags...[, action][, nargs][, const][, default][, type][, choices][, required][, help][, metavar][, dest])
# action is one of: store[_const,_true,_false], append[_const], count
# nargs is one of: N, ?(defaults to const when no args), *, +, argparse.REMAINDER
# help supports %(var)s: help='default value is %(default)s'
##################################################################################
def ParseArgs():

    parser = argparse.ArgumentParser(description=RON_TRACE_ANALYZER_DESCRIPTION,
                                     #formatter_class=argparse.RawTextHelpFormatter
                                     epilog='(*1/N): These arguments will be applied to their respective graphs/groups in the order they are specified in.  If only one argument is given, it will be applied to all the groups.')

    # Input Traces
    parser.add_argument('--files', '-f', type=str, nargs='+',
                        help='''files from which to read trace data''')
