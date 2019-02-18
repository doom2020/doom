# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 09:12:26 2018

@author: yuanzj5

"""

import paramiko
import myLogger
import re
import threading
import time
import numpy as np
import matplotlib.pyplot as plt

#1.创建连接对象
def connect_host(host,port,username,password,allow_agent=True,timeout=30,banner_timeout=300):#banner_timeout:服务器接受连接但是ssh守护进程没有及时响应
    """use paramiko connect target windows server and return a connect object"""
    ssh=paramiko.SSHClient()
#    弹出对话框默认yes
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    logger.writeLog("start connect target server",level='info')
    try:
#        1.获取秘钥
#        ssh.connect(host,port=port,username=username,password=password,allow_agent=allow_agent,look_for_keys=True,timeout=timeout,banner_timeout=banner_timeout)
#        2.密码登录(选择第二种方式)
        ssh.connect(host,port=port,username=username,password=password,allow_agent=allow_agent,timeout=timeout,banner_timeout=banner_timeout)
        logger.writeLog("connect target server success",level='info')
        return ssh
    except:
#        需要增加一个递归调用，尝试连接次数(retry_count)
        logger.writeLog("connect target windows server error",level='error')
        return None

#2.获取服务器名
def get_hostname(ssh):
    """get host name"""
    cmd01='hostname'
    retry_number=3
    try:
        while True:
            if retry_number == 0:
                logger.writeLog("get hostname fail",level='error')
                break
            stdin,stdout,stderr=ssh.exec_command(cmd01)
            data01=stdout.read().decode().strip()
            print(data01)
            if data01 == "":
                retry_number -= 1
                logger.writeLog("hostname data is null",level='error')
                continue
            else:
                print("monitor hostname:",data01)
                logger.writeLog("get hostname success",level='info')
                return data01
                break
    except:
        logger.writeLog("get host name error",level='error')
        return None

#3.端口连接数统计
def get_port_counts(ssh):
    """get how many client using this port(default=22) now"""
    cmd02='netstat -na'
    retry_number=3
    try:
        while True:
            if retry_number == 0:
                logger.writeLog("get port counts fail",level='error')
                break
            stdin,stdout,stderr=ssh.exec_command(cmd02)
            data02=(stdout.read().decode('gbk').strip().replace(' ','').replace('\t','').replace('\r','').replace('\n',''))
            print(data02)
            if data02 == "":
                    retry_number -= 1
                    logger.writeLog("port counts data is null",level='error')
                    continue
            else:
                pattern=re.compile('1.*?:22',re.S)
                match_list=re.findall(pattern,data02)
                print(match_list)
                port_count=len(match_list)
                logger.writeLog("get port counts success",level='info')
                print("port connected counts:",port_count)
                return port_count
                break
    except:
        logger.writeLog("get port counts error",level='error')
        return None

#4.cpu使用率
def get_cpu_info(ssh):
    """get the cpu use info"""
    cmd03_1='wmic process get Caption,KernelModeTime,UserModeTime'
    cmd03_2='wmic process get Caption,KernelModeTime,UserModeTime'
    retry_number=3
    try:
        while True:
            if retry_number == 0:
                logger.writeLog("get cpu info fail",level='error')
                break
            stdin,stdout,stderr=ssh.exec_command(cmd03_1)
#            time.sleep(3)
            data03_1=stdout.read().decode().split()
            result_list1=[]
            for data in data03_1:
                try:
                    value=int(data)
                    result_list1.append(value)
                except:
                    continue
            print(result_list1)
#            time.sleep(10)
            stdin,stdout,stderr=ssh.exec_command(cmd03_2)
            data03_2=stdout.read().decode().split()
            result_list2=[]
            for data in data03_2:
                try:
                    value=int(data)
                    result_list2.append(value)
                except:
                    continue
#            result_list=list(filter(lambda x:type(x) == type(1),data03))
            print(result_list2)
            if data03_1 == "" or data03_2 == "":
                retry_number -= 1
                logger.writeLog("get cpu info is null",level='error')
                continue
            else:
                allPorcessTime1=sum(result_list1)
                systemProcessTime1=sum(result_list1[:4])
                allPorcessTime2=sum(result_list2)
                systemProcessTime2=sum(result_list2[:4])
                busyTime=allPorcessTime2-allPorcessTime1
                idleTime=systemProcessTime2-systemProcessTime1
                cpu_use_ratio=100*(busyTime)/(busyTime+idleTime)
                print("cpu use info:",cpu_use_ratio)
                logger.writeLog("get cpu info success",level='info')
                return cpu_use_ratio
    except:
        logger.writeLog("get cpu info error",level='error')
        return None
        
                
##5.内存总量/Gb
#def get_memory_size(ssh):
#    """get memory sum size"""
#    cmd04='wmic memorychip get capacity'
#    retry_number=3
#    try:
#        while True:
#            if retry_number == 0:
#                logger.writeLog("get memory sum size fail",level='error')
#                break
#            stdin,stdout,stderr=ssh.exec_command(cmd04)
#            data04=stdout.read().decode().strip('Capacity')
#            print(data04)
#            if data04 == "":
#                retry_number -= 1
#                logger.writeLog("get memory sum size data null",level='error')
#                continue
#            else:
#                result_list=data04.split()
#                print(result_list)
#                memory_size=float(int(result_list[0])+int(result_list[1]))/1024/1024/1024
#                print("mem total Gb: ",memory_size)
#                logger.writeLog("get memory sum size success",level='info')
#                return memory_size
#                break
#    except:
#        logger.writeLog("get memory size error",level='error')
#        return None
#
##6.内存剩余量/Gb
#def get_memory_surplus(ssh):
#    """get memory surplus"""
#    cmd05='wmic OS get FreePhysicalMemory'
#    retry_number=3
#    try:
#        while True:
#            if retry_number == 0:
#                logger.writeLog("get memory surplus fail",level='error')
#                break
#            stdin,stdout,stderr=ssh.exec_command(cmd05)
#            data05=int(stdout.read().decode().split()[1])
#            print(data05)
#            if data05 == "":
#                logger.writeLog("get memory surplus data null",level='error')
#                retry_number -= 1
#                continue
#            else:
#                memory_surplus=round(float(data05)/1024/1024,4)
#                print("mem free Gb: ",memory_surplus)
#                logger.writeLog("get memory surplus data success",level='info')
#                return memory_surplus
#                break
#    except:
#        logger.writeLog("get memory surplus error",level='error')
#        return None
#
##7.内存使用率
#def get_memory_ratio(ssh):
#    """get memory ratio"""
#    memory_size=get_memory_size(ssh)
#    memory_surplus=get_memory_surplus(ssh)
#    if memory_size == "" or memory_surplus == "":
#        logger.writeLog("memory_szie is null or memory_surplus is null",level='error')
#        return None
#    else:
#        try:
#            data06=round(float((memory_size-memory_surplus))/memory_size,4)
#            print("mem use ratio: ",data06)
#            logger.writeLog("get memory ratio success",level='info')
#            return data06
#        except:
#            logger.writeLog("get memory ratio error",level='error')
#            return None
            
#5.内存总量/Gb
def get_memory_info(ssh):
    """get memory sum size"""
    cmd04='wmic memorychip get capacity'
    retry_number1=3
    try:
        while True:
            if retry_number1 == 0:
                logger.writeLog("get memory sum size fail",level='error')
                break
            stdin,stdout,stderr=ssh.exec_command(cmd04)
            data04=stdout.read().decode().strip('Capacity')
            print(data04)
            if data04 == "":
                retry_number1 -= 1
                logger.writeLog("get memory sum size data null",level='error')
                continue
            else:
                result_list=data04.split()
                print(result_list)
                memory_size=float(int(result_list[0])+int(result_list[1]))/1024/1024/1024
                print("mem total Gb: ",memory_size)
                logger.writeLog("get memory sum size success",level='info')
                # return memory_size
                break
    except:
        logger.writeLog("get memory size error",level='error')
        return None

#6.内存剩余量/Gb
# def get_memory_surplus(ssh):
    """get memory surplus"""
    cmd05='wmic OS get FreePhysicalMemory'
    retry_number2=3
    try:
        while True:
            if retry_number2 == 0:
                logger.writeLog("get memory surplus fail",level='error')
                break
            stdin,stdout,stderr=ssh.exec_command(cmd05)
            data05=int(stdout.read().decode().split()[1])
            print(data05)
            if data05 == "":
                logger.writeLog("get memory surplus data null",level='error')
                retry_number2 -= 1
                continue
            else:
                memory_surplus=round(float(data05)/1024/1024,4)
                print("mem free Gb: ",memory_surplus)
                logger.writeLog("get memory surplus data success",level='info')
                # return memory_surplus
                break
    except:
        logger.writeLog("get memory surplus error",level='error')
        return None

#7.内存使用率
# def get_memory_ratio(ssh):
    """get memory ratio"""
    # memory_size=get_memory_size(ssh)
    # memory_surplus=get_memory_surplus(ssh)
    if memory_size == "" or memory_surplus == "":
        logger.writeLog("memory_szie is null or memory_surplus is null",level='error')
        return None
    else:
        try:
            data06=round(float((memory_size-memory_surplus))/memory_size,4)
            print("mem use ratio: ",data06)
            logger.writeLog("get memory ratio success",level='info')
            return (memory_size,memory_surplus,data06)
        except:
            logger.writeLog("get memory ratio error",level='error')
            return None

#8.磁盘信息,根系统盘C:
def get_disk_info(ssh):
    """get disk info"""
    #cmd07='fsutil volume diskfree c:'
    cmd07='wmic LOGICALDISK get FreeSpace,Size'
    retry_number=3
    #C盘总量
    try:
        while True:
            if retry_number == 0:
                logger.writeLog("get disk info fail",level='error')
                break
            stdin,stdout,stderr = ssh.exec_command(cmd07)
            d7_1=stdout.read().decode().split()
            print(d7_1)
            if d7_1 == "":
                logger.writeLog("get disk info data is null",level='error')
                retry_number -= 1
                continue
            #获取C分区盘总量Gb,获取的数据默认单位是bytes
            data07=round(float(d7_1[3])/1024/1024/1024,4)
            print("C disk total Gb:",data07)
            #获取C分区盘剩余量Gb
            data08=round(float(d7_1[2])/1024/1024/1024,4)
            print("C disk free Gb:",data08)
            #C分区盘使用率
            data09=round((data07-data08)/data07,4)
            print("C disk space use ratio: ",data09)
            logger.writeLog("get disk info success",level='info')
            return (data07,data08,data09)
            break
    except:
        logger.writeLog("get disk info error",level='error')
        return None

#9.获取网络流量信息
def get_network_info(ssh):
    cmd08='netstat -e'
    retry_number=3
    try:
        while True:
            if retry_number == 0:
                logger.writeLog("get network info fail",level='error')
                break
            stdin,stdout,stderr=ssh.exec_command(cmd08)
            d8_1=stdout.read().decode('gbk').split()
            if d8_1 == "":
                logger.writeLog("network info data is null",level='error')
                retry_number -= 1
            #发送的流量累加总计Gb
            data10=round(float(d8_1[5])/1024/1024/1024,4)
            print("send trafic flow Gb: ",data10)
            #接收的流量累加总计
            #net_data2=re.sub('[^\u4e00-\u9fa5]','',d8_3[3])
            data11=round(float(d8_1[4])/1024/1024/1024,4)
            print("recv trafic flow Gb: ",data11)
            
            #发送的数据包累加总数Tcp/ip层
            #发送的数据包累加总数
            data12=round(float(d8_1[8])/1024/1024/1024,4)
            print("send packets: ",data12)
            
            #接收的数据包累计
            data13=round(float(d8_1[7])/1024/1024/1024,4)
            print("recv packets: ",data13)
            return (data10,data11,data12,data13)
            break
    except:
        logger.writeLog("get network info error",level='error')
        return None



if __name__ == "__main__":
    logger = myLogger.LogHelper()
    ssh=connect_host('127.0.0.1',22,'root','123456')
    t1=threading.Thread(target=get_hostname,args=(ssh,))
    t2=threading.Thread(target=get_port_counts,args=(ssh,))
    t3=threading.Thread(target=get_cpu_info,args=(ssh,))
    t4=threading.Thread(target=get_memory_info,args=(ssh,))
#    t4=threading.Thread(target=get_memory_size,args=(ssh,))
#    t5=threading.Thread(target=get_memory_surplus,args=(ssh,))
#    t6=threading.Thread(target=get_memory_ratio,args=(ssh,))
    t7=threading.Thread(target=get_disk_info,args=(ssh,))
    t8=threading.Thread(target=get_network_info,args=(ssh,))
    t_list=[t1,t2,t3,t4,t7,t8]
    for i in t_list:
        i.start()
    for i in t_list:
        i.join()
#    hsot_name=get_hostname(ssh)
#    port_counts=get_port_counts(ssh)
#    cpu_info=get_cpu_info(ssh)
#    memory_info=get_memory_info(ssh)
#    memory_size=get_memory_size(ssh)
#    memory_surplus=get_memory_surplus(ssh)
#    memory_ratio=get_memory_ratio(ssh)
#    disk_info=get_disk_info(ssh)
#    network_info=get_network_info(ssh)
#    now=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
#    print("**********"+now+"***********")
#    print("服务器: ",hsot_name)
#    print("当前端口使用数量: ",port_counts)
#    print("CPU使用率: ",cpu_info)
#    print("内存大小(GB): ",memory_info[0])
#    print("内存剩余(GB): ",memory_info[1])
#    print("内存使用率(GB): ",memory_info[2])
#    print("C盘大小(GB): ",disk_info[0])
#    print("C盘剩余空间(GB): ",disk_info[1])
#    print("C盘使用率(GB): ",disk_info[2])
#    print("发送的流量(GB): ",network_info[0])
#    print("接收的流量(GB): ",network_info[1])
#    print("发送的数据包: ",network_info[2])
#    print("接收的数据包: ",network_info[3])
    ssh.close()
    logger.removeLog()
    
    
    
    
    
    
    
    
    
        
