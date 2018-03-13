FROM andreisamuilik/php5.5.9-apache2.4-mysql5.5

MAINTAINER albertchang <albertchang336@gmail.com>

ADD nu1lctf.tar.gz /app/
RUN apt-get update
RUN apt-get install python2.7 -y
RUN apt-get install tcpdump -y
RUN a2enmod rewrite
COPY a.sql /tmp/a.sql
COPY run.sh /run.sh
COPY tcpdump.sh /root/tcpdump.sh
COPY flag_233333 /flag_233333
RUN mkdir /home/nu1lctf
RUN chmod +x /root/tcpdump.sh
RUN chmod +x /run.sh
RUN chmod 777 /tmp/a.sql
RUN chmod 444 /flag_233333


EXPOSE 80
CMD ["/run.sh"]

