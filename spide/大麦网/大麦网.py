# -*- coding: utf-8 -*-
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DataUtils:
    @staticmethod
    def user_login(login_type=None, login_name=None, login_password=None):
        login_url = 'https://passport.damai.cn/login'
        damai_title = '大麦网-全球演出赛事官方购票平台-100%正品、先付先抢、在线选座！'

        # 创建了一个Chrome浏览器的选项对象。
        option = webdriver.ChromeOptions()
        # 关闭了Chrome浏览器的开发者模式，以避免一些网站检测到使用Selenium自动化测试工具而导致的问题
        # excludeSwitches 表示要排除哪些选项，enable-automation 表示排除Chrome浏览器的开发者模式。
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_argument('--disable-blink-features=AutomationControlled')  # 禁用Chrome浏览器的自动化控制特性。
        # option.add_argument('headless')               # 即在后台无窗口运行Chrome浏览器，以避免测试过程中的界面干扰。
        # option.add_argument('window-size=1920x1080')  # 设置浏览器窗口大小为1920x1080像素，以适应不同的测试场景和需求。
        # option.add_argument('no-sandbox')             # 取消Chrome浏览器的沙盒模式，以避免一些权限问题
        # option.add_argument('--disable-gpu')          # 禁用Chrome浏览器的GPU加速，以避免一些兼容性问题
        # option.add_argument('disable-dev-shm-usage')  # 将大量渲染时写入临时目录/tmp而非/dev/shm，以避免一些内存问题。

        browser = webdriver.Chrome(options=option)
        browser.set_page_load_timeout(60)  # 设置页面加载的最长超时时间为60秒

        browser.get(login_url)

        # 账号密码登录 验证码登录 扫码登录
        if login_type == 'account':
            browser.switch_to.frame('alibaba-login-box')
            browser.find_element(By.ID, "fm-login-id").send_keys(login_name)
            browser.find_element(By.ID, "fm-login-password").send_keys(login_password)
            browser.find_element(By.CLASS_NAME, "password-login").send_keys(Keys.ENTER)
        elif login_type == 'sms':
            pass
        elif login_type == 'qrcode':
            pass
        else:
            pass
        # 创建一个等待对象，最长等待时间为180秒，轮询间隔为0.5秒。 # 等待页面title包含指定的字符串
        WebDriverWait(browser, 180, 0.5).until(EC.title_contains(damai_title))  # 这一行的作用是等待登录完成，确保页面加载完毕。

        login_cookies = {}
        if browser.title != damai_title:
            print('登录异常，请检查页面登录提示信息')

        # 登录成功 获取登录后的cookies
        for cookie in browser.get_cookies():
            login_cookies[cookie['name']] = cookie['value']
        # 检查cookies 是否有效
        if DataUtils.check_login_status(login_cookies):
            return login_cookies

    @staticmethod
    def check_login_status(login_cookies):
        pass


class DaMaiTicket:
    def __init__(self):
        # 登录信息
        self.login_cookies = {}
        self.session = requests.Session()
        self.login_name: str = 'account'  # 大麦网登录账户名
        self.login_password: str = 'password'  # 大麦网登录密码
        # 以下为抢票必须的参数
        self.ticket_id: int = 610820299671  # 商品id
        self.viewer: list = ['viewer1']  # 在大麦网已填写的观影人
        self.buy_nums: int = 1  # 购买影票数量, 需与观影人数量一致
        self.ticket_price: int = 180  # 购买指定票价


if __name__ == "__main__":
    damai = DaMaiTicket()
