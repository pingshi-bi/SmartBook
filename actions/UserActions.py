# -*- coding:utf-8 -*-
"""
模块描述:
用户模块的操作
"""
from applogger import logger
from api.PublicApi import *
from pages.RegsterPage import RegisterPage
from pages.WelcomePage import WelcomePage
from pages.LoginPage import LoginPage
from pages.HomePage import HomePage
from pages.UserinfoPage import UserinfoPage
from pages.ReaderListPage import ReaderListPage
from pages.ReaderInfoPage import ReaderInfoPage
from models.UserinfoModel import UserinfoDAO, Userinfo


def user_login(page):
    LoginPage().show()


def user_register(page):
    RegisterPage().show()


def do_register(page):
    # 接收用户输入的个人信息
    # 输入用户名
    username = accept_input(message="请输入用户名(3-16位字母、数字、下划线组合):",
                            check_re=r"^\w{3,16}$")

    logger.debug("用户名: {}".format(username))

    # 输入密码
    password = accept_input(message="请输入密码(6-12位):",
                            check_re=r"^\S{6,12}$", is_passowrd=True)
    logger.debug("密码: {}".format(password))

    # 输入确认密码
    apassword = accept_input(message="请确认密码:", warning="两次输入密码不一致, 请重新输入..",
                             check_re=f"^{password}$", is_passowrd=True)

    logger.debug("确认密码: {}".format(apassword))

    # 输入昵称
    realname = accept_input(message="请输入昵称:", check_re=r"^\S{1,10}$")
    logger.debug("昵称: {}".format(realname))

    # 输入手机号码
    phone = accept_input(message="请输入手机号:", check_re=r"^[1][3456789]\d{9}$")
    logger.debug("手机号码: {}".format(phone))

    print("*" * 50)
    print("您输入的信息如下:")
    print("用户名:", username)
    print("密码:", "*" * len(password))
    print("昵称:", realname)
    print("手机号:", phone)
    print("*" * 50)

    # 接收确认指令
    command = accept_input(message="确认注册(Y), 取消(N), 重新输入(R):", check_re=r"^[ynrYNR]$")
    logger.debug("确认结果: {}".format(command))

    # 如果用户确认注册，我们将用户的个人信息，保存到文件中
    if command.lower() == "y":
        logger.debug("完成注册用户信息的保存")
        # 讲录入的个人信息保存到文件中
        try:
            user = Userinfo()
            user.username = username
            user.realname = realname
            user.password = password
            user.phone = phone

            UserinfoDAO.insert(user)

            input("注册成功...任意键继续")
            # 跳转回欢迎页
            WelcomePage().show()
        except Exception as e:
            logger.exception(e)
            input(str(e) + "...按任意键继续")
            page.show()

    elif command.lower() == 'n':
        # 不注册的时候，回到欢迎页面welcome 的show()
        WelcomePage().show()
    elif command.lower() == 'r':
        # 重新输入的时候，再次展示register页面的show()
        page.show()
    else:
        # 为了程序的健壮性，要把其他情况考虑进来
        input("您输入的指令不支持...请联系管理员.")
        WelcomePage().show()


def do_login(page):
    logger.info("用户登陆检查")
    username = accept_input(message="请输入用户名:", warning="用户名必输...")
    logger.debug("用户名: {}".format(username))

    # 输入密码
    password = accept_input(message="请输入密码:", is_passowrd=True, warning="密码必输...")

    try:
        user = UserinfoDAO.selectOne(username)
        logger.info(f"当前用户，{str(user)}")

        # 检查密码
        if user is None or user.password != encrypt_password(username, password):
            logger.error(username)
            logger.error(password)
            logger.error(user.password)
            logger.error(encrypt_password(username, password))
            raise PermissionError("用户名或密码错误")

        input("登陆成功...任意键继续")
        # 进入主页面
        HomePage(user).show()
    except Exception as e:
        logger.exception(e)
        input(str(e) + "....任意键重新录入")
        page.show()


def do_findpass(page):
    """密码找回"""
    # 输入用户名
    username = accept_input(message="请输入用户名:",
                            check_re=r"^\w{3,16}$")
    logger.debug("用户名: {}".format(username))

    user = UserinfoDAO.selectOne(username)
    if user is None:
        print("用户不存在...任意键继续")
        page.show()

    print(f"验证码发送到({user.phone[-4:]})的手机上,请注意查收...")

    randCode = accept_input("请输入验证码:", check_re=r"^\d{6}$")
    logger.debug("验证码 {}".format(randCode))
    # 检查验证码的正确性

    # 输入密码
    password = accept_input(message="请输入新密码(6-12位):",
                            check_re=r"^\S{6,12}$", is_passowrd=True)
    logger.debug("密码: {}".format(password))

    # 输入确认密码
    apassword = accept_input(message="请确认密码:", warning="两次输入密码不一致, 请重新输入..",
                             check_re=f"^{password}$", is_passowrd=True)

    logger.debug("确认密码: {}".format(apassword))

    # 更新用户的密码
    user.password = password
    UserinfoDAO.update(user)
    input("找回密码成功...任意键继续")
    page.show()


@logincheck
def do_changepass(page):
    # 输入密码
    password = accept_input(message="请输入原密码:",
                            is_passowrd=True)

    if encrypt_password(page.user.username, password) != page.user.password:
        input("密码错误...任意键继续")
        page.show()

    # 输入密码
    password = accept_input(message="请输入新密码(6-12位):",
                            check_re=r"^\S{6,12}$", is_passowrd=True)
    logger.debug("密码: {}".format(password))

    # 输入确认密码
    apassword = accept_input(message="请确认密码:", warning="两次输入密码不一致, 请重新输入..",
                             check_re=f"^{password}$", is_passowrd=True)
    logger.debug("确认密码: {}".format(apassword))

    page.user.password = password
    UserinfoDAO.update(page.user)
    input("密码修改成功...任意键继续")
    page.show()


@logincheck
def do_changename(page):
    # 输入密码
    password = accept_input(message="请输入原密码:",
                            is_passowrd=True)

    if encrypt_password(page.user.username, password) != page.user.password:
        input("密码错误...任意键继续")
        page.show()

    # 输入昵称
    realname = accept_input(message="请输入新昵称:", check_re=r"^\S{1,10}$")
    logger.debug("昵称: {}".format(realname))

    page.user.realname = realname
    UserinfoDAO.update(page.user)
    input("昵称修改成功...任意键继续")
    page.show()


@logincheck
def user_info(page):
    """个人用户信息页面"""
    UserinfoPage(user=page.user, home=page, prev=page).show()


@logincheck
def user_logout(page):
    """用户注销"""
    page.user = None
    WelcomePage().show()


@authcheck
def user_readerlist(page):
    print("进入读者管理页面")
    ReaderListPage(user=page.user, home=page, prev=page).show()


@authcheck
def do_readerlist(page):
    command = accept_input(message="查询条件: 用户名(U), 手机号(P), 读者详情(I), 回车查全部:",
                           check_re=r"^[upiUPI]$", empty=True)
    logger.debug(command)

    if not command or command.lower() != 'i':
        if command.lower() == 'u':
            username = accept_input(message="请输入用户名:")
        if command.lower() == 'p':
            phone = accept_input(message="请输入手机号:")

        readers = UserinfoDAO.select(level='reader')
        print("-" * page.MESSAGE_MAX_LEN)
        print("{0:4s}|{1:13s}|{2:16s}|{3:11s}".format("编号", "用户名", "昵称", "手机号"))
        print("-" * page.MESSAGE_MAX_LEN)
        count = 0
        for reader in readers:
            if command.lower() == 'u' and reader.username != username:
                continue
            if command.lower() == 'p' and reader.phone != phone:
                continue

            realname_length = 18 - (len(reader.realname.encode('utf-8')) - len(reader.realname)) // 2
            print("{0:6d}|{1:16s}|{2:{4}s}|{3:11s}".format(reader.userid, reader.username,
                                                           reader.realname, reader.phone, realname_length))
            count += 1

        print("-" * page.MESSAGE_MAX_LEN)
        print(f"共{count}条数据.")

    reader_id = accept_input(message="查看用户详情，请输入用户编号，回车继续:",
                             check_re=r"^\d+$", empty=True)

    if reader_id:
        logger.debug(reader_id)

        reader = UserinfoDAO.selectOne(p_userid=int(reader_id))
        if reader is None:
            input(f"读者{reader_id}不存在....任意键继续")
            page.show()
        else:
            # 进入读者详情页面
            ReaderInfoPage(user=page.user, reader=reader, home=page.home_page, prev=page).show()
    else:
        page.show()


@authcheck
def do_setAdmin(page):
    """设为管理员"""
    reader = page.reader

    confirm = accept_input(message="确认(Y), 取消(N)", check_re=r"^[ynYN]$")
    if confirm.lower() == "y":
        reader.is_admin = True
        UserinfoDAO.update(reader)
        input("设置成功...任意键继续")

    page.show()
