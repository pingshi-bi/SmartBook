# -*- coding:utf-8 -*-
"""
模块描述:
系统的公共方法
"""
import datetime
import re
import os
import hashlib
from getpass import getpass
from applogger import logger


def encrypt_password(username, password):
    return hashlib.md5((username + password).encode('utf-8')).hexdigest()


def getToday():
    # return datetime.datetime.now().strftime("%Y-%m-%d")
    return "yyyy-mm-dd"


def accept_input(message, warning="输入有误, 请重新输入..", check_re=None, is_passowrd=False, empty=False):
    while True:
        inStr = input(message) if not is_passowrd else getpass(message)
        res = inStr

        # 如果允许为空
        if empty is True and not inStr:
            break

        # 正则表达式
        if inStr and (re.match(check_re, inStr) if check_re else True):
            break
        else:
            print(warning)

    return res


def clear_screen():
    os.system('cls')


# 装饰器 检查管理员权限
def authcheck(func):
    def wrapper(page):
        try:
            logger.info("管理员权限检查：")
            logger.info(page.user)
            logger.info(page)

            if page.user.is_admin is not True:
                raise PermissionError("权限不足.")

            func(page)
        except Exception as e:
            logger.exception(e)
            print(e)
    return wrapper


# 装饰器 登陆检查
def logincheck(func):
    def wrapper(page):
        try:
            logger.info("登陆检查：")
            logger.info(page.user)
            logger.info(page)

            if page.user is None:
                raise PermissionError("请登陆.")
            func(page)
        except Exception as e:
            logger.exception(e)
            print(e)
    return wrapper
