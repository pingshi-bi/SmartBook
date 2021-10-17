# -*- coding:utf-8 -*-
"""
模块描述:
系统公共actions方法
"""
import sys
from applogger import logger


def sys_exit(page):
    print("再见，欢迎下次使用...")
    logger.info("用户退出系统")
    sys.exit(0)
