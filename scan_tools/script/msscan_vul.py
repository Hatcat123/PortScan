# -*- encoding: utf-8 -*-


import masscan



class MasscanVul():
    def __init__(self,ports):
        self.portdict = []
        self.ports=ports

    def run(self,ip,thread):
        self.masscanresult(ipstr=ip,thread=thread)
        return self.portdict

    def masscanresult(self,ipstr, thread):
        '''
        敏感端口扫描
        :param ipstr:
        :param thread:
        :return:
        '''
        mas = masscan.PortScanner()
        threads = '--max-rate ' + str(thread)
        mas.scan(ipstr,ports=self.ports, arguments=threads)

        for result in mas.scan_result['scan']:
            yuanzu = list(mas.scan_result['scan'].values())
            port = list(yuanzu[0]["tcp"].keys())
            for i in port:
                ipdata = str(i)
                self.portdict.append(ipdata)






if __name__ == '__main__':
    ports = "21,22,23,25,80,161,389,443,445,512,513,514,873,1025,111,1433,1521,5560,7778,2601,2604,3128,3306,3312,3311,3389,4440,5432,5900,5984,6082,6379,7001,7002,7778,8000,8001,8080,8089,8090,9090,8083,8649,8888,9200,9300,10000,11211,27017,27018,28017,50000,50070,50030"
    mv =MasscanVul(ports)
    print(mv.run(ip='47.100.199.115',thread=1000))

