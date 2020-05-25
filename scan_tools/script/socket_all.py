# -*- encoding: utf-8 -*-

from socket import *
import threading
import queue


class SocketAll():
    def __init__(self):
        self.portdict = []
        self.threads = []
        self.port_queue = queue.Queue()
    def run(self,ip,thread):
        self.portll(ip,thread)
        return self.portdict




    def portll(self,ip,thread):
        setdefaulttimeout(1)
        for i in range(65535):
            self.port_queue.put(i)

        for i in range(thread):

            t = threading.Thread(target=self.portScanner,args=(ip,))
            self.threads.append(t)


        for t in self.threads:
            t.setDaemon(True)
            t.start()
        for q in [self.port_queue]:
                q.join()


    def portScanner(self,host,):
        while True:
            try:
                port = self.port_queue.get()

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
            finally:
                self.port_queue.task_done()

if __name__ == '__main__':
    sa =SocketAll()
    print(sa.run(ip='47.100.199.115',thread=1000))