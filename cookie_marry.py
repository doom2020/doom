# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 13:30:07 2018

@author: yuanzj5
使用cookie登录大众点评页面,并抓取相关内容

"""

import requests
import re


class PeopleIdea(object):
    def __init__(self,base_url,headers,proxies,timeout,retry_num):
        self.base_url=base_url
        self.headers=headers
        self.proxies=False
        self.timeout=False
        self.retry_num=False
        self.sum_list=[]
        self.page_number=29
        
    def get_page_url_list(self):
        for page in range(1,self.page_number+1):
            page_url=self.base_url+str(page)
            page_html=requests.get(url=page_url,headers=self.headers)
            html_page=page_html.text
            pattern=re.compile('<li class[\s\S]*?href="([\s\S]*?)"',re.S)
            result_list=re.findall(pattern,html_page)
            result_list.remove('##')
            for result in result_list:
                self.sum_list.append(result)
        return self.sum_list
            
    def get_shop_info(self):
        shop_url_list=self.get_page_url_list()
        for shop_url in shop_url_list:
            shop_html=requests.get(url=shop_url,headers=self.headers)
            html_shop=shop_html.text
        return html_shop
    
    def save_shop_info(self):
        html=self.get_shop_info()
        pass
    
if __name__ == "__main__":
    #请求base_url
    base_url="http://www.dianping.com/search/keyword/16/0_婚纱摄影/p"
    #请求头设置
    headers={
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"utf-8",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Connection":"keep-alive",
            "Cookie":"cy=16; cye=wuhan; _lxsdk_cuid=167b0a404e7c8-01fe8851bb77b1-b781636-e1000-167b0a404e8c8; _lxsdk=167b0a404e7c8-01fe8851bb77b1-b781636-e1000-167b0a404e8c8; _hc.v=face3c4d-b4bc-decc-4427-8fc89783f0a3.1544856798; ctu=4eee497af77e661b865f328b933e000e59c925e49a2fbd8c0aae79429792a6b4; s_ViewType=10; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=167b5814eeb-5eb-f2c-3e6%7C%7C11; lgtoken=05f10e2e6-4335-4cd3-9616-47ff28a71f94; dper=cda4913e3b963247355d96ae7b2b170261e9e0838c10be6ecf7d35f8532438b313dd36793f0f4167e95245cdf1d3e31eb51e7bba12b12251b6c73ac38a3b853a30f23a73f4bcaefdecfa89bd56b8605733f1f4952b95da1365d3c783ae3f7c79; ll=7fd06e815b796be3df069dec7836c3df; ua=13207123556",
            "Host":"www.dianping.com",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
            }

    people_idea=PeopleIdea()
