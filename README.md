# CyOpSE 

## VM / Raspberry Pi
##### user: cyopse
##### pass: capstone

## Dependencies:
sudo apt-get install cmake make gcc g++ flex git bison libpcap-dev libssl-dev python-dev swig zlib1g-dev
Install Bro
Copy broctl to bin

## Install Bro
Using http://knowm.org/how-to-install-bro-network-security-monitor-on-ubuntu/
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


#### Modify Nodes
sudo nano /nsm/bro/etc/node.cfg

#### Modify IP range
sudo nano /nsm/bro/etc/networks.cfg

#### Modify MailTo
sudo nano /nsm/bro/etc/broctl.cfg

## Install Broctl
sudo /nsm/bro/bin/broctl
install
exit

## Install Oracle Java 8
Using http://knowm.org/how-to-set-up-the-elk-stack-elasticsearch-logstash-and-kibana/
sudo add-apt-repository -y ppa:webupd8team/java
sudo apt-get update
echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections
echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections
sudo apt-get -y install oracle-java8-installer
java -version

## Install Elasticsearch
cd /var/cache/apt/archives
sudo wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/deb/elasticsearch/2.3.2/elasticsearch-2.3.2.deb
sudo dpkg -i elasticsearch-2.3.2.deb

sudo update-rc.d elasticsearch defaults 95 10
sudo /etc/init.d/elasticsearch restart
OR
sudo systemctl enable elasticsearch
sudo systemctl restart elasticsearch

cd /etc/elasticsearch
sudo nano /etc/elasticsearch/elasticsearch.yml
cd /var/log/elasticsearch

Note: If you want to access your Elasticsearch instance from clients on a different IP address via Javascript, add the following inside elasticsearch.yml:
http.cors.enabled: true
http.cors.allow-origin: "*"

Also note that if you want to access Elasticsearch of any of the plugins like kopf from a host besides local host, you’ll need to add the following to elasticsearch.yml:
network.bind_host: 0

## Kopf Plugin
sudo /usr/share/elasticsearch/bin/plugin install lmenezes/elasticsearch-kopf/v2.1.2

## Integrate Bro IDS with ELK Stack
Using http://knowm.org/integrate-bro-ids-with-elk-stack/
cd /etc/logstash/conf.d/
sudo wget -N https://raw.githubusercontent.com/timmolter/logstash-dfir/master/conf_files/bro/bro-conn_log.conf
sudo wget -N https://raw.githubusercontent.com/timmolter/logstash-dfir/master/conf_files/bro/bro-dns_log.conf
sudo wget -N https://raw.githubusercontent.com/timmolter/logstash-dfir/master/conf_files/bro/bro-files_log.conf
sudo wget -N https://raw.githubusercontent.com/timmolter/logstash-dfir/master/conf_files/bro/bro-http_log.conf
sudo wget -N https://raw.githubusercontent.com/timmolter/logstash-dfir/master/conf_files/bro/bro-notice_log.conf
sudo wget -N https://raw.githubusercontent.com/timmolter/logstash-dfir/master/conf_files/bro/bro-ssh_log.conf
sudo wget -N https://raw.githubusercontent.com/timmolter/logstash-dfir/master/conf_files/bro/bro-ssl_log.conf
sudo wget -N https://raw.githubusercontent.com/timmolter/logstash-dfir/master/conf_files/bro/bro-weird_log.conf
sudo wget -N https://raw.githubusercontent.com/timmolter/logstash-dfir/master/conf_files/bro/bro-x509_log.conf

In the input section, we need to put all paths to the actual Bro log files on OUR system.
In the output section at the end of the config file, we need to push the data to Elasticsearch: elasticsearch { host => localhost }.
In the main filter section, a csv filter is assigned and configured for the bro log. You can hand write the csv filters if you want.
The other filter sections do a few more manipulations to the data and are explained quite well in the comment sections.
Starting Elasticsearch 2.0 it does not support field names with a . (or dot character) in them. Since the bro logs contain fields with dots in their names (id.orig_p), we need to use a filter to convert the dots to underscores. If not you may see an error like: failed to put mappings on indices [[logstash-2016.05.02]], type [bro-conn_log] MapperParsingException[Field name [id.orig_h] cannot contain '.']. The mutate plugin is used to convert the field names containing dots to underscores with the rename command.

## Install logstash-filter-translate

The above logstash config uses a plugin called logstash-filter-translate. The following terminal commands show how to install the logstash-filter-translate plugin. For a more in-depth explanation of installing logstash plugins see How to Install Logstash Plugins for Version 1.5.

cd /opt/logstash
sudo bin/plugin install logstash-filter-translate

sudo -u logstash /opt/logstash/bin/logstash agent -f /etc/logstash/conf.d --configtest

sudo -u logstash /opt/logstash/bin/logstash -f /etc/logstash/conf.d --debug

sudo /etc/init.d/logstash restart

## Modify:
change deploy.sh to current user directories

#### Start on system Startup
sudo nano /etc/rc.local
#add: /nsm/bro/bin/broctl start

#### Crontab for maintenance
crontab -e
#add: 0-59/5 * * * * /nsm/bro/bin/broctl cron

#### Ensure Bro is running after restart
tail -f /nsm/bro/logs/current/conn.log
