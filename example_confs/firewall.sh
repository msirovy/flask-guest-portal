#!/bin/sh
#
# Firewall iptables service EXAMPLE to manage firewall
# on guest portall router.
#


IPT="/sbin/iptables"
WAN="eth0"
DENY=5
CAPTIVE_PORTAL="10.10.0.1"

OUT1_NAT="17.2.1.2"     # EDU
OUT2_NAT="17.2.1.27"    # GUEST

do_stop() {
	# CLEAN ALL
	echo -n "Stoping service... "
	$IPT -F
	$IPT -X
	$IPT -t nat -F
	$IPT -t nat -X
	$IPT -t mangle -F
	$IPT -t mangle -X
	$IPT -P INPUT ACCEPT
	$IPT -P OUTPUT ACCEPT
	$IPT -P FORWARD ACCEPT
	echo "OK"
}

do_start() {
	echo "Starting service..."
	echo 1 > /proc/sys/net/ipv4/ip_forward
	echo 0 > /proc/sys/net/netfilter/nf_conntrack_tcp_loose

FZU_NETS="147.231.26.0/23 147.231.126.0/23 10.0.0.0/8"
	echo -n "LIST HTTP... "
	$IPT -N HTTP
	$IPT -A HTTP -s 147.231.11.0/26 -p tcp -j ACCEPT
	$IPT -A HTTP -s 147.231.19.178/32 -p tcp -j ACCEPT
	$IPT -A HTTP -s 147.231.26.0/23 -p tcp -j ACCEPT
	$IPT -A HTTP -s 147.231.126.0/23 -p tcp -j ACCEPT
	$IPT -A HTTP -s 10.0.0.0/8 -p tcp -j ACCEPT
	echo "OK"

	echo -n "LIST SSH... "
	$IPT -N SSH
	$IPT -A SSH -s 10.26.2.0/24 -p tcp -m comment --comment "JEN PRO TESTY" -j ACCEPT
	echo "OK"

	echo -n "LIST MONITORING... "
	$IPT -N MONITORING
	$IPT -A MONITORING -s 17.2.1.10/32 -p tcp -m comment --comment "node2" -j ACCEPT
	$IPT -A MONITORING -s 17.1.7.20/32 -p tcp -m comment --comment "node1" -j ACCEPT
	echo "OK"

	echo -n " INPUT... "
	$IPT -A INPUT -i lo -j ACCEPT
	$IPT -A INPUT -m state --state INVALID -j DROP
	$IPT -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
	$IPT -A INPUT -p icmp -j ACCEPT
	$IPT -A INPUT -p tcp -m pkttype --pkt-type broadcast -j DROP
	$IPT -A INPUT -p tcp -m pkttype --pkt-type multicast  -j DROP
	$IPT -A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -m limit --limit 20/min -j SSH
	$IPT -A INPUT -p tcp -m state --state NEW --dport 5666 -j MONITORING
	$IPT -A INPUT -p tcp -m state --state NEW --dport 4949 -j MONITORING
	$IPT -A INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j HTTP
	$IPT -A INPUT -p tcp -m state --state NEW -m tcp --dport 443 -j HTTP
	$IPT -A INPUT -p udp -m udp --dport 123 -j ACCEPT
	$IPT -A INPUT -p udp -m udp --dport 67 -j ACCEPT
	$IPT -A INPUT -p tcp -m limit --limit 20/min -j LOG --log-prefix "DROP: "
	$IPT -A INPUT -p tcp -j DROP
	echo "OK"

	echo -n " MANGLE... "
	$IPT -N internet -t mangle
	$IPT -t mangle -A PREROUTING -s 10.10.0.0/24 -j internet
	for mac in `cat /etc/network/mac_list | grep -v "^#"`; do
		$IPT -t mangle -A internet -m mac --mac-source $mac -j RETURN
	done
	$IPT -t mangle -A internet -j LOG --log-level 4 --log-prefix "MARK AS DENY: " -m limit --limit 10/min
	$IPT -t mangle -A internet -j MARK --set-mark $DENY
	echo "OK"

	echo -n " Captive portal redirection..."
	$IPT -t nat -A PREROUTING -p TCP -s 10.10.0.0/24 --dport 443 -m mark --mark $DENY -j DNAT --to-destination $CAPTIVE_PORTAL:443
	$IPT -t nat -A PREROUTING -p TCP -s 10.10.0.0/24 -m mark --mark $DENY -j DNAT --to-destination $CAPTIVE_PORTAL:80
	echo "OK"

	echo -n " FORWARD... "
	# LOG NEW CONNECTIONS as NEW-CONN
	$IPT -A FORWARD -j LOG -m state --state NEW --log-level 4 --log-prefix "NEW-CONN: " -m limit --limit 1/s
	#$IPT -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT
	#$IPT -A FORWARD -m mark --mark $DENY -j DROP
	#$IPT -A FORWARD -j ACCEPT
	echo "OK"


	echo -n " SNAT... "
	$IPT -t nat -A POSTROUTING -s 10.10.0.0/24 -o $WAN -j SNAT --to $OUT2_NAT
	#$IPT -t nat -A POSTROUTING -s NOVA_SIT -o $WAN -j SNAT --to $NOVA_ODCHOZI_IP
	echo "OK"
}


# UI
case "$1" in
	start)
		do_stop
		do_start
		;;

	stop)
		do_stop
		;;

	restart)
		# stejne jako start
		do_stop
		do_start
		;;

	*)
		echo "Right syntax is $0 start|stop|restart"
		exit 1
		;;
esac
