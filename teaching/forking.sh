#! /bin/bash
## Simple script to demonstrate PIDs and inheritance of environment variables when forking.

function inf_loop {
    while true
    do
	echo "Process $BASHPID sleeping and VARIABLE is $VARIABLE"
	sleep 3
    done
}

# Executed when child is forked
function child {
    echo "Child PID: $BASHPID, VARIABLE is $VARIABLE"
    echo "Child changing VARIABLE to 30"
    VARIABLE=30
    inf_loop
}

# Executed when Ctrl-C is pressed
function cleanup {
    echo parent killed. stopping child
    # $! gets the PID of the last process we ran in the background
    kill -9 $!
    exit
}

VARIABLE=20

echo "Parent PID: $BASHPID, VARIABLE is $VARIABLE"

(child) &
echo "Child process started"

trap cleanup SIGINT
inf_loop
