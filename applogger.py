# -*- coding:utf-8 -*-
"""
模块描述:
日志处理模块
"""
import logging
import os

current_path = os.path.abspath(__file__)
log_file = os.path.join(os.path.abspath(os.path.dirname(current_path)), 'debug.log')

logging.basicConfig(level=logging.DEBUG, filename=log_file,
                    format="%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s")

logger = logging.getLogger()
