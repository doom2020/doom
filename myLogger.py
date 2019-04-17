import logging
import sys

class LogHelper:
  """此类用来封装logging"""
  def __init__(self, name='LogHelper', setLevel=logging.DEBUG):
      #设置logger的name属性
       self.logger = logging.getLogger(name)
       self.formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
       # self.formatter=logging.Formatter(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
       #文件输出
       self.file_handler = logging.FileHandler(name+".log")
       self.file_handler.setFormatter(self.formatter)
       #终端输出
       self.consle_handler = logging.StreamHandler(sys.stdout)
       self.consle_handler.setFormatter(self.formatter)
       #设置logger的等级
       self.logger.setLevel(setLevel)
       #将logger添加到输出处理
       self.logger.addHandler(self.file_handler)
       self.logger.addHandler(self.consle_handler)


  def writeLog(self, info, level='debug'):
      """此方法为写日志"""
      if level == "critial":
          self.logger.critical(info)
      elif level == "error":
          self.logger.error(info)
      elif level == "warning":
          self.logger.warning(info)
      elif level == "info":
          self.logger.info(info)
      else:
          self.logger.debug(info)
            
  def removeLog(self):
      """此方法删除旧的日志"""
      self.logger.removeHandler(self.file_handler)
      self.logger.removeHandler(self.consle_handler)
        
if __name__ == "__main__":
    logger = LogHelper()
    logger.writeLog("helloworld", level='error')
    logger.removeLog()