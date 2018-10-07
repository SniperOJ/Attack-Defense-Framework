#!/bin/bash

python watch.py $*
if [ $? -eq 255 ]
then
    exit $?
else
    while [ $? -ne 0 ]
    do
        echo "Process exits with errors! Restarting!"
        python watch.py $*
    done
fi
echo "Process ends!"


