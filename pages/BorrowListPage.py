# -*- coding:utf-8 -*-
"""
模块描述:
个人信息页面
"""
from pages.SuperPage import SuperPage


class BorrowListPage(SuperPage):
    PAGE_MESSAGES = [
        "----借阅清单----",
    ]

    PAGE_ACTIONS = [{
        "KEY": "s",
        "DESC": "查询",
        "ACTION": "BookActions.do_borrowlist"
    }, {
        "KEY": "r",
        "DESC": "归还图书",
        "ACTION": "BookActions.do_return"
    }]
