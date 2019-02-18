from socket import *
import os
import sys
from myLogger import LogHelper
import re


def main_client():
    if len(sys.argv) < 3:
        sys.exit('输入有误')
    sockfd = socket()
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST, PORT)
    sockfd.connect(ADDR)
    try:
        while True:
            data = sockfd.recv(1024).decode()
            # pattern=re.compile(r'.*?.(.*?)',re.S)
            # result=re.findall(pattern,data)
            # print(result[0])
            # print(result)
            if data == "":
                sys.exit('服务器端异常')
            if data[-3:] == "txt":
                logger.writeLog(data, level='error')
            logger.writeLog(data, level='info')
    except KeyboardInterrupt:
        sockfd.close()
        sys.exit('正常退出')


if __name__ == "__main__":
    logger = LogHelper()
    main_client()