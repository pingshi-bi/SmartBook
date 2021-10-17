# -*- coding:utf-8 -*-
"""
模块描述:
图书登记
"""
from pages.SuperPage import SuperPage


class BookAddPage(SuperPage):
    PAGE_MESSAGES = [
        "----图书登记----",
    ]

    PAGE_ACTIONS = [{
        "ACTION": "BookActions.do_register"
    }]
