# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 15:29:44 2018

@author: doom
此模块用来模拟公司尾牙抽奖活动

"""


import random

class YearDinner():
    """此类实现简单的抽奖"""
    def __init__(self,ls,first_level_number,second_level_number,third_level_number):
        #员工总是列表
        self.ls=ls
        #一等奖名额数
        self.first_level_number=first_level_number
        #二等奖名额数
        self.second_level_number=second_level_number
        #三等奖名额数
        self.third_level_number=third_level_number
        #一等奖获奖者名单列表
        self.get_first_list=[]
        #二等奖获奖者名单列表
        self.get_second_list=[]
        #三等奖获奖者名单列表
        self.get_third_list=[]
        #阳光普照将获奖者列表
        self.get_normal_list=[]
        #抽奖类型（一，二，三，阳光普照）
        self.level_type=""
        #判断抽奖类型是否重复
        self.flage=[]
        
    
    def choose_level(self):
        """此方法实现抽奖等奖"""
        while True:
            try:
                self.level_type=int(input("请输入抽奖等级('1','2','3')'0'(结束抽奖):"))
                self.flage.append(self.level_type)
            except ValueError as e:
                print("输入不合法:%s"% e)
                continue
            if self.level_type == 1:
                if self.flage.count(1) <= 1:
                    print("一等奖抽奖开始！")
                    self.first_level()
                    print("一等奖抽奖结束")
                    continue
                else:
                    print("一等奖已经抽过了！！")
                    continue
            elif self.level_type == 2:
                if self.flage.count(2) <= 1:
                    print("二等奖抽奖开始！")
                    self.second_level()
                    print("二等奖抽奖结束")
                    continue
                else:
                    print("二等奖已经抽过了！！")
                    continue
            elif self.level_type == 3:
                if self.flage.count(3) <= 1:
                    print("三等奖抽奖开始！")
                    self.third_level()
                    print("三等奖抽奖结束")
                    continue
                else:
                    print("三等奖已经抽过了！！")
                    continue
            elif self.level_type == 4:
                if self.flage.count(4) <= 1:
                    print("阳光普照奖开始！")
                    self.normal_level()
                    print("阳光普照奖结束！")
                    continue
                else:
                    print("阳光普照奖已经抽过了！！")
                    continue
            elif self.level_type == 0:
                print("抽奖结束！！！")
                break
            else:
                print("输入不合法！")
                continue
    
    def first_level(self):
        """一等奖执行方法"""
        for i in range(self.first_level_number):
            prize_people=random.choice(self.ls)
            if prize_people in self.ls:
                #将已获奖员工剔除员工列表
                self.ls.remove(prize_people)
            prize_people_info="工号:"+str(prize_people['工号'])+"  姓名:"+str(prize_people['姓名'])+"  部门:"+str(prize_people['部门'])
#            yield prize_people_info
            print("一等奖中奖人信息:%s"% prize_people_info)
            #将已获奖员工追加至一等奖获奖列表中
            self.get_first_list.append(prize_people_info)
#        for i in self.ls:
#            if i in self.get_first_list:
#                self.ls.remove(i)
        print("抽完一等奖后未中奖人数：%d"% len(self.ls))
        print(self.get_first_list)
        return self.get_first_list
    
    def second_level(self):
        """二等奖执行方法"""
        for i in range(self.second_level_number):
            prize_people=random.choice(self.ls)
            if prize_people in self.ls:
                #将已获奖员工剔除员工列表
                self.ls.remove(prize_people)
            prize_people_info="工号:"+str(prize_people['工号'])+"  姓名:"+str(prize_people['姓名'])+"  部门:"+str(prize_people['部门'])
#            yield prize_people_info
            print("二等奖中奖人信息:%s"% prize_people_info)
            #将已获奖员工追加至二等奖获奖列表中
            self.get_second_list.append(prize_people_info)
#        for i in self.ls:
#            if i in self.get_second_list:
#                self.ls.remove(i)
        print("抽完二等奖后未中奖人数：%d"% len(self.ls))
        print(self.get_second_list)
        return self.get_second_list
    
    def third_level(self):
        """三等奖执行方法"""
        for i in range(self.third_level_number):
            prize_people=random.choice(self.ls)
            if prize_people in self.ls:
                #将已获奖员工剔除员工列表
                self.ls.remove(prize_people)
            prize_people_info="工号:"+str(prize_people['工号'])+"  姓名:"+str(prize_people['姓名'])+"  部门:"+str(prize_people['部门'])
#            yield prize_people_info
            print("三等奖中奖人信息:%s"% prize_people_info)
            #将已获奖员工追加至三等奖获奖列表中
            self.get_third_list.append(prize_people_info)
#        for i in self.ls:
#            if i in self.get_third_list:
#                self.ls.remove(i)
        print("抽完三等奖后未中奖人数：%d"% len(self.ls))
        print(self.get_third_list)
        return self.get_third_list
    
    def normal_level(self):
        """普通奖执行方法"""
        #剩余员工全部为阳光普照奖
        self.get_normal_list=self.ls
        print("剩余未中奖人数有%d人"% len(self.get_normal_list))
        for i in self.get_normal_list:
            prize_people_info="工号:"+str(i['工号'])+"  姓名:"+str(i['姓名'])+"  部门:"+str(i['部门'])
#            yield prize_people_info
            print("阳光普照奖中奖人信息:%s"% prize_people_info)
#        print("抽完阳光普照奖后未中奖人数：%d"% len(self.ls))
        print(self.get_normal_list)
        return self.get_normal_list
            
if __name__ == "__main__":
    while True:
        print("*****尾牙抽奖*****")
        start=input("Start the-end-year dinner?(yes/no):")
        if start == "yes":
            ls=[]
            default_info="6666"
            while True:
                try:
                    count=int(input("输入公司员工的数量:"))
                except ValueError as e:
                    print("输入不合法:%s"% e)
                    continue
                if count > 0:
                    break
                else:
                    print("员工数量不能少于1个！")
                    continue
            for i in range(count): 
                staff_info={'工号':default_info+str(i),'姓名':'aa'+str(i),'部门':'bb',}
                ls.append(staff_info)
#            print(ls)
            while True:
                try:
                    first_level_number=int(input("请输入一等奖名额个数:"))
                except ValueError as e:
                    print("输入不合法:%s"% e)
                    continue
                if first_level_number < 1:
                    print("输入不合法!")
                    continue
                else:
                    break
            while True:
                try:
                    second_level_number=int(input("请输入二等奖名额个数:"))
                except ValueError as e:
                    print("输入不合法:%s"% e)
                    continue
                if second_level_number < 1:
                    print("输入不合法!")
                    continue
                else:
                    break
            while True:
                try:
                    third_level_number=int(input("请输入三等奖名额个数:"))
                except ValueError as e:
                    print("输入不合法:%s"% e)
                    continue
                if third_level_number < 1:
                    print("输入不合法!")
                    continue
                else:
                    break
#            while True:
#                try:
#                    level_type=int(input("请输入level等级('1','2','3'):"))
#                except ValueError as e:
#                    print(e)
#                    continue
#                if (level_type != 1) and (level_type != 2) and (level_type != 3):
#                    print("你的输入有误，请重新输入！")
#                else:
#                    break
            #创建类的实例
            everyone=YearDinner(ls,first_level_number,second_level_number,third_level_number)
            #调用方法
            everyone.choose_level()
            break
        elif start == "no":
            print("活动即将开始，敬请期待！")
            continue
        elif start == "exit" or start == "quit":
            print("本次活动已结束，谢谢！")
            break
        else:
            print("输入不合法，请重新输入！")
            continue
        
        

















