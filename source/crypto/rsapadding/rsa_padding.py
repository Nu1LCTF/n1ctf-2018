#!/usr/bin/env python
# -*- coding=utf-8 -*-

from Crypto.Util.number import getPrime, GCD, bytes_to_long
from hashlib import sha256, md5
import random
import signal
import sys, os

signal.alarm(20)

m = b"Welcom to Nu1L CTF, Congratulations, You get flag, and flag is N1CTF{f7efbf4e5f5ef78ca1fb9c8f5eb02635}"
n = 21727106551797231400330796721401157037131178503238742210927927256416073956351568958100038047053002307191569558524956627892618119799679572039939819410371609015002302388267502253326720505214690802942662248282638776986759094777991439524946955458393011802700815763494042802326575866088840712980094975335414387283865492939790773300256234946983831571957038601270911425008907130353723909371646714722730577923843205527739734035515152341673364211058969041089741946974118237091455770042750971424415176552479618605177552145594339271192853653120859740022742221562438237923294609436512995857399568803043924319953346241964071252941
e = 3

def welcom():
    batch = """
 _   _      __ _         _____ _______ ______  
| \ | |    /_ | |       / ____|__   __|  ____| 
|  \| |_   _| | |      | |       | |  | |__    
| . ` | | | | | |      | |       | |  |  __|   
| |\  | |_| | | |____  | |____   | |  | |      
|_| \_|\__,_|_|______|  \_____|  |_|  |_|      

_|_|_|      _|_|_|    _|_|          _|_|_|    _|_|    _|      _|  _|_|_|_|  
_|    _|  _|        _|    _|      _|        _|    _|  _|_|  _|_|  _|        
_|_|_|      _|_|    _|_|_|_|      _|  _|_|  _|_|_|_|  _|  _|  _|  _|_|_|    
_|    _|        _|  _|    _|      _|    _|  _|    _|  _|      _|  _|        
_|    _|  _|_|_|    _|    _|        _|_|_|  _|    _|  _|      _|  _|_|_|_|                        
"""
    print(batch)

def proof():
    strings = "abcdefghijklmnopqrstuvwxyzWOERFJASKL"
    prefix = "".join(random.sample(strings, 6))
    starwith = str(random.randint(10000, 99999))
    pf = """
sha256("%s"+str).hexdigest().startswith("%s") == True
Please give me str
"""%(prefix, starwith)
    print(pf)
    s = input().strip()
    if sha256((prefix+s).encode()).hexdigest().startswith(starwith):
        return True
    else:
        return False

def cmd():
    help = """
1. get code
2. get flag
Please tell me, what you want?
"""
    while True:
        print(help)
        c = input().strip()
        if c == "1":
            return True
        elif c == "2":
            return False
        else:
            print("Enter Error!")

def checktime():
    return os.path.exists("/root/crypto/start")

def main():
    if not checktime():
        print("Hacked by Nu1L")
        return
    if not proof():
        print("Check Failed!")
        return
    welcom()
    if cmd():
        f = open("/root/crypto/file.py")
        print(f.read())
        return
    mm = bytes_to_long(m)
    assert pow(mm, e) != pow(mm, e, n)
    sys.stdout.write("Please give me a padding: ")
    padding = input().strip()
    padding = int(sha256(padding.encode()).hexdigest(),16)
    c = pow(mm+padding, e, n)
    print("Your Ciphertext is: %s"%c)

if __name__ == '__main__':
    try:
        main()
    except:
        os._exit(-1)
    # main()

    

