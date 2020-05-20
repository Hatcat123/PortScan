# -*- encoding: utf-8 -*-


import nmap

class NmapScan():
    def __init__(self,model):

        self.model =model

    def run(self,ip,port):
        if self.model=='version-all':
            '''重量级扫描'''
            return self.nmapall(network_prefix=ip, ports=port)
        else:

            return self.nmaptop(network_prefix=ip,ports=port)



    def nmaptop(self,network_prefix,ports):
        '''
        端口扫描：-pn不使用ping值
        :param network_prefix:
        :param ports:
        :return:
        '''
        # try:
        if 1==1:

            nm = nmap.PortScanner()
            scan_raw = nm.scan(hosts = network_prefix,ports=ports,arguments='-sV -Pn')

            if not scan_raw['scan']:
                return []

            return scan_raw['scan'].get(network_prefix).get('tcp')


    def nmapall(self,network_prefix,ports):
        '''
        端口扫描：-pn不使用ping值
        :param network_prefix:
        :param ports:
        :return:
        '''
        # try:
        if 1==1:

            nm = nmap.PortScanner()
            scan_raw = nm.scan(hosts = network_prefix,ports=ports,arguments='-sV  -version-all ')
            print(scan_raw)


            for result in scan_raw['scan'].values():

                for port in list(result["tcp"].keys()):
                    top = str(list(result["addresses"].values())[0]) +':'+str(port)

            return scan_raw['scan'].get(network_prefix).get('tcp')



if __name__ == '__main__':

    ns = NmapScan(model='nmap')
    print(ns.run(ip='127.0.0.2',port='445,3306,3389,8080'))
