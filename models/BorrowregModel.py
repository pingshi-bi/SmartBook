# -*- coding:utf-8 -*-
"""
借阅管理系统
SmartBook 借阅登记簿
代码描述:
     Borrowreg数据访问对象
     DAO Data Access Object
"""
from models.SuperModel import SuperModel
from applogger import logger
from api.PublicApi import *


class Borrowreg(SuperModel):
    """
    Borrowreg model类
    对应借阅信息数据文件中的一条记录
    """
    BORROW_STATUS = {
        "BORROW": "B",
        "RETURN": "R"
    }
    
    def __init__(self, bookid=None, borrowuserid=None):
        """
        构造函数
        """
        self.id = None
        self.book_id = bookid
        self.borrow_user_id = borrowuserid
        self.state = Borrowreg.BORROW_STATUS['BORROW']
        self.return_user_id = None
        # self.borrowdate = createdate
        # self.returndate = returndate

    @property
    def properties(self):
        return [str(self.id), str(self.book_id), str(self.borrow_user_id), self.state, str(self.return_user_id)]

    def to_file_str(self):
        return self.FILE_SEPARATOR.join(self.properties) + "\n"

    def __str__(self):
        return "Borrowreg:(" + ','.join(self.properties) + ")"

    def __repr__(self):
        return self.__str__()


class BorrowregDAO(SuperModel):
    """
    Borrowreg 数据访问对象类
    用来访问和处理借阅记录数据
    """
    FILE_NAME = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))), "Borrowreg.dbx")

    @staticmethod
    def insert(p_borrow):
        """
        插入借阅信息
        :param p_borrow: Borrowreg对象
        :return: None
        """
        if type(p_borrow) is not Borrowreg:
            raise TypeError('参数类型必须为Borrowreg对象.')

        if os.path.exists(BorrowregDAO.FILE_NAME):
            r_borrows = BorrowregDAO.select()
            p_borrow.id = r_borrows[-1].id + 1
        else:
            p_borrow.id = 1

        with open(BorrowregDAO.FILE_NAME, "a", encoding=SuperModel.FILE_ENCODING) as wf:
            wf.write(p_borrow.to_file_str())
        logger.info("INSERT borrow:")
        logger.info(p_borrow)

    @staticmethod
    def select(p_state=None, p_borrow_user_id=None):
        """
        查询多条借阅数据
        :param p_state: borrow:借阅 return:归还 默认:全部
        :param p_borrow_user_id: int 类型 借阅人id，Userinfo.id
        :return: Borrowreg 列表
        """
        res = []
        logger.debug("数据文件: %s" % os.path.abspath(BorrowregDAO.FILE_NAME))
        if os.path.exists(BorrowregDAO.FILE_NAME):
            with open(BorrowregDAO.FILE_NAME, 'r', encoding=SuperModel.FILE_ENCODING) as rf:
                for line in rf.readlines():

                    fields = line.strip().split(SuperModel.FILE_SEPARATOR)

                    borrow = Borrowreg()
                    borrow.id = int(fields[0])
                    borrow.book_id = int(fields[1])
                    borrow.borrow_user_id = int(fields[2])
                    borrow.state = fields[3]
                    borrow.return_user_id = int(fields[4]) if fields[4] != "None" else None

                    if p_state:
                        if p_state == "borrow":
                            if borrow.state != Borrowreg.BORROW_STATUS['BORROW']:
                                continue
                        else:
                            raise ValueError("state 参数错误.")

                    if p_borrow_user_id:
                        if type(p_borrow_user_id) is not int:
                            raise ValueError("p_borrow_user_id 参数类型错误.")
                        if borrow.borrow_user_id != p_borrow_user_id:
                            continue

                    res.append(borrow)
        return res

    @staticmethod
    def selectOne(p_id=None):
        if p_id is not None and type(p_id) is not int:
            raise ValueError("p_id 参数类型错误.")
        borrows = BorrowregDAO.select()
        for borrow in borrows:
            if p_id is not None and borrow.id == p_id:
                logger.info("SELECT BY ID:")
                logger.info(borrow)
                return borrow
        return None

    @staticmethod
    def update(p_borrow):
        if p_borrow is not None and p_borrow.id > 0:
            borrows = BorrowregDAO.select()
            for borrow in borrows:
                if borrow.id == p_borrow.id:
                    logger.debug(borrow)
                    logger.debug(p_borrow)
                    borrow.borrow_user_id = p_borrow.borrow_user_id
                    borrow.return_user_id = p_borrow.return_user_id
                    borrow.book_id = p_borrow.book_id
                    borrow.state = p_borrow.state
                    logger.info("UPDATE borrow:")
                    logger.info(borrow)
                    break
            with open(BorrowregDAO.FILE_NAME, "w", encoding=SuperModel.FILE_ENCODING) as wf:
                for borrow in borrows:
                    wf.write(borrow.to_file_str())
        else:
            raise ValueError("借阅信息错误.")


if __name__ == '__main__':
    pass
