# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 19:07:01 2019
运行环境：python3.71
安装依赖包：pip install pdfminer3k
@author: yuanzj5
"""


import re
import csv
import os
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

# 文件的初始路径
basic_file_path = 'C://Users//yuanzj5//Desktop//'
# pdf文件绝对路径
pdf_file = os.path.join(basic_file_path, 'EAPRIL 2016.pdf')
# 解析后的txt文件绝对路径
txt_file = os.path.join(basic_file_path, 'first.txt')
# 再次处理后的txt文件绝对路径
txt_file_filter = os.path.join(basic_file_path, 'second.txt')
# 最终生成的csv文件
csv_file = os.path.join(basic_file_path, 'info_new.csv')

def parse_pdf2txt():
    """解析PDF文本，并保存到TXT文件中"""
    fp = open(pdf_file, 'rb')
    # 用文件对象创建一个PDF文档分析器
    parser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器，与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)

    # 提供初始化密码，如果没有密码，就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDF，资源管理器，来共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释其对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page内容
        # doc.get_pages() 获取page列表
        for page in doc.get_pages():
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            # 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    # 文件有特殊的字符(貌似德文。。)要做编码处理
                    with open(txt_file, 'a', encoding="UTF-8") as f:
                        results = x.get_text()
                        print(results)
                        f.write(results + "\n")

def txt_dealwith_first():
    """将转化为txt档文件进一步处理,去掉特殊字符"""
    with open(txt_file, "r", encoding="UTF-8") as fr:
        with open(txt_file_filter, 'w', encoding="UTF-8") as fw:
            for line in fr.readlines():
                    if "!" in line or "EAPRIL'Conference'Proceedings''2016'" in line:
                        continue
                    print(line)
                    fw.write(line)

def txt_dealwith_second():
    """将处理过的txt文档进行拆分"""
    with open(txt_file_filter, "r", encoding="UTF-8") as fr:
        # 读取整个文件
        src_file = fr.read()
        # 将文件(一个大的字符串)以"ABSTRACT"分割成列表
        result_list = src_file.split("ABSTRACT")
        # 切片去掉最后一个无关元素
        for result in result_list[:-1]:
            # 以空行分割数据,并切片获取需要的数据
            data_list = result.split("\n\n")[-4:-1]
            txt2csv(data_list)

def get_title(data_list):
    # 获取文章标题(字符串),去掉换行符
    title = data_list[0].replace("\n", "")
    return title

def get_author(data_list):
    # 获取作者的姓名(多个作者名字的字符串),去掉"*"
    title = get_title(data_list)
    if ("FAMILY - SCHOOL COOPERATION" in title) or ("THE CURSE OF DROPOUT" in title) or \
            ("PROJECT-BASED LEARNING AND" in title) or ("WHERE IS THE LINK BETWEEN DIRECT" in title):
        author_str = data_list[2].replace("*", "")
    else:
        author_str = data_list[1].replace("*", "")
        # 将多个作者姓名拆分
    author_list = author_str.split(",")
    return author_list

def get_position_and_email(data_list):
    position_list = []
    email_list = []
    # 获取所有作者的职位和邮箱,去掉换行符
    title = get_title(data_list)
    if ("FAMILY - SCHOOL COOPERATION" in title) or ("THE CURSE OF DROPOUT" in title) or \
            ("PROJECT-BASED LEARNING AND" in title) or ("WHERE IS THE LINK BETWEEN DIRECT" in title):
        all_position_and_email_list = data_list[1].replace("\n", "").split("*")
    else:
        all_position_and_email_list = data_list[2].replace("\n", "").split("*")
    # print(all_position_and_email_list)
    if len(all_position_and_email_list) == 2:
        position = all_position_and_email_list[1][:-1]
        email = all_position_and_email_list[1][-1]
        position_list.append(position)
        email_list.append(email)
    if len(all_position_and_email_list) == 1:
        position = all_position_and_email_list[0][:-1]
        email = all_position_and_email_list[0][-1]
        position_list.append(position)
        email_list.append(email)
    for i in all_position_and_email_list:
        # print(len(i))
        # 去掉空的元素
        if len(i) == 0:
            continue
        # 获取每个作者的职位和邮箱
        position_and_email_list = i.split(",")
        # print(position_and_email_list)
        # 判断邮箱所在的位置进行分割
        for e in position_and_email_list:
            if "@" in e:
                # 获取邮箱元素索引
                index = position_and_email_list.index(e)
                # 获取邮箱
                email = position_and_email_list[index]
                # 获取职位
                position = ",".join(position_and_email_list[:index])
                position_list.append(position)
                email_list.append(email)
    return (position_list, email_list)

def txt2csv(data_list):
    """将txt内容写入至csv文件"""
    # 各列标题
    first_line = ["TITLE", "AUTHOR", "POSITION", "EMAIL"]
    all_data_list = []
    # "utf-8"编码还是会有乱码,需使用"utf_8_sig"
    with open(csv_file, 'a', newline="", encoding="utf_8_sig") as csvf:
        writer = csv.writer(csvf)
        title = get_title(data_list)
        author_list = get_author(data_list)
        position_email_tuple = get_position_and_email(data_list)
        for i in range(len(author_list)):
            try:
                ls = [title, author_list[i], position_email_tuple[0][i], position_email_tuple[1][i]]
            except IndexError:
                continue
            all_data_list.append(ls)
        writer.writerows(all_data_list)

if __name__ == "__main__":
    parse_pdf2txt()
    txt_dealwith_first()
    txt_dealwith_second()
