#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import sys

sys.setrecursionlimit(10000)

f0 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&'\"()*+,-./:;<=>?@[\\]^_`{|}~"
p1 = '1vI{e[8Td]-nQ.7O"bl(jq@<0Vy&Z3~\\ps,aD^;BN9JUoh|CE2_6!G\'rHuf>$S%MxgzKY4`c+WXA5F)mR}#PtL?*=i/:wk'
p2 = 'Bp}i{XU%f$DR\\0<Lx=o"Sl`bz)-e62|&JqFT!(C5yh;@u*.WaZ#Qv,?cr8wEm4_t19PH:j]>[NVMn7YGkK\'^/~OIdsA+3g'
p3 = '_r+#yh[Y)S8aXJwV&jv"o=I(6>pg,f-M]qbN4\'EDKF\\t<3G%|$csPQm}~0@R;uU2z9iWB./HCk!{:Od^ZT7`Anl1e5L*x?'

flag = "N1CTF{did_cmm_helped?1109ef6af4b2c6fc274ddc16ff8365d1}"
name = 'Index'

lengths = []

def solve(n, k):
    if n == 0:
        return f0[k]

    t1s = len(p1)
    t1e = len(p1) + lengths[n - 1]
    t2s = t1e + len(p2)
    t2e = t2s + lengths[n - 1]
    if k < t1s:
        return p1[k]
    elif k >= t1s and k < t1e:
        return solve(n-1, k-t1s)
    elif k >= t1e and k < t2s:
        return p2[k-t1e]
    elif k >= t2s and k < t2e:
        return solve(n-1, k-t2s)
    return p3[k-t2e]

def make(x):
    if x == 0:
        return f0
    return p1 + make(x-1) + p2 + make(x-1) + p3

def main(args):
    for i in xrange(10000):
        if i == 0:
            lengths.append(len(f0))
        else:
            lengths.append(lengths[i-1] * 2 + len(p1 + p2 + p3))

    result = []

    test = False
    if len(args) > 1:
        test = True

    for i in xrange(len(flag)):
        if i < 6:
            low = i * 3
            limit = (i + 1) * 3
        else:
            if not test:
                low = 5000
                limit = 10000
            else:
                low = 5
                limit = 15

        found = False
        while not found:
            depth = random.randrange(low, limit)
            max_length = lengths[depth] & 0x1FFFFFFF
            x = random.randrange(0, max_length)
            while x < max_length:
                if solve(depth, x) == flag[i]:
                    found = True
                    break
                x = x + 1

        result.append(' (%s %d %d)' % (name, depth, x))
    print ',\n'.join(result)
    return

main(sys.argv)
