#CyOpSE 

##VM
###user: cyopse
###pass: capstone

##Dependencies:
###Install Bro
sudo apt-get install cmake make gcc g++ flex bison libpcap-dev libgeoip-dev libssl-dev python-dev zlib1g-dev libmagic-dev swig libgoogle-perftools-dev
sudo mkdir -p /nsm/bro
cd ~
wget https://www.bro.org/downloads/bro-2.5.tar.gz
tar -xvzf bro-2.5.tar.gz
cd bro-2.5
./configure --prefix=/nsm/bro
make
sudo make install
export PATH=/nsm/bro/bin:$PATH

Modify Nodes
sudo nano /nsm/bro/etc/node.cfg

Modify IP range
sudo nano /nsm/bro/etc/networks.cfg

Modify MailTo
sudo nano /nsm/bro/etc/broctl.cfg

###Install Broctl
sudo /nsm/bro/bin/broctl
install
exit

Modify:
change deploy.sh to current user directories

Start on system Startup
sudo nano /etc/rc.local
"#" add: /nsm/bro/bin/broctl start

Crontab for maintenance
crontab -e
"#" add: 0-59/5 * * * * /nsm/bro/bin/broctl cron

Ensure Bro is running after restart
tail -f /nsm/bro/logs/current/conn.log
