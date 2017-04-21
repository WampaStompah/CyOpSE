#!/bin/sh
sudo broctl deploy 
sleep 2
wmctrl -s 1
sleep 2
lxterminal -e python /home/cyopse/CyOpSE/Python/CyOpSE_Client.py &

lxterminal -e python /home/cyopse/CyOpSE/Python/CyOpSE_Client2.py &

lxterminal -e python /home/cyopse/CyOpSE/Python/CyOpSE_Client3.py &

sleep 2
wmctrl -s 0
sleep 2

pcmanfm /usr/local/bro/spool/wired
