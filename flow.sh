#!/bin/bash
{
cd /home/swasher/scriptflow
python flow.py $1
} > /dev/tty1 2> /dev/tty1
