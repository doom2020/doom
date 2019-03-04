"""
Author:doom
datetime:2019.2.26
email:408575225@qq.com
github:doom2020
function:txt file change to csv file
comment:if you update my code,please update comment as too,thanks
"""



import csv
import os





class DealwithTXT:
    """this class parse the pdf file to csv file"""
    def __init__(self):
        # parsed txt file init path
        self.basic_txt_file_path = r'C:\Users\Administrator\Desktop\txt'
        # file name
        self.file_name = 'aaa.txt'
        # txt file
        self.txt_file = os.path.join(self.basic_txt_file_path, self.file_name)
        # parsed csv file init path
        self.basic_csv_file_path = r'C:\Users\Administrator\Desktop\csv'

    def txt_dealwith_split(self):
        """this method:split the txt file use your format"""
        # init info_list
        info_list = []
        # use pdf_file name to get txt_file name
        csv_file = os.path.join(self.basic_csv_file_path, self.txt_file.replace(self.basic_txt_file_path, "")[1:-4] + ".csv")
        with open(self.txt_file, "r", encoding="UTF-8") as fr:
            # read all file
            src_file = fr.read()
            # use src_file(a big str) split list by 'ABSTRACT'(keyword,need yourself analyze)
            result_list = src_file.split("ABSTRACT")
            # use list method of slice delete the last element(need yourself analyze)
            for result in result_list[:-1]:
                # use '/n/n' to split data then use slice get data that you need(need yourself analyze)
                data_list = result.split("\n\n")[-4:-1]
                print(data_list)
                # callback function get_title()
                title = self.get_title(data_list)
                # callback function get_author()
                author = self.get_author(data_list)
                # callback function get_position()
                position = self.get_position(data_list)
                # callback function get_email()
                email = self.get_email(data_list)
                info = [title, author, position, email]
                info_list.append(info)
            # callback function txt2csv()
            self.txt2csv(info_list, csv_file)

    def get_title(self, data_list):
        """this method:get article title(str type) and delete '\n'"""
        if len(data_list) == 2:
            try:
                title = data_list[0].replace("\n", "")
            except IndexError:
                title = "NA"
                return title
            return title
        if len(data_list) == 3:
            try:
                title = data_list[1].replace("\n", "")
            except IndexError:
                title = "NA"
                return title
            return title

    def get_author(self, data_list):
        """this method:get article author name(many author name set,type str)"""
        if len(data_list) == 2:
            try:
                author_str = data_list[1].split('\n')[0]
            except IndexError:
                author_str = "NA"
                return author_str
            return author_str
        if len(data_list) == 3:
            try:
                author_str = data_list[2].split('\n')[0]
            except IndexError:
                author_str = "NA"
                return author_str
            return author_str

    def get_position(self, data_list):
        """this method:get article author's position"""
        if len(data_list) == 2:
            try:
                position = "".join(("".join(data_list[1].split('\n')[1:])).split(";")[:-1])
            except IndexError:
                position = "NA"
                return position
            return position
        if len(data_list) == 3:
            try:
                position = "".join(("".join(data_list[2].split('\n')[1:])).split(";")[:-1])
            except IndexError:
                position = "NA"
                return position
            return position

    def get_email(self, data_list):
        if len(data_list) == 2:
            try:
                email = ("".join(data_list[1].split('\n')[1:])).split(";")[-1]
            except IndexError:
                email = "NA"
                return email
            return email
        if len(data_list) == 3:
            try:
                email = ("".join(data_list[2].split('\n')[1:])).split(";")[-1]
            except IndexError:
                email = "NA"
                return email
            return email

    def txt2csv(self, info_list, csv_file):
        """this method:read txt file writer to csv file"""
        # colspan name
        first_line = ["TITLE", "AUTHOR", "POSITION", "EMAIL"]
        # use 'utf-8' is not valid,just try use 'utf_8_sig'
        with open(csv_file, 'a', newline="", encoding="utf_8_sig") as csvf:
            writer = csv.writer(csvf)
            # add first row the colspan name
            writer.writerow(first_line)
            writer.writerows(info_list)


if __name__ == "__main__":
    # create instance for class
    pdf_obj = DealwithTXT()