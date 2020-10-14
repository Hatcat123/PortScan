# -*- encoding: utf-8 -*-

from socket import *
import threading



class SocketAll():
    def __init__(self):
        self.portdict = []
        self.threads = []
    def run(self,ip):
        self.portll(ip)
        return self.portdict




    def portll(self,ip):
        setdefaulttimeout(1)
        for i in range(65535):
            t = threading.Thread(target=self.portScanner,args=(ip,i))
            self.threads.append(t)
            t.start()

        for t in self.threads:
            t.join()

    def portScanner(self,host,port):
        try:
            port = int(port)
            s = socket(AF_INET,SOCK_STREAM)
            s.settimeout(1)
            result = s.connect((host,port))
            if result:
                pass
            else:
                portname = str(port)
                self.portdict.append(portname)
            s.close()
        except:
            pass

if __name__ == '__main__':
    sa =SocketAll()
    print(sa.run(ip='47.100.199.115'))