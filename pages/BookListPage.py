# -*- coding:utf-8 -*-
"""
模块描述:
图书浏览
"""
from pages.SuperPage import SuperPage


class BookListPage(SuperPage):
    PAGE_MESSAGES = [
        "----图书浏览----",
        "在册图书({len(BookinfoDAO.select(p_state='normal'))})册, 借阅({len(BookinfoDAO.select(p_is_borrow=True))})册",
    ]

    PAGE_ACTIONS = [{
        "KEY": "n",
        "DESC": "登记图书",
        "AUTH": "admin",
        "ACTION": "BookActions.book_register"
    }, {
        "KEY": "s",
        "DESC": "查询图书",
        "ACTION": "BookActions.do_booklist"
    }, {
        "KEY": "u",
        "DESC": "借阅",
        "ACTION": "BookActions.do_borrow"
    }, {
        "KEY": "m",
        "DESC": "修改",
        "AUTH": "admin",
        "ACTION": "BookActions.do_modify"
    }, {
        "KEY": "d",
        "DESC": "删除",
        "AUTH": "admin",
        "ACTION": "BookActions.do_delete"
    }]
