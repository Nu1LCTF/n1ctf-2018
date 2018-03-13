#!/bin/sh

umask 0077
cd `dirname $0`
tcpdump -G 600 -i eth0 -w /tmp/tcpdump/eatingcms-%Y-%m-%d_%H-%M-%S.pcap 'port 80'