#!/bin/bash

NEW_USER=$2
OLD_USER=$1

sudo bash
cd /home/$OLD_USER
tar cf - . | (cd ../$NEW_USER;tar xf -)
chown -R $NEW_USER:$NEW_USER /home/$NEW_USER
exit
