# -*- coding:utf-8 -*-
"""
模块描述:
测试脚本
作者：Sniper.ZH
"""
from pages.ReaderListPage import ReaderListPage
from pages.HomePage import HomePage
from models.UserinfoModel import UserinfoDAO

user = UserinfoDAO.selectOne("admin")
# user = UserinfoDAO.selectOne("sniper")
HomePage(user).show()

# print(len(UserinfoDAO.select(level='reader')))
