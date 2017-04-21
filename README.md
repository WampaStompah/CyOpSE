"# CyOpSE" 

VM
user: cyopse
pass: capstone

Dependencies:
sudo apt-get install cmake make gcc g++ flex git bison libpcap-dev libssl-dev python-dev swig zlib1g-dev
Install Bro
Copy broctl to bin

Modify:
deploy.sh to current user directory

Add: 
/home/[user]/CyOpSE/PiScripts/deploy.sh &
to 
/etc/rc.local