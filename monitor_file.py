"""此模块用来实时监控在ftp共享服务器上上传的文件"""
from watchdog.observers import Observer
from watchdog.events import *
from socket import *
import time
import sys

class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
            connfd.send("directory moved from {0} to {1}".format(event.src_path, event.dest_path).encode())
        else:
            print("file moved from {0} to {1}".format(event.src_path, event.dest_path))
            connfd.send("file moved from {0} to {1}".format(event.src_path, event.dest_path).encode())

    def on_created(self, event):
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
            connfd.send("directory created:{0}".format(event.src_path).encode())
        else:
            print("file created:{0}".format(event.src_path))
            connfd.send("file created:{0}".format(event.src_path).encode())

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
            connfd.send("directory deleted:{0}".format(event.src_path).encode())
        else:
            print("file deleted:{0}".format(event.src_path))
            connfd.send("file deleted:{0}".format(event.src_path).encode())

    def on_modified(self, event):
        if event.is_directory:
            print("directory modified:{0}".format(event.src_path))
            connfd.send("directory modified:{0}".format(event.src_path).encode())
        else:
            print("file modified:{0}".format(event.src_path))
            connfd.send("file modified:{0}".format(event.src_path).encode())

if __name__ == "__main__":
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    HOST = '127.0.0.1'
    PORT = 6666
    ADDR = (HOST, PORT)
    sockfd.bind(ADDR)
    sockfd.listen(10)
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, r"C:\Users\yuanzj5\Desktop\Automation_line", True)
    observer.start()
    while True:
        print("监听中...")
        connfd, addr = sockfd.accept()
        print('客户端{}已经连入'.format(addr))
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            connfd.close()
            sockfd.close()
            observer.stop()
        observer.join()
        sys.exit('服务已停止')

