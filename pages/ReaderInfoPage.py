# -*- coding:utf-8 -*-
"""
模块描述:
读者详情页面
"""
from pages.SuperPage import SuperPage


class ReaderInfoPage(SuperPage):
    PAGE_MESSAGES = [
        "",
        "----读者详情----",
        "编号: {self.reader.userid}",
        "用户名: {self.reader.username}",
        "手机号: {self.reader.phone}",
        "",
    ]

    PAGE_ACTIONS = [{
        "KEY": "a",
        "DESC": "设为管理员",
        "ACTION": "UserActions.do_setAdmin"
    }, {
        "KEY": "s",
        "DESC": "借阅清单",
        "ACTION": "BookActions.book_readerborrowlist"
    }]
