#!/bin/sh

/usr/sbin/arp -a | /bin/grep "($1)" | /usr/bin/awk '{print $4}' | sed 's/://g'
