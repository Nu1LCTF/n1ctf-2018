# -*- coding:utf-8 -*-

import win32serviceutil
import win32service
import win32event
import win32process
import sys
import servicemanager
import SocketServer
import subprocess
import string
import random
import os
import re

WORK_DIR = "C:\\ctf\\chall\\"
SOLUTION_DIR = "C:\\collected\\solutions\\"
CAPTURE_DIR = "C:\\ctf\\chall\\captured\\"
FLAG_SERVER = "C:\\ctf\\chall\\server.exe"
SANDBOX = "C:\\ctf\\chall\\sandbox.exe"
HASHCASH = "C:\\ctf\\chall\\hashcash.exe"
SANDBOX_PROFILE = "C:\\ctf\\chall\\sandbox.json"
SIZE_LIMIT = 300 * 1024 * 1024
TIMEOUT = 45
BITS = 30

####################################################################
# Server code
####################################################################

def randstr(length=8):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in xrange(length)])

def gen_challenge():
    return randstr()

def verify(chall, work):
    try:
        hashcash = subprocess.Popen([HASHCASH, "-c", "-b", str(BITS), "-d", "-r", chall, work])
        ret = hashcash.wait()
    except:
        return False
    return ret == 0

def valid(name):
    if len(name) > 40 or len(name) == 0:
        return False
    if not all(ord(c) < 128 for c in name):
        return False
    if re.match("[a-zA-Z0-9]*", name).group() != name:
        return False
    return True

class TRTCPServer(SocketServer.ThreadingMixIn, SocketServer.ThreadingTCPServer):
    pass        

class TRTCPHandler(SocketServer.StreamRequestHandler):
    def read_exact(self, nbytes):
        result = ''
        rem = nbytes 
        while rem:
            result += self.rfile.read(rem)
            rem = nbytes - len(result)
        return result 

    def banner(self):
        req = self.request
        req.sendall("Welcome to this service!\n")
        req.sendall("Default timeout is %d seconds, and will be activated after receiving your PoW.\n" % TIMEOUT)
        req.sendall("After validating your PoW, the server will execute your PE binary.\n")
        req.sendall("Your binary should not exceed the size limit of 300Kb.\n")
        req.sendall("Try to get the flag inside server.exe!\n")
        req.sendall("Since this is an experimental task, ask @shiki7 in IRC if you got into any trouble.\n")

        chall = gen_challenge()
        req.sendall("Please run : \n")
        req.sendall("hashcash -m -b %d %s\n" % (BITS, chall))
        req.sendall("And sends the PoW to us : ")
        try:
            work = self.rfile.readline().strip()
        except Exception:
            req.sendall("I/O Error.\n")
            req.close()
            return False

        if verify(chall, work):
            req.sendall("PoW Ok\n")
        else:
            req.sendall("Invalid PoW\n")
            return False

        req.settimeout(TIMEOUT)
        return True

    def handle(self):
        req = self.request

        if not self.banner():
            req.close()
            return

        req.sendall("Give me your name (your ID our your team ID)\n")
        req.sendall("Alphabet chars or digits only and no longer than 40 chars: ")
        try:
            teamname = self.rfile.readline().strip()
        except Exception:
            req.sendall("I/O error\n")
            req.close()
            return

        if not valid(teamname):
            req.sendall("Invalid name.\n")
            req.sendall("Please use alphabet characters and digits only.\n")
            req.sendall("Make sure your string won't exceed the length limit.\n")
            req.close()
            return

        req.sendall("The byte size of you executable: ")
        try:
            pe_size = long(self.rfile.readline().strip())
        except Exception:
            req.sendall("Invalid input.")
            req.close()
            return

        if pe_size >= SIZE_LIMIT:
            req.sendall("No you don't need such a huge executable.\n")
            req.sendall("Try to reduce the size of your solution.\n")
            req.close()
            return

        if pe_size <= 10:
            req.sendall("No kidding, this is a serious challenge. :)\n")
            req.close()
            return

        req.sendall("Got it, send me exactly %d bytes: " % pe_size)
        try:
            binary = self.read_exact(pe_size)
        except:
            req.sendall("Error when receiving binary.\n")
            req.close()
            return
        
        if not binary.startswith('MZ'):
            req.sendall("Not a valid PE file.\n")
            req.sendall("Try send me some valid executables.\n")
            req.close()
            return

        filename = teamname + '-' + randstr() + '.exe'
        filepath = SOLUTION_DIR + filename
        cappath = CAPTURE_DIR + filename
        try:
            open(filepath, 'wb').write(binary)
            open(cappath, 'wb').write(binary)
        except Exception, ex:
            req.sendall("Error saving solution, contact admin.\n")
            req.sendall("Exception : " + str(ex) + "\n")
            req.close()
            return
        
        # TODO: Secure solution file

        req.sendall("Got it, running your solution...\n")

        try:
            output = subprocess.check_output([SANDBOX, SANDBOX_PROFILE, filepath])
        except Exception, ex:
            req.sendall("Error when executing your binary, please check.\n")
            req.sendall("Exception : " + str(ex) + "\n")
            os.remove(filepath)
            req.close()
            return

        req.sendall("Output : \n")
        req.sendall(output)
        req.close()

        os.remove(filepath)
        return


####################################################################
# Svc code
####################################################################

class ChalServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = 'chalsvc'
    _svc_display_name_ = 'chalsvc'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.flag_server = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        self.flag_server.terminate()
        sys.exit(0)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED,
                (self._svc_name_, ''))
        self.main()
        
    def main(self):
        self.activateFlagServer()
        os.chdir(WORK_DIR)
        server = TRTCPServer(('0.0.0.0', 13337), TRTCPHandler)
        server.allow_reuse_address = True
        server.serve_forever()
        return

    def activateFlagServer(self):
        self.flag_server = subprocess.Popen([FLAG_SERVER])
        return

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(ChalServerSvc)


