# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 22:14:40 2018


@author: xiaojian
此模块用来抓取大众点评
婚纱摄影的数据：店名，图片，星级，团购，优惠，评论
http://www.dianping.com/search/keyword/16/0_婚纱摄影(第一页)
http://www.dianping.com/search/keyword/16/0_婚纱摄影/p2(第二页)
"""
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import time
from myLogger import LogHelper
from selenium.common.exceptions import NoSuchElementException

#创建log实例
logger=LogHelper()

#创建操作浏览器对象
#修改user-agent
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11")
#设置无图模式(False)
dcap["phantomjs.page.settings.loadImages"] = True
#driver = webdriver.PhantomJS(desired_capabilities=dcap)
driver = webdriver.Chrome(desired_capabilities=dcap)
#大众点评首页
url='https://www.dianping.com/'
driver.get(url)
logger.writeLog("进入首页成功",level='debug')
#隐式等待
driver.implicitly_wait(4)
driver.save_screenshot('大众点评首页.png')

#点击"你好,请登录"，进入登陆方式选择页
driver.find_elements_by_class_name("item")[2].click()
time.sleep(2)
#print(driver.page_source)
logger.writeLog("进入登录方式选择页成功",level='debug')
driver.save_screenshot("登陆方式选择.png")
time.sleep(2)
#点击账号登录
try:
    #尝试使用xpath找element
    driver.switch_to_frame(driver.find_element_by_xpath('//*[@id="J_login_container"]/div/iframe'))
    driver.find_element_by_xpath("/html/body/div/div[2]/div[5]/span").click()
    driver.switch_to_default_content()
except NoSuchElementException:
    logger.writeLog("xpath查找element失败",level='error')
    #尝试使用class_name查找
    try:
        driver.switch_to_frame(driver.find_element_by_xpath('//*[@id="J_login_container"]/div/iframe'))
        driver.find_element_by_class_name("bottom-password-login").click()
        driver.switch_to_default_content()
    except NoSuchElementException:
        logger.writeLog("class_name查找element失败")
        driver.quit()
        logger.writeLog("查找失败退出",level='error')
else:
    #查早element成功
    logger.writeLog("进入账号登录页成功",level='debug')
    time.sleep(2)
    driver.save_screenshot('账号登录页.png')
    try:
        #账号输入,验证码输入，点击登陆按钮
        driver.switch_to_frame(driver.find_element_by_xpath('//*[@id="J_login_container"]/div/iframe'))
        driver.find_element_by_id("mobile-number-textbox").send_keys('13207123556')
        status=1
        while True:
            if status == 0:
                break
            driver.find_element_by_id("send-number-button").click()
            #注意这里有过期时间，可以在做细化处理
            wait_max_time=10
            while wait_max_time != 0:
                time.sleep(1)
                print("倒计时:%d"% wait_max_time)
                wait_max_time -= 1
            while True:
                result=input("message send you?--(y/n):")
                if result == "y":
                    phone_code=input('请输入手机收到的验证码:')
                    driver.find_element_by_id("number-textbox").send_keys(phone_code)
                    status=0
                    break
                elif result == "n":
                    retry_time=30
                    while retry_time != 0:
                        time.sleep(1)
                        print("请在等待%d秒后重试!"% retry_time)
                        retry_time -= 1
                    break
                else:
                    print("输入有误，请重新输入！")
                    continue

#验证码的处理可以自动识别处理，不需要人为识别
#if driver.find_element_by_id('captcha-textbox'):
#    driver.save_screenshot('验证码.png')
#    nol_code=input('请输入图片验证码:')
#    driver.find_element_by_id('captcha-textbox').send_keys(nol_code)
#else:
#    pass
        time.sleep(2)
        driver.find_element_by_id("login-button-mobile").click()
        driver.switch_to_default_content()
    except NoSuchElementException:
        logger.writeLog("登陆失败",level='error')
        driver.quit()
        logger.removeLog()
    else:
        logger.writeLog("登陆成功",level='debug')
        time.sleep(2)
        driver.save_screenshot('登陆成功后主页面.png')
        #在搜索页中，在搜索框中输入要查找的关键词
        kw=input('请输入搜索关键词(婚纱摄影):')
        driver.find_element_by_id('J-search-input').clear()
        driver.find_element_by_id('J-search-input').send_keys(kw)
        time.sleep(1)
        driver.save_screenshot('输入.png')
#        print(driver.page_source)
        time.sleep(2)
#        js='document.getElementById("J-all-btn").click();'
#        driver.execute_script(js)
#        driver.execute('document.getElementByID("J-all-btn").click()')
        driver.find_element_by_class_name('search-bnt-panel').click()
        
#        eAction = driver.findElement(By.xpath('//*[@id="J-all-btn"]'))
#       ((JavascriptExecutor)driver).executeScript("arguments[0].click();", eAction)
#        driver.find_element_by_xpath('//*[@id="J-all-btn"]').click()
#        driver.find_element_by_id('J-all-btn').submit()
        driver.find_element_by_id('J-all-btn').click()
#        driver.find_element_by_id('J-all-btn').send_keys(Keys.ENTER)
        logger.writeLog("进入婚纱摄影页面成功",level='debug')
        time.sleep(6)
#        print(driver.page_source)
        driver.save_screenshot('婚纱摄影页面.png')
        driver.quit()
        logger.writeLog("程序正常退出",level='debug')
        logger.removeLog()
#正式进入爬取内容页面



































