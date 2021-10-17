# -*- coding:utf-8 -*-
"""
模块描述:
用户注册页面
"""
from pages.SuperPage import SuperPage


class RegisterPage(SuperPage):
    PAGE_MESSAGES = [
        "",
        "用户注册",
        "",
    ]

    PAGE_ACTIONS = [{
        "ACTION": "UserActions.do_register"
    }]


if __name__ == '__main__':
    RegisterPage().show()
