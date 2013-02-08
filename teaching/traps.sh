#! /bin/bash
## This script serves as an example of how to use traps and interrupts in Linux.
## It will prompt the user for an activity that they need to accomplish,
## and incessantly ask the if they've accomplished it.
##
## The main lesson here is that the temp file in which this activity is stored
## in should be deleted when the user presses Ctrl-C (SIGINT) or sends SIGKILL.
##
## @author: Kyle Benson
##
## Based off "Errors and Signals and Traps (Oh, My!) - Part 2"
## by William Shotts, Jr. (http://www.linuxcommand.org/wss0160.php)
## Adapted for the University of California, Irvine course
## CS 143A - Principles of Operating Systems
## Winter 2013

# Generate a random temporary filename so that users aren't overwriting each
# others' 
TEMP_FILE=/tmp/activity_file.txt

echo "Hello, $USER!"
echo "What task would you like me to remind you about today?"
read

# If the user specified a task,
if 
[ "$REPLY" ]
then
    #store it in the temp file
    echo "$REPLY" > $TEMP_FILE
fi

############ Using traps #################
# Perform program exit housekeeping
function clean_up {
    echo #newline
    echo "Great job on being so productive! Goodbye!"
    rm $TEMP_FILE
    exit
}

trap clean_up SIGINT SIGTERM SIGHUP

##########################################

# Ask the user if they performed the task every 2 seconds
TASK=`cat $TEMP_FILE`
while true
do
    echo "Did you $TASK yet?"
    sleep 2
done
