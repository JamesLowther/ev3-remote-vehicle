#!/bin/bash

scp *.py requirements.txt james@vps.jameslowther.com:~/ev3-server
scp -r web james@vps.jameslowther.com:~/ev3-server
