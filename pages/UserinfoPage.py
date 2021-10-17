# -*- coding:utf-8 -*-
"""
模块描述:
个人信息页面
"""
from pages.SuperPage import SuperPage


class UserinfoPage(SuperPage):
    PAGE_MESSAGES = [
        "----我的个人信息----",
        "用户名: {self.user.username}",
        "编号: {self.user.userid}",
        "昵称: {self.user.realname}",
        "手机号: {self.user.phone}",
        "注册日期: {self.user.create_date}",
        "上次登录日期: {self.user.last_date}",
    ]

    PAGE_ACTIONS = [{
        "KEY": "m",
        "DESC": "修改密码",
        "ACTION": "UserActions.do_changepass"
    }, {
        "KEY": "n",
        "DESC": "修改昵称",
        "ACTION": "UserActions.do_changename"
    }]
