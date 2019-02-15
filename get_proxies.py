# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 10:37:20 2018

@author: xiaojian
此模块为代理大全(免费快代理)
"""
#https://www.kuaidaili.com/free/inha/1
#url=https://www.kuaidaili.com/free/inha/2/
import re,time,random
import requests
from get_user_agent import get_user_agent

def get_proxies():
    base_url="https://www.kuaidaili.com/free/inha/"
    headers=random.choice(get_user_agent())
#    begin_page=int(input("请输入起始页:"))
#    end_page=int(input("请输入终止页:"))
    #起始页
    begin_page=1
    #终止页
    end_page=5
    proxies_list=[]
    while end_page - begin_page >= 1:
        number=0
        #获取页面的html
        url=base_url+str(begin_page)
        timeout=10
        time.sleep(random.randint(1,4))
        resp=requests.get(url,headers=headers,timeout=timeout)
        resp.encoding="utf-8"
        html=resp.text
        #解析html
        pattern=re.compile('<tr>[\s\S]*?"IP">([\s\S]*?)<[\s\S]*?"PORT">([\s\S]*?)<[\s\S]*?"类型">([\s\S]*?)<[\s\S]*?</tr>',re.S)
        result_list=re.findall(pattern,html)
        for result in result_list:
            proxy={
                    result[-1].strip():result[0].strip()+":"+result[1].strip()
                  }
            number += 1
            proxies_list.append(proxy)
        print("第%d页代理ip爬取完成,共有%d条记录"% (begin_page,number))
        begin_page += 1
    print(proxies_list)
    return proxies_list
    
#if __name__ == "__main__":
#    get_proxies()
