# -*- coding:utf-8 -*-
"""
模块描述:
欢迎页
"""
from pages.SuperPage import SuperPage


class WelcomePage(SuperPage):
    PAGE_MESSAGES = [
        "",
        "欢迎来到,",
        "图书管理系统(SmartBook)",
        "版本号: v0.1",
        "开发者: Sniper",
        "系统日期: yyyy年mm月dd日",
        "",
    ]

    PAGE_ACTIONS = [{
        "KEY": "l",
        "DESC": "登陆",
        "ACTION": "UserActions.user_login"
    }, {
        "KEY": "r",
        "DESC": "注册",
        "ACTION": "UserActions.user_register"
    }, {
        "KEY": "f",
        "DESC": "找回密码",
        "ACTION": "UserActions.do_findpass"
    }, {
        "KEY": "q",
        "DESC": "退出",
        "ACTION": "PublicActions.sys_exit"
    }]


if __name__ == '__main__':
    WelcomePage().show()