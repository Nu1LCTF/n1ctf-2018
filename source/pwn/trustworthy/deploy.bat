@echo off

REM This batch script should be run as administrator.
REM Deploy dir : C:\ctf\chall\
REM dependency installed : vc redist 2015 x64, python 2.7.14 amd64, pywin32-221 amd64

REM Create directories
mkdir C:\collected\solutions\
mkdir C:\ctf\chall\captured

REM Creak token
echo "this_is_not_the_flag" > C:\token.txt

REM Create challenge users
net user ctf "super_s3cr3t_p4ssw0rd_nobody_knows!" /add
net user victim "h!_th1s_15_v!ct!m_pwn_me_if_you_c4n" /add

REM disable outbound by default
netsh advfirewall set allprofiles firewallpolicy blockinbound,blockoutbound

REM enable service port
netsh advfirewall firewall add rule name="chalservice" dir=in action=allow protocol=TCP localport=13337

REM Modify ACLs
icacls C:\token.txt /inheritance:d
icacls C:\token.txt /remove:g "Authenticated Users" /remove:g "Users" /grant victim:(RX)

icacls C:\ctf\chall\ /inheritance:d
icacls C:\ctf\chall\ /remove:g "Authenticated Users" /remove:g "Users"

REM Register & run the service
python C:\ctf\chall\service.py install
net start chalsvc


