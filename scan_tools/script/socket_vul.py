# -*- encoding: utf-8 -*-

from socket import *
import threading


class SocketVul():
    def __init__(self, ports):
        self.portdict = []
        self.threads = []
        self.ports = ports

    def run(self, ip):
        self.portll(ip)
        return self.portdict

    def portll(self, ip):
        setdefaulttimeout(1)
        portList = ["21", "22", "23", "80", "161", "389", "443", "445", "512", "513", "514", "873", "1025", "111",
                    "1433",
                    "1521", "5560", "7778", "2601", "2604", "3128", "3306", "3312", "3311", "3389", "4440", "5432",
                    "5900",
                    "5984", "6082", "6379", "7001", "7002", "7778", "8000", "8001", "8080", "8089", "8090", "9090",
                    "8083",
                    "8649", "8888", "9200", "9300", "10000", "11211", "27017", "27018", "28017", "50000", "50070",
                    "50030"]
        for p in self.ports.split(','):
            # p= int(p)
            t = threading.Thread(target=self.portScanner, args=(ip, p))
            self.threads.append(t)
            t.start()

        for t in self.threads:
            t.join()

    def portScanner(self, host, port):
        try:
            port = int(port)
            s = socket(AF_INET, SOCK_STREAM)
            s.settimeout(1)
            result = s.connect((host, port))
            if result:
                print("ok")
            else:
                portname = str(port)
                self.portdict.append(portname)
            s.close()
        except Exception as e:
            pass
            # print(e)


if __name__ == '__main__':
    '''
    高风险端口多线程扫描
    '''
    ports = "21,22,23,80,161,389,443,445,512,513,514,873,1025,111,1433,1521,5560,7778,2601,2604,3128,3306,3312,3311,3389,4440,5432,5900,5984,6082,6379,7001,7002,7778,8000,8001,8080,8089,8090,9090,8083,8649,8888,9200,9300,10000,11211,27017,27018,28017,50000,50070,50030"

    sv = SocketVul(ports)
    print(sv.run(ip='47.100.199.115'))
