import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# logging.basicConfig(level = logging.INFO,format = '%(asctime)s -%(levelname)s:%(message)s')	#配置信息

dir = os.path.dirname(__file__)
handler = logging.FileHandler(r"{}/log.log".format(dir),encoding='utf-8')	#指明文件
handler.setLevel(logging.INFO)			   #设置打印到文件的消息等级

formatter = logging.Formatter('%(asctime)s -%(levelname)s:%(message)s')
handler.setFormatter(formatter)			  #设置打印到文件的配置信息

logger.addHandler(handler)