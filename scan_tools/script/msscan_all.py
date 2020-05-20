# -*- encoding: utf-8 -*-


import masscan


class MasscanAll():
    def __init__(self):
        self.portdict = []

    def run(self, ip, thread):
        self.masscanresult(ip, thread)
        return self.portdict

    def masscanresult(self, ipstr, thread):
        mas = masscan.PortScanner()
        threads = '--max-rate ' + str(thread)
        mas.scan(ipstr, ports='1-65535', arguments=threads)
        for result in mas.scan_result['scan']:
            yuanzu = list(mas.scan_result['scan'].values())
            port = list(yuanzu[0]["tcp"].keys())
            for i in port:
                ipdata = str(i)
                self.portdict.append(ipdata)


if __name__ == '__main__':
    ma = MasscanAll()
    ma.run(ip='47.100.199.115', thread=1000)
