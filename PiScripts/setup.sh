sudo apt install git
git clone https://github.com/WampaStompah/CyOpSE.git

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


sudo /nsm/bro/bin/broctl
install
exit

sudo add-apt-repository -y ppa:webupd8team/java
sudo apt-get update
echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections
echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections
sudo apt-get -y install oracle-java8-installer
java -version

cd /var/cache/apt/archives
sudo wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/deb/elasticsearch/2.3.2/elasticsearch-2.3.2.deb
sudo dpkg -i elasticsearch-2.3.2.deb

sudo systemctl enable elasticsearch
sudo systemctl restart elasticsearch

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

cd /opt/logstash
sudo bin/plugin install logstash-filter-translate

sudo -u logstash /opt/logstash/bin/logstash agent -f /etc/logstash/conf.d --configtest

sudo /etc/init.d/logstash restart
