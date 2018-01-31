import threading
import requests
import pymysql

conn = pymysql.connect(host='localhost', user='root', passwd='', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute('USE ippool')

def test_ip(prox):
    try:
        r = requests.get('https://www.baidu.com/', proxies={prox})
    except:
        print(prox, ': connect failed')
    else:
        intervaltime = r.elapsed.microseconds
        cur.execute('''INSERT INTO proxypool (proxyip, respontime) VALUES (%s, %s)''',(prox, intervaltime))
        print(prox, ': connect within ', intervaltime, ' s')

ippool = []
with open('./ippools.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        ippool.append(line.strip())
print(ippool)
threadpool = []
for prox in ippool:
    t = threading.Thread(target=test_ip, args=(prox,))
    threadpool.append(t)
    t.start()

for t in threadpool:
    t.join()
