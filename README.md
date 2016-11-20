Silly Flask & IPtables guest portal
===================================

Guest portal is solution to controll access to wireless and ethernet network by login and name or mac address (in this case confirmed mac address).

Workflow:
---------
 - connect your computer or handlet to network managed by __guest portal__ first time
 - after open browser and try to request any web page you receive enroll form
 - after you fill all inputs, the application register your request with your computer's mac address to database and send email to person you filled as grant (this person must be member of organization and must have email in organization domain)
 - when this request arrive to grant's mailbox and they confirm it, your mac address will be allowed in this network
 - after a few minutes you will be able to use network and in future (until you have the same computer) you will can use network without login

 Good idea (in case you use wifi) is encrypt network by WPA to be sure that nobody can stole your mac and use this network.  



Installation
------------
In directory example_conf is everything what you need to start this portal and setup firewall on your router (if anybody pay me for it I'm able to create docker image from it or deploy it to your infrastructure)

 - prepare postgresql server wit table by scheme in enroll.sql and create login and password with grants insert, select, update
 - install nginx and use configuration example from example_conf/nginx.conf
 - install uwsgi,uwsgi-plugin-python3,  Flask, pymysql for python3
 - use uwsgi config from example_conf/uwsgi.ini as example for uwsgi configuration
 - create user portal with home and copy source of this application there
 - start uwsgi and nginx after all configuration was modified to your environment
 - iptables example (Debian 7 without systemd) is in example_conf/firewall.sh, deploy it to gateway for your captive portal (Do it only IF YOU KNOW WHOT ARE YOU DOING!!!)
 - crontab on gateway should be updated by crontab like this
```
*/5 * * * *  root wget https://portal.example.com/get --no-check-certificate -O /etc/network/mac_list && /etc/init.d/firewall restart &> /dev/null
```


If you follow this instructions and modify all configurations to your environment you should see portal enroll formular after you connect to wireless network and opening browser
