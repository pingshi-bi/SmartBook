# -*- coding:utf-8 -*-
"""
模块描述:
    用户登陆页面
"""
from pages.SuperPage import SuperPage


class LoginPage(SuperPage):
    PAGE_MESSAGES = [
        "用户登陆",
        "----请输入用户名和密码----"
    ]

    PAGE_ACTIONS = [{
        "ACTION": "UserActions.do_login"
    }]
