CREATE database nu1lctf;
use nu1lctf;
create table ctf_users (id int PRIMARY KEY AUTO_INCREMENT,username char(100),password char(100),ip char(50),is_admin char(10),allow_diff_ip char(10));
create table ctf_user_signature (id int PRIMARY KEY AUTO_INCREMENT,username char(100),userid int,signature text,mood text);

insert into ctf_users( `username`,`password`,`ip`,`is_admin`,`allow_diff_ip` ) values ( 'admin','2533f492a796a3227b0c6f91d102cc36','127.0.0.1','1','0');
create database flag;
use flag;
create table flag (id int PRIMARY KEY,flag char(120));
INSERT INTO flag VALUES (1,'n1ctf{php_unserialize_ssrf_crlf_injection_is_easy:p}');
CREATE USER 'Nu1L'@'localhost' IDENTIFIED BY 'Nu1Lpassword233334';
grant all privileges on `nu1lctf`.* to 'Nu1L'@'%' identified by 'Nu1Lpassword233334';
