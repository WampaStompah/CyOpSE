#!/bin/sh
broctl deploy 
sleep 2
wmctrl -s 1
sleep 2
lxterminal -e python /home/cyopse/CyOpSE_Client.py &

lxterminal -e python /home/cyopse/CyOpSE_Client2.py &

lxterminal -e python /home/cyopse/CyOpSE_Client3.py &

#lxterminal -e broctl &

sleep 2
wmctrl -s 0
sleep 2

nautilus /usr/local/bro/spool/wired
