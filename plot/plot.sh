#!/usr/bin/expect

#if [ -z "$1" ]; then
#    echo "Error: You must provide the IP of the RPi"
#    exit
#fi

set ip [lindex $argv 0];

spawn scp pi@$ip:~/BrickPi/b.log .
expect "assword:"
send "icrsislife2k16\r"
wait
#python plot.py
