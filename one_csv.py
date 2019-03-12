# -*- coding: utf-8 -*-
"""
Author:doom
datetime:2019.2.26
email:408575225@qq.com
function:pdf file change csv file
comment:if you update my code,please update comment as too,thanks
this is format case 12:
format:
    author
    position
    email

"""
import codecs
import re
import csv
import time
import os
import glob
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

# 原pdf文件的初始路径
basic_pdf_file_path = r'C:\Users\Administrator\Desktop\pdf'
# 获取所有的pdf文件
pdf_files = glob.glob("{}/*.pdf".format(basic_pdf_file_path))
# 解析后的txt文件初始路径
basic_txt1_file_path = r'C:\Users\Administrator\Desktop\txt'
# 获取所有的txt文件
txt_files = glob.glob("{}/*.txt".format(basic_txt1_file_path))
# 最终生成的csv文件初始路径
basic_csv_file_path = r'C:\Users\Administrator\Desktop\csv'

def parse_pdf2txt():
    """解析PDF文本，并保存到TXT文件中"""
    count = 0
    for pdf_file in pdf_files:
        try:
            fp = open(pdf_file, 'rb')
            # 解析后的txt文件绝对路径
            txt_file = os.path.join(basic_txt1_file_path, pdf_file.replace(basic_pdf_file_path, "")[1:-4] + ".txt")
            count += 1
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
        except Exception as e:
            print(e)
            continue
        print("第{}个pdf文件转化txt完成".format(count))
        time.sleep(1)


def txt_dealwith_second():
    """将txt文档进行拆分"""
    info_list = []
    # 解析后的csv文件
    txt_file = r'C:\Users\Administrator\Desktop\txt_new\ICPAM 2015.txt'
    with open(txt_file, "r", encoding="utf-8-sig") as fr:
        # 读取整个文件
        src_file = fr.read()
        # print(src_file)
        # 将文件(一个大的字符串)以"ABSTRACT"分割成列表
        result_list = src_file.split("\n\n")
        for result in result_list:
            if "@" in result:
                index_b = result_list.index(result)
                index_e = index_b
                try:
                    while "Abstract" not in result_list[index_e+1]:
                        index_e += 1
                except IndexError:
                    info = result_list[index_b:index_e+1]
                    if "International Conference on Pure and Applied" in info[2]:
                        # print(info)
                        info_list.append(info)
                info = result_list[index_b:index_e+2]
                if "International Conference on Pure and Applied" in info[2]:
                    # print(info)
                    info_list.append(info)
        count = len(info_list)
        for i in range(count):
            try:
                title = "".join(info_list[i][3:5])
                if "1" in info_list[i][4]:
                    title = "".join(info_list[i][3:4])
                    author = info_list[i][4]
                    position = info_list[i][5]
                    email = info_list[i + 1][0]
                    info_first = [title, author, position, email]
                    print(info_first)
                    count_e = info_first[-1].count("@")
                    # case:1(只有一个email)
                    if count_e == 1:
                        title = info_first[0].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                        author = info_first[1].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                        position = info_first[2].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                        email = info_first[-1]
                        result_info = [title, author, position, email]
                        if author and "@" in email:
                            info_list.append(result_info)
                    elif 1 < count_e < 4:
                        count_d = len(info_first[-1].split(","))
                        if count_d > 1:
                            title = info_first[0].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                            author = info_first[1].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                            position = info_first[2].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                            email_ls = info_first[-1].split(",")
                            for z in range(count_d):
                                email = email_ls[z]
                                result_info = [title, author, position, email]
                                if author and "@" in email:
                                    info_list.append(result_info)
                        else:
                            title = info_first[0].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                            author_ls = info_first[1].split(",")
                            position = info_first[2].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                            email_ls = info_first[-1].split("\n")
                            for x in range(len(author_ls)):
                                author = author_ls[x].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                                email = email_ls[x].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                                result_info = [title, author, position, email]
                                if author and "@" in email:
                                    info_list.append(result_info)
                    elif count_e > 3:
                        count_d = len(info_first[-1].split("\n"))
                        title = info_first[0].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                        author_ls = info_first[1].split(",")
                        position = "NA"
                        if len(author_ls) < count_d:
                            author_ls = "".join(info_first[1:3]).split(",")
                        email_ls = info_first[-1].split("\n")
                        for y in range(count_d):
                            author = author_ls[y].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                            email = email_ls[y].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                            result_info = [title, author, position, email]
                            if author and "@" in email:
                                info_list.append(result_info)

                else:
                    author = info_list[i][5]
                    position = info_list[i][6]
                    email = info_list[i + 1][0]
                    info_first = [title, author, position, email]
                    print(info_first)
                    count_e = info_first[-1].count("@")
                    # case:1(只有一个email)
                    if count_e == 1:
                        title = info_first[0].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                        author = info_first[1].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                        position = info_first[2].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                        email = info_first[-1]
                        result_info = [title, author, position, email]
                        if author and "@" in email:
                            info_list.append(result_info)
                    elif 1 < count_e < 4:
                        count_d = len(info_first[-1].split(","))
                        if count_d > 1:
                            title = info_first[0].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                            author = info_first[1].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                            position = info_first[2].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                            email_ls = info_first[-1].split(",")
                            for z in range(count_d):
                                email = email_ls[z]
                                result_info = [title, author, position, email]
                                if author and "@" in email:
                                    info_list.append(result_info)
                        else:
                            title = info_first[0].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                            author_ls = info_first[1].split(",")
                            position = info_first[2].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                            email_ls = info_first[-1].split("\n")
                            for x in range(len(author_ls)):
                                author = author_ls[x].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                                email = email_ls[x].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                                result_info = [title, author, position, email]
                                if author and "@" in email:
                                    info_list.append(result_info)
                    elif count_e > 3:
                        count_d = len(info_first[-1].split("\n"))
                        title = info_first[0].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                        author_ls = info_first[1].split(",")
                        position = "NA"
                        if len(author_ls) < count_d:
                            author_ls = "".join(info_first[1:3]).split(",")
                        email_ls = info_first[-1].split("\n")
                        for y in range(count_d):
                            author = author_ls[y].strip().replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
                            email = email_ls[y]
                            result_info = [title, author, position, email]
                            if author and "@" in email:
                                info_list.append(result_info)
            except IndexError:
                continue
        txt2csv(info_list)
        print("存入csv完成")


def txt2csv(info_list):
    csv_file = r'C:\Users\Administrator\Desktop\csv_new\ICPAM 2015aa.csv'
    """将txt内容写入至csv文件"""
    # 各列标题
    first_line = ["TITLE", "AUTHOR", "POSITION", "EMAIL"]
    # "utf-8"编码还是会有乱码,需使用"utf_8_sig"
    with open(csv_file, 'a', newline="", encoding="utf-8-sig") as csvf:
        # csvf.write(codecs.BOM_UTF8)
        writer = csv.writer(csvf)
        # 添加首行各列标题
        writer.writerow(first_line)
        writer.writerows(info_list)

if __name__ == "__main__":
    txt_dealwith_second()