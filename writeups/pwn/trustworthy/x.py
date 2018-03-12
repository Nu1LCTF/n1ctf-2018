# -*- coding:utf-8 -*-

import socket
import telnetlib
import struct
import subprocess

HASHCASH = "D:\\Tools\\hashcash\\hashcash.exe"

def get_pow(chall, bits=30):
    output = subprocess.check_output([HASHCASH, "-m", "-b", str(bits), chall])
    result = output.lstrip("hashcash stamp: ")
    return result

def read_until(f, delim='\n'):
    buf = ''
    while not buf.endswith(delim):
        buf += f.read(1)
    return buf

def main():
    s = socket.socket()

    s.connect(('47.96.138.135', 13337))
    #s.connect(('47.75.59.56', 13337))
    f = s.makefile('rw', bufsize=0)

    # pow
    read_until(f, "run : \n")
    x = read_until(f).strip().split(' ')
    chall = x[4]
    bits = int(x[3])
    print "Running PoW %s with %d bits..." % (chall, bits)
    work = get_pow(chall, bits)
    read_until(f, "us : ")
    print work
    f.write(work)

    if not 'Ok' in read_until(f):
        print 'PoW failed... wtf...'
        return

    solution = open('solution.exe', 'rb').read()

    read_until(f, ':')
    f.write('Nu1L\n')
    read_until(f, ':')
    f.write(str(len(solution)) + '\n')
    read_until(f, ': ')
    f.write(solution)

    t = telnetlib.Telnet()
    t.sock = s
    t.interact()
    return

main()
