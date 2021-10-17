# -*- coding:utf-8 -*-
"""
图书管理系统
SmartBook model类
代码描述:
     Bookinfo数据访问对象
     DAO Data Access Object
"""
from models.SuperModel import SuperModel
from applogger import logger
from api.PublicApi import *


class Bookinfo(SuperModel):
    """
    Bookinfo model类
    对应图书信息数据文件中的一条记录
    """
    BOOK_STATUS = {
        "NORMAL": "0",
        "DELETE": "9"
    }
    
    BOOK_TYPES = {
        "01": "科普读物",
        "02": "科学技术",
        "03": "儿童绘本"
    }

    def __init__(self, bookid=None, booktype=None, bookname=None, author=None,
                 is_borrow=None, state=None, createuser=None):
        """
        构造函数
        """
        self.id = bookid
        self.booktype = booktype
        self.bookname = bookname
        self.author = author
        self.state = state
        self.is_borrow = is_borrow
        self.createuser = createuser
        # self.createdate = createdate
        # self.publish = publish
        # self.publishdate = publishdate

    @property
    def properties(self):
        return [str(self.id), self.booktype, self.bookname, self.author,
                self.state, str(self.is_borrow), self.createuser]

    def to_file_str(self):
        return self.FILE_SEPARATOR.join(self.properties) + "\n"

    @property
    def is_borrow(self):
        return self.__is_borrow == "True" or self.__is_borrow is True

    @is_borrow.setter
    def is_borrow(self, value):
        self.__is_borrow = value

    def __str__(self):
        return "Bookinfo:(" + ','.join(self.properties) + ")"

    def __repr__(self):
        return self.__str__()


class BookinfoDAO(SuperModel):
    """
    Bookinfo 数据访问对象类
    用来访问和处理图书信息数据
    """
    FILE_NAME = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))), "Bookinfo.dbx")

    @staticmethod
    def insert(p_book):
        """
        插入图书信息
        :param p_book: Bookinfo对象
        :return: None
        """
        if type(p_book) is not Bookinfo:
            raise TypeError('参数类型必须为Bookinfo对象.')

        if os.path.exists(BookinfoDAO.FILE_NAME):
            r_books = BookinfoDAO.select()
            p_book.id = r_books[-1].id + 1
        else:
            p_book.id = 1

        if p_book.state is None:
            p_book.state = Bookinfo.BOOK_STATUS['NORMAL']

        with open(BookinfoDAO.FILE_NAME, "a", encoding=SuperModel.FILE_ENCODING) as wf:
            wf.write(p_book.to_file_str())
        logger.info("INSERT book:")
        logger.info(p_book)

    @staticmethod
    def select(p_state=None, p_is_borrow=None, p_author=None):
        """
        查询多条图书数据
        :param p_state: normal:查询未删除图书 默认:全部
        :param p_is_borrow: bool 类型 借阅状态
        :param p_author: 作者
        :return: Bookinfo 列表
        """
        res = []
        logger.debug("数据文件: %s" % os.path.abspath(BookinfoDAO.FILE_NAME))
        if os.path.exists(BookinfoDAO.FILE_NAME):
            with open(BookinfoDAO.FILE_NAME, 'r', encoding=SuperModel.FILE_ENCODING) as rf:
                for line in rf.readlines():

                    fields = line.strip().split(SuperModel.FILE_SEPARATOR)

                    book = Bookinfo()
                    book.id = int(fields[0])
                    book.booktype = fields[1]
                    book.bookname = fields[2]
                    book.author = fields[3]
                    book.state = fields[4]
                    book.is_borrow = fields[5]
                    book.createuser = fields[6]

                    if p_state:
                        if p_state == "normal":
                            if book.state != Bookinfo.BOOK_STATUS['NORMAL']:
                                continue
                        else:
                            raise ValueError("state 参数错误.")

                    if p_is_borrow:
                        if type(p_is_borrow) is not bool:
                            raise ValueError("is_borrow 参数错误.")
                        if book.is_borrow != p_is_borrow:
                            continue

                    if p_author and book.author != p_author:
                        continue

                    res.append(book)
        return res

    @staticmethod
    def selectOne(p_id=None):
        books = BookinfoDAO.select()
        for book in books:
            if p_id is not None and book.id == p_id:
                logger.info("SELECT BY ID:")
                logger.info(book)
                return book
        return None

    @staticmethod
    def update(p_book):
        if p_book is not None and p_book.id > 0:
            books = BookinfoDAO.select()
            for book in books:
                if book.id == p_book.id:
                    logger.debug(book)
                    logger.debug(p_book)
                    book.bookname = p_book.bookname
                    book.booktype = p_book.booktype
                    book.author = p_book.author
                    book.state = p_book.state
                    book.is_borrow = p_book.is_borrow
                    book.createuser = p_book.createuser
                    logger.info("UPDATE book:")
                    logger.info(book)
                    break
            with open(BookinfoDAO.FILE_NAME, "w", encoding=SuperModel.FILE_ENCODING) as wf:
                for book in books:
                    wf.write(book.to_file_str())
        else:
            raise ValueError("图书信息错误.")


if __name__ == '__main__':
    pass
