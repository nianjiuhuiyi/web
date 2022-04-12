import logging

# 通过传参决定日志等级
# import sys
# print(sys.argv)
# level = sys.argv[1]
#
# numeric_level = getattr(logging, level)
# logging.basicConfig(level=numeric_level)

"(1)、安静日志输出到控制台"
# # 这个等级就代表了 logging.INFO即其以上的才会被记录
# # 若不给这个，默认等级为 logging.WARNING
# format格式不是必须的，但是这样会更加直观，定位了时间，错误位置
# logging.basicConfig(level=logging.INFO,
#                     format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")


"(2)、将日志输出到文件"
# # win上用的gbk，好像无法指定encoding
# logging.basicConfig(level=logging.WARNING,
#                     filename="./log.txt",
#                     filemode="w",       # 这个跟open的模式是一样的,it defaults to 'a'
#                     format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")


# "(3)、既要把日志输出到控制台，也要写入到日志文件"
# 第一步：创建一个logger
logger = logging.getLogger()  # 传建一个日志对象，不创建，默认就是root
logger.setLevel(logging.INFO)  # 这是log等级总开关

# 第二步：创建一个handler，用于写入日志文件
logfile = "./log.txt"
fh = logging.FileHandler(logfile, mode="a", encoding="utf-8")
fh.setLevel(logging.DEBUG)     # 输出到file中的log等级开关

# 第三步：再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)   # 输出到console中的log等级开关

# 第四步：定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 第五步：将logger添加到handler里面
logger.addHandler(fh)
logger.addHandler(ch)

# 日志
logger.debug("这是 logging debug message")
logger.info("这是 logging info message")
logger.warning("这是 logging warning message")
logger.error("这是 logging error message")
logger.critical("这是 logging critical message")

# 这个是可以跨日志的


"""-------配置文件用法------------"""
import logging.config
import yaml

# 通过配置文件配置logging
with open("./logging.conf.yaml", encoding="utf-8") as fp:
    dic = yaml.load(fp, Loader=yaml.FullLoader)
logging.config.dictConfig(dic)


# 创建logger
logger = logging.getLogger()

# 输出日志
logger.debug("这是 logging debug message")
logger.info("这是 logging info message")
logger.warning("这是 logging warning message")
logger.error("这是 logging error message")
logger.critical("这是 logging critical message")



