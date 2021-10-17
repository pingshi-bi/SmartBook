# -*- coding:utf-8 -*-
"""
模块描述:
图书管理模块的actions
"""
from api.PublicApi import *
from models.UserinfoModel import UserinfoDAO
from pages.BookAddPage import BookAddPage
from pages.BookListPage import BookListPage
from models.BookinfoModel import BookinfoDAO, Bookinfo
from models.BorrowregModel import Borrowreg, BorrowregDAO
from pages.BorrowListPage import BorrowListPage


@logincheck
def book_list(page):
    """进入图书列表页面"""
    BookListPage(user=page.user, home=page, prev=page).show()


@authcheck
def book_register(page):
    """进入图书登记页面"""
    BookAddPage(user=page.user, home=page.home_page, prev=page).show()


@authcheck
def do_register(page):
    """登记图书"""
    # 接收用户输入图书的信息
    bookname = accept_input(message="请输入书名:", check_re=r"^\w{1,30}$")

    bookname = f"《{bookname}》"
    logger.debug("书名: %s" % bookname)

    # 接收图书分类
    print("图书分类:")
    for i, key in enumerate(Bookinfo.BOOK_TYPES):
        print(f"{key}-{Bookinfo.BOOK_TYPES[key]}")

    re_str = f"^{'|'.join([x for x in Bookinfo.BOOK_TYPES.keys()])}$"
    logger.debug(re_str)
    booktype = accept_input(message=f"请选择分类({'/'.join([x for x in Bookinfo.BOOK_TYPES.keys()])}):",
                            check_re=re_str)

    logger.debug("分类是 %s" % booktype)

    # 输入作者
    author = accept_input(message="请输入作者:", check_re=r"^\w{2,10}$")
    logger.debug("作者 %s" % author)

    print("*" * 50)
    print("您输入的信息如下:")
    print("书名:", bookname)
    print("分类:", Bookinfo.BOOK_TYPES[booktype])
    print("作者:", author)
    print("*" * 50)

    confirm = accept_input(message="确认(Y), 取消(N), 重输(R):", check_re=r"^[ynrYNR]$")

    if confirm.lower() == "n":
        # 回到图书浏览页面
        page.prev_page.show()
    elif confirm.lower() == "r":
        page.show()
    elif confirm.lower() == "y":
        try:
            # 构造一个新书
            book = Bookinfo()
            book.bookname = bookname
            book.author = author
            book.booktype = booktype
            book.is_borrow = False
            book.createuser = page.user.username

            # 将图书存入文件
            BookinfoDAO.insert(book)

            confirm = accept_input(message="登记成功...结束(Q), 继续请回车:", check_re=r"^[qQ]$", empty=True)

            if confirm.lower() == 'q':
                BookListPage(page.user).show()
            else:
                page.show()
        except Exception as e:
            logger.exception(e)
            input(str(e) + "....任意键继续")
            page.show()


@logincheck
def do_booklist(page):
    # 展示查询条件
    # 可以按书名/分类/借阅状态
    command = accept_input(message="查询条件:书名(N),分类(T),借阅状态(P),回车查全部:",
                           warning="输入有误...",
                           check_re=r"^[ntpNTP]{1}$",
                           empty=True)
    logger.debug(command)
    if command is None or command.lower() != 'i':
        if command.lower() == "n":
            bookname = accept_input(message="请输入书名:",
                                    warning="输入有误,请重新输入...")
        if command.lower() == "t":
            print("图书分类:")
            for i, key in enumerate(Bookinfo.BOOK_TYPES):
                print(f"[{key}]-{Bookinfo.BOOK_TYPES[key]}")
            booktype = accept_input(message=f"请选择分类({'/'.join([x for x in Bookinfo.BOOK_TYPES.keys()])}):",
                                    check_re=f"^{'|'.join([x for x in Bookinfo.BOOK_TYPES.keys()])}$")

        if command.lower() == "p":
            is_borrow = accept_input(message="请选择(空闲Z/借阅B):",
                                     warning="输入有误,请重新输入...",
                                     check_re=r"^[ZBzb]{1}$")

        books = BookinfoDAO.select(p_state="normal")

        print("-" * page.MESSAGE_MAX_LEN)
        print("{0:4s}| {1:32s}| {2:8s}| {3:4s}".format("编号", "书名", "分类", "借阅"))
        print("-" * page.MESSAGE_MAX_LEN)
        count = 0
        for book in books:
            if command:
                if command.lower() == 'n' and bookname not in book.bookname:
                    continue
                if command.lower() == 't' and book.booktype != booktype:
                    continue
                if command.lower() == 'p':
                    if book.is_borrow and is_borrow.lower() == 'z':
                        continue
                    if not book.is_borrow and is_borrow.lower() == 'b':
                        continue

            bookname_length = 34 - (len(book.bookname.encode('utf-8')) - len(book.bookname)) // 2
            r_booktype = Bookinfo.BOOK_TYPES.get(book.booktype, "")
            r_is_borrow = "√" if book.is_borrow else ""
            print("{0:6s}| {1:{4}s}| {2:6s}| {3:^4s}".format(str(book.id), book.bookname, r_booktype,
                                                             r_is_borrow, bookname_length))
            count += 1

        print("-" * page.MESSAGE_MAX_LEN)
        print(f"总记录: {count} 条")
        input("......任意键继续......")
        page.show()
    else:
        pass


@logincheck
def do_borrow(page):
    """图书借阅"""
    book_id = accept_input(message="请输入要借阅的图书编号:", check_re=r"^\d+$")

    book = BookinfoDAO.selectOne(p_id=int(book_id))

    if book is None or book.state == Bookinfo.BOOK_STATUS['DELETE']:
        input("图书不存在..")
        page.show()

    if book.is_borrow is True:
        input("图书已经借出..")
        page.show()

    print("*" * 50)
    print("您输入的信息如下:")
    print("书名:", book.bookname)
    print("分类:", Bookinfo.BOOK_TYPES[book.booktype])
    print("作者:", book.author)
    print("*" * 50)

    # 确认一下
    confirm = accept_input(message="确认(Y), 取消(N):", check_re=r"^[ynYN]$")

    if confirm.lower() == "y":
        """登记借阅信息"""

        # 登记是谁借的那本书，包含借阅的时间
        borrow = Borrowreg(bookid=book.id, borrowuserid=page.user.userid)
        BorrowregDAO.insert(borrow)

        # 将图书的状态改成已经借阅
        book.is_borrow = True
        BookinfoDAO.update(book)
        input("借阅登记成功...任意键继续")

    page.show()


@authcheck
def do_delete(page):
    book_id = accept_input(message="请输入要删除的图书编号:",
                           warning="输入有误...",
                           check_re=r"^\d+$")

    book = BookinfoDAO.selectOne(p_id=int(book_id))
    if book is None or book.state != Bookinfo.BOOK_STATUS['NORMAL']:
        input(f"编号({book_id})的图书不存在....")
        page.show()

    if book.is_borrow:
        input(f"未归还的图书不能删除...")
        page.show()

    print("=" * 50)
    print("您要删除的图书信息如下:")
    print("编号:", book.id)
    print("书名:", book.bookname)
    print("分类:", Bookinfo.BOOK_TYPES[book.booktype])
    print("作者:", book.author)
    print("=" * 50)

    # 接收确认结果
    confirm = accept_input(message="确认删除(Y), 取消(N):",
                           warning="输入有误...",
                           check_re=r"^[ynYN]{1}$")
    logger.debug("确认结果: %s" % confirm)

    if confirm.lower() == "y":
        # 1.修改图书信息，将状态改为删除
        book.state = Bookinfo.BOOK_STATUS['DELETE']
        BookinfoDAO.update(book)

        input("删除成功...任意键继续")

    page.show()


@authcheck
def do_modify(page):
    book_id = accept_input(message="请输入要修改的图书编号:",
                           warning="输入有误...",
                           check_re=r"^\d+$")

    book = BookinfoDAO.selectOne(p_id=int(book_id))
    if book is None or book.state != Bookinfo.BOOK_STATUS['NORMAL']:
        input(f"编号({book_id})的图书不存在....")
        page.show()

    print("=" * 50)
    print("原图书信息如下:")
    print("书名:", book.bookname)
    print("分类:", Bookinfo.BOOK_TYPES[book.booktype])
    print("作者:", book.author)
    print("=" * 50)

    print("(请输入要修改的内容, 不修改直接回车)")
    # 接收书名
    bookname = accept_input(message="请输入新的书名:",
                            check_re=r"^(\w){1,30}$", empty=True)

    if bookname:
        bookname = f"《{bookname}》"

    logger.debug("书名: %s" % bookname)

    # 接收类型
    print("图书分类:")
    for i, key in enumerate(Bookinfo.BOOK_TYPES):
        print(f"[{key}]-{Bookinfo.BOOK_TYPES[key]}")
    booktype = accept_input(message=f"请选择新分类({'/'.join([x for x in Bookinfo.BOOK_TYPES.keys()])}):",
                            check_re=f"^{'|'.join([x for x in Bookinfo.BOOK_TYPES.keys()])}$", empty=True)
    logger.debug("输入分类: %s" % booktype)

    # 接收作者
    author = accept_input(message="请输入新作者:",
                          check_re=r"^(\w){2,10}$", empty=True)
    logger.debug("确认作者: %s" % author)

    if bookname is not None \
            or booktype is not None \
            or author is not None:
        print("=" * 50)
        print("您输入的信息如下:")
        if bookname:
            print("新书名:", bookname)
        if booktype:
            print("新分类:", Bookinfo.BOOK_TYPES[booktype])
        if author:
            print("新作者:", author)
        print("=" * 50)

        # 接收确认结果
        confirm = accept_input(message="确认修改(Y), 取消(N):",
                               warning="输入有误...",
                               check_re=r"^[ynYN]{1}$")
        logger.debug("确认结果: %s" % confirm)

        if confirm.lower() == "y":
            # 1.修改图书信息
            if bookname:
                book.bookname = bookname
            if booktype:
                book.booktype = booktype
            if author:
                book.author = author
            BookinfoDAO.update(book)

            input("修改成功...任意键继续")
    else:
        print("未输入任何新内容，不做修改.")

    page.show()


@logincheck
def book_borrowlist(page):
    """跳转借阅清单页面"""
    BorrowListPage(user=page.user, home=page, prev=page).show()


@authcheck
def book_readerborrowlist(page):
    """跳转借阅清单页面"""
    # 注意：这里是要查看读者的借阅，而不是管理员自己的借阅
    BorrowListPage(user=page.user, home=page.home_page, prev=page, reader=page.reader).show()


@logincheck
def do_borrowlist(page):
    if page.reader is not None:
        if page.user.is_admin is not True:
            input("无权查看他人信息...任意键继续")
            page.home_page.show()
        borrows = BorrowregDAO.select(p_borrow_user_id=page.reader.userid)
    else:
        borrows = BorrowregDAO.select(p_borrow_user_id=page.user.userid)

    print("-" * page.MESSAGE_MAX_LEN)
    print("{0:6s}|{1:22s}|{2:12s}|{3:4s}".format("借阅编号", "书名", "借阅人", "状态"))
    print("-" * page.MESSAGE_MAX_LEN)

    count = 0
    for reg in borrows:
        user = UserinfoDAO.selectOne(p_userid=reg.borrow_user_id)
        book = BookinfoDAO.selectOne(p_id=reg.book_id)
        bookname_length = 24 - (len(book.bookname.encode('utf-8')) - len(book.bookname))//2
        reg_state_str = "借出" if reg.state == "B" else "归还"
        print("{0:10s}|{1:{4}s}|{2:15s}|{3:4s}".format(str(reg.id), book.bookname, user.username,
                                                       reg_state_str, bookname_length))

        count += 1

    print("-" * page.MESSAGE_MAX_LEN)
    print(f"总记录：{count}条.")
    input(".....任意键继续......")
    page.show()


@logincheck
def do_return(page):
    """归还图书"""
    reg_id = accept_input(message="请输入要归还的借阅编号:", check_re=r"^\d+$")

    reg = BorrowregDAO.selectOne(p_id=int(reg_id))

    # 借阅记录是不是存在或者已归还，是不是本人借的
    if reg is None or reg.state == "R" or (reg.borrow_user_id == page.user.userid or page.user.is_admin):
        reg.state = Borrowreg.BORROW_STATUS['RETURN']
        reg.return_user_id = page.user.userid
        BorrowregDAO.update(reg)

        # 不要忘了，要同时更新图书状态
        book = BookinfoDAO.selectOne(p_id=reg.book_id)
        book.is_borrow = False
        BookinfoDAO.update(book)

        input("图书归还成功")
    else:
        input("无权操作...任意键继续")

    page.show()
