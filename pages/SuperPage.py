# -*- coding:utf-8 -*-
"""
模块描述:
所有页面的父类
"""
from applogger import logger
from api.PublicApi import *
from models.UserinfoModel import UserinfoDAO
from models.BookinfoModel import BookinfoDAO


class SuperPage:
    """
    封装所有页面的公共方法
    """
    MESSAGE_MAX_LEN = 60

    def __init__(self, user=None, reader=None, home=None, prev=None):
        self.user = user
        self.reader = reader
        self.home_page = home
        self.prev_page = prev

    def show(self):
        clear_screen()

        if self.user:
            print(f"当前用户:{self.user.username}({self.user.realname}), 系统日期 {getToday()}")
        print("*" * self.MESSAGE_MAX_LEN)
        for msg in self.PAGE_MESSAGES:
            logger.debug(msg)
            logger.debug(re.findall(r"(\{.+?\})", msg))
            for ps in re.findall(r"(\{.+?\})", msg):
                # eval
                # ps是{}括起来的表达式
                msg = msg.replace(ps, str(eval(ps[1:-1])))
            print("{0:^{1}s}".format(msg, self.MESSAGE_MAX_LEN - (len(msg.encode('utf-8')) - len(msg)) // 2))
        print("*" * self.MESSAGE_MAX_LEN)

        self.do_action()

    def do_action(self):

        if self.PAGE_ACTIONS:
            if len(self.PAGE_ACTIONS) == 1:
                action_str = self.PAGE_ACTIONS[0]['ACTION']
            else:
                if self.PAGE_ACTIONS:
                    command_line = ""
                    for action in self.PAGE_ACTIONS:
                        # 判断管理员权限，显示对应的指令，如果是普通用户，跳过管理员权限的指令
                        if action.get('AUTH', None) == "admin" and self.user.is_admin is not True:
                            continue
                        if command_line:
                            command_line += ","
                        command_line += f"{action['DESC']}({action['KEY'].upper()})"
                logger.debug(command_line)
                print("您可以选择如下操作:")
                if self.home_page is not None:
                    print("首页(H),", end='')
                if self.prev_page is not None and self.prev_page != self.home_page:
                    print("后退(B),", end="")
                print(command_line)

                while True:
                    command = input("请输入:")
                    if command.lower() in [x['KEY'].lower() for x in self.PAGE_ACTIONS] + ['h', 'b']:
                        logger.debug("用户输入的命令是: {}".format(command))
                        break
                    else:
                        print("输入有误, 请重新输入..")

                # 回首页
                if command.lower() == 'h':
                    self.home_page.show()
                if command.lower() == "b":
                    self.prev_page.show()

                # 根据用户的指令获取action字符串
                for action in self.PAGE_ACTIONS:
                    if command.lower() == action['KEY'].lower():
                        action_str = action['ACTION']
                        logger.debug("找到指令:")
                        logger.debug(action_str)

            # 使用反射映射方法并调用 reflect
            module, funcname = action_str.split(".")
            module = __import__("actions." + module, fromlist=True)
            if hasattr(module, funcname):
                logger.info(f">>>action:{action_str}")
                action_func = getattr(module, funcname)
                action_func(self)
            else:
                print(f"指令{command}方法{action_str}未定义")
        else:
            logger.warning("页面未定义actions")
