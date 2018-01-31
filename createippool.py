import requests
from bs4 import BeautifulSoup
import random
import time

urls = ['http://www.kuaidaili.com/free/inha/{}/'.format(str(i)) for i in range(1, 2)]

pool = []
for url in urls:
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    ips = soup.findAll('td', {"data-title": "IP"})
    ports = soup.findAll('td', {"data-title": "PORT"})
    for ip, port in zip(ips, ports):
        s = 'http://'+str(ip.get_text())+':'+str(port.get_text())
        if s in pool:
            continue
        pool.append(s)
    a = random.uniform(10, 15)
    time.sleep(a)

with open('./ippools.txt', 'wt', encoding='utf-8') as fout:
    for proxystring in pool:
        fout.write(proxystring+'\n')