# -*- coding:utf-8 -*-
"""
模块描述:
Userinfo 模型层
"""
import hashlib
import os

from models.SuperModel import SuperModel
from api.PublicApi import *
from applogger import logger


class Userinfo:
    """
    Useirnfo model类
    对应这文件中的一行
    """

    def __init__(self, userid=None, username=None, password=None, realname=None, phone=None,
                 is_admin=False, state=None, create_date=None, last_date=None):
        """
        构造函数
        """
        self.userid = userid
        self.username = username
        self.password = password
        self.realname = realname
        self.phone = phone
        self.is_admin = is_admin
        self.state = state
        self.create_date = create_date
        self.last_date = last_date

    def properties(self):
        return [str(self.userid), self.username, self.password, self.realname, self.phone, str(self.__is_admin),
                self.state, self.create_date, self.last_date]

    def to_file_line(self):
        return SuperModel.FILE_SEPARATOR.join(self.properties()) + "\n"

    def __str__(self):
        return f"Userinfo:({','.join(self.properties())})"

    def __repr__(self):
        return self.__str__()

    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, value):
        self.__is_admin = value == "True" or value is True


class UserinfoDAO:
    """
    Userinfo 数据访问对象
    DAO: data access object
    """
    current_path = os.path.abspath(__file__)
    FILE_NAME = os.path.join(os.path.abspath(os.path.dirname(current_path)), "Userinfo.dbx")

    @staticmethod
    def insert(p_user):
        # 计算用户id
        # 以r的方式打开文件，进行文件读取操作
        if os.path.exists(UserinfoDAO.FILE_NAME):
            with open(UserinfoDAO.FILE_NAME, 'r', encoding=SuperModel.FILE_ENCODING) as rf:
                fileLines = rf.readlines()

                # 检查用户名的重复性
                for line in fileLines:
                    if line.split(SuperModel.FILE_SEPARATOR)[1] == p_user.username:
                        raise NameError("用户名已注册.")

            p_user.userid = len(fileLines) + 1
        else:
            p_user.userid = 1

        p_user.state = "0"
        p_user.is_admin = False
        p_user.create_date = getToday()
        p_user.last_date = getToday()
        # 密码加密处理
        p_user.password = encrypt_password(p_user.username, p_user.password)
        with open(UserinfoDAO.FILE_NAME, 'a', encoding=SuperModel.FILE_ENCODING) as wf:
            wf.write(p_user.to_file_line())

    @staticmethod
    def select(level=None):
        res = []
        if os.path.exists(UserinfoDAO.FILE_NAME):
            with open(UserinfoDAO.FILE_NAME, 'r', encoding=SuperModel.FILE_ENCODING) as rf:
                fileLines = rf.readlines()

                for line in fileLines:
                    fields = line.strip().split(SuperModel.FILE_SEPARATOR)
                    user = Userinfo()
                    user.userid = int(fields[0])
                    user.username = fields[1]
                    user.password = fields[2]
                    user.realname = fields[3]
                    user.phone = fields[4]
                    user.is_admin = fields[5]
                    user.state = fields[6]
                    user.create_date = fields[7]
                    user.last_date = fields[8]

                    # 我要获取读者信息，当前记录是管理员，那么就跳过
                    if level == 'reader' and user.is_admin is True:
                        logger.debug("continue")
                        logger.debug(user)
                        continue

                    res.append(user)

        return res

    @staticmethod
    def selectOne(p_username=None, p_userid=None):
        users = UserinfoDAO.select()
        for user in users:
            if user.username == p_username:
                return user
            if user.userid == p_userid:
                return user
        return None

    @staticmethod
    def update(p_user):
        if p_user is not None and p_user.userid > 0:
            users = UserinfoDAO.select()
            for i_user in users:
                if i_user.userid == p_user.userid:
                    i_user.username = p_user.username
                    logger.debug(p_user.username)
                    logger.debug(p_user.password)
                    logger.debug(encrypt_password(p_user.username, p_user.password))
                    i_user.password = encrypt_password(p_user.username, p_user.password)
                    i_user.realname = p_user.realname
                    i_user.phone = p_user.phone
                    i_user.is_admin = p_user.is_admin
                    i_user.state = p_user.state
                    i_user.create_date = p_user.create_date
                    i_user.last_date = p_user.last_date

                    logger.info("update userinfo:")
                    logger.info(i_user)

            with open(UserinfoDAO.FILE_NAME, 'w', encoding=SuperModel.FILE_ENCODING) as wf:
                for u in users:
                    logger.debug("write user: {}".format(u))
                    wf.write(u.to_file_line())
        else:
            raise ValueError("user参数错误.")
