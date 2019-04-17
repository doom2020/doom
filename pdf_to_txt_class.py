# -*- coding: utf-8 -*-
"""
Author:doom
datetime:2019.2.26
email:408575225@qq.com
function:pdf file change txt file
comment:if you update my code,please update comment as too,thanks
this is format case seven:

"""

import time
import os
import glob
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


class ParsePDFtoTXT:
    def __init__(self, src_pdf_path, save_txt_path):
        # 原pdf文件的初始路径(需要根据自己文件路径更改)
        # self.basic_pdf_file_path = r'C:\Users\Administrator\Desktop\pdf_new'
        # 实例对象传两个参数(pdf文件路径)
        self.basic_pdf_file_path = src_pdf_path
        # 获取所有的pdf文件
        self.pdf_files = glob.glob("{}/*.pdf".format(self.basic_pdf_file_path))
        # 解析后的txt文件初始路径(需要根据自己的文件路径更改)
        # self.basic_txt1_file_path = r'C:\Users\Administrator\Desktop\txt_new'
        self.basic_txt_file_path = save_txt_path
        # 文件总数量
        self.file_count = len(self.pdf_files)
        # 解析成功的文件
        self.success_parse_count = 0
        # 解析失败的文件
        self.fail_parse_list = []
        # 解析总共时间
        self.summary_time = 0


    def parse_pdf2txt(self):
        """解析PDF文本，并保存到TXT文件中"""
        for pdf_file in self.pdf_files:
            time_begin = time.time()
            try:
                fp = open(pdf_file, 'rb')
                # 解析后的txt文件绝对路径
                txt_file = os.path.join(self.basic_txt_file_path, pdf_file.replace(self.basic_pdf_file_path, "")[1:-4] + ".txt")
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
                                with open(txt_file, 'a', encoding="UTF-8", errors='ignore') as f:
                                    results = x.get_text()
                                    print(results)
                                    f.write(results + "\n")
                    self.success_parse_count += 1
            except Exception as e:
                print(e)
                print("pdf file>>>:{}解析失败".format(pdf_file))
                self.fail_parse_list.append(pdf_file)
                continue
            time_end = time.time()
            time_use = time_end - time_begin
            self.summary_time += time_use
            time.sleep(1)
        fail_file_count = self.file_count - self.success_parse_count
        ave_time = self.summary_time//self.success_parse_count
        print("一共转了{}个文件，成功了{}个,失败了{}个总用时{}秒，平均用时{}秒".format(self.file_count, self.success_parse_count, fail_file_count, self.summary_time, float(self.summary_time/self.success_parse_count)))
        print(self.fail_parse_list)
        return {"sum_file": self.file_count, "success_file_count": self.success_parse_count, "fail_file_count": fail_file_count, "sum_time": self.summary_time, "ave_time": ave_time, "fail_file_list": self.fail_parse_list }


if __name__ == "__main__":
    parse = ParsePDFtoTXT("src_pdf_path", "save_txt_path")
    parse.parse_pdf2txt()