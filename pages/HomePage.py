# -*- coding:utf-8 -*-
"""
模块描述:
    个人主页信息

"""
from pages.SuperPage import SuperPage


class HomePage(SuperPage):
    PAGE_MESSAGES = [
        "",
        "您好{self.user.realname},您是第{self.user.userid}个读者",
        "欢迎来到,图书管理系统(SmartBook)",
        "在册登记图书({len(BookinfoDAO.select(p_state='normal'))}), 借阅图书({len(BookinfoDAO.select(p_is_borrow=True))})",
        "上次登陆: {self.user.last_date}",
        "",
    ]

    PAGE_ACTIONS = [{
        "KEY": "p",
        "DESC": "个人信息",
        "ACTION": "UserActions.user_info"
    }, {
        "KEY": "l",
        "DESC": "图书浏览",
        "ACTION": "BookActions.book_list"
    }, {
        "KEY": "u",
        "DESC": "读者管理",
        "AUTH": "admin",
        "ACTION": "UserActions.user_readerlist"
    }, {
        "KEY": "s",
        "DESC": "借阅清单",
        "ACTION": "BookActions.book_borrowlist"
    }, {
        "KEY": "e",
        "DESC": "注销",
        "ACTION": "UserActions.user_logout"
    }]
