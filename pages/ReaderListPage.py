# -*- coding:utf-8 -*-
"""
模块描述:
个人信息页面
"""
from pages.SuperPage import SuperPage


class ReaderListPage(SuperPage):
    PAGE_MESSAGES = [
        "----读者管理----",
        "注册读者({len(UserinfoDAO.select(level='reader'))})",
    ]

    PAGE_ACTIONS = [{
        "ACTION": "UserActions.do_readerlist"
    }]
