#!/bin/bash
chown www-data:www-data /app -R

if [ "$ALLOW_OVERRIDE" = "**False**" ]; then
    unset ALLOW_OVERRIDE
else
    sed -i "s/AllowOverride None/AllowOverride All/g" /etc/apache2/apache2.conf

    a2enmod rewrite
fi
## close php://filter
sed -i "s/allow_url_fopen = On/allow_url_fopen = Off/g" /etc/php5/cli/php.ini
sed -i "s/allow_url_include = On/allow_url_include = Off/g" /etc/php5/cli/php.ini
sed -i "s/allow_url_fopen = On/allow_url_fopen = Off/g" /etc/php5/apache2/php.ini
# sed -i "s/allow_url_include = On/allow_url_include = off/g" /etc/php5/apache2/php.ini
# initialize database
mysqld_safe --skip-grant-tables&
sleep 5
## change root password
mysql -uroot -e "use mysql;UPDATE user SET password=PASSWORD('Nu1LCTF2018!@#qwe') WHERE user='root';FLUSH PRIVILEGES;"
## restart mysql
service mysql restart
## execute sql file
mysql -uroot -pNu1LCTF2018\!\@\#qwe < /tmp/a.sql
ln -s /usr/bin/python2.7 /bin/python

## change level
cd /app;chown -R root:root .;chmod 777 ./upload_b3bb2cfed6371dfeb2db1dbcceb124d3;

## crontab
(while true;do rm -rf /app/upload_b3bb2cfed6371dfeb2db1dbcceb124d3/*;sleep 5;done)&
## rm sql
cd /tmp/
rm a.sql

## clean danger 
rm -rf /var/www/phpinfo
sed -i "s/;session.upload_progress.enabled = On/session.upload_progress.enabled = Off/g" /etc/php5/cli/php.ini
sed -i "s/;session.upload_progress.enabled = On/session.upload_progress.enabled = Off/g" /etc/php5/apache2/php.ini

cd /etc/php5/apache2/conf.d/
rm 20-xdebug.ini
rm 20-memcached.ini
rm 20-memcache.ini

## start cron
cron

source /etc/apache2/envvars
tail -F /var/log/apache2/* &
exec apache2 -D FOREGROUND
service apache2 start
