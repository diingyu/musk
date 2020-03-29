from selenium import webdriver,common
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

import sys
import time
import random
from datetime import datetime


APPOINTMENT = 1
RUSHBUY = 2

class JdMusk():
    def __init__(self,mode=APPOINTMENT):
        self.mode = mode
        self.appTime = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 15, 0).timestamp()
        self.orderTime = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 20, 0).timestamp()
        self.url = 'https://item.jd.com/100011551632.html'#口罩

    def setCookie(self):
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 20, 0.05)
        self.driver.get('https://passport.jd.com/new/login.aspx')
        # first_result = wait.until(presence_of_element_located((By.LINK_TEXT, "有小孩了")))

    def start(self):
        if self.mode == APPOINTMENT:
            while True:
                nowTime = datetime.now().timestamp()
                # 提前10秒开始预约
                if (self.appTime - nowTime < -600):
                    print('已经过了预约时间，明天再来吧！')
                    sys.exit(2)
                if (self.appTime - nowTime < 10):
                    print('准备预约！')
                    self.appointment()
                    # self.driver.quit()
                    break
        if self.mode == RUSHBUY:
            while True:
                nowTime = datetime.now().timestamp()
                # 提前10秒开始抢购
                leftTime = self.orderTime - nowTime
                if (leftTime < 10):
                    print('准备抢购！')
                    self.order1()  # 立即抢购
                    # self.driver.quit()
                    break
                elif (leftTime % 50 == 0):
                    print(leftTime)

    def order(self):
        tag = 1
        while True:
            self.driver.get(self.url)
            first_result = self.wait.until(presence_of_element_located((By.ID, "btn-reservation")))
            textContent = first_result.get_attribute("textContent")
            if (textContent == '等待抢购'):
                print('还没开始，等待抢购！{}'.format(tag))
            elif (textContent == '立即抢购'):
                try:
                    print('终于开始了，立即抢购!')
                    first_result.click()
                    first_result = self.wait.until(presence_of_element_located((By.CLASS_NAME, "checkout-submit")))
                    first_result.click()
                    print("提交订单！")
                    time.sleep(100)
                    break
                except common.exceptions.TimeoutException as e:
                    print('没赶上，明天再来吧！')
                    break
            time.sleep(random.randint(1, 3) * 0.01)
            tag += 1
            if (tag > 300):
                break

    #去购物车结算的方式
    def order1(self):
        tag = 1
        while True:
            self.driver.get(self.url)
            first_result = self.wait.until(presence_of_element_located((By.ID, "btn-reservation")))
            textContent = first_result.get_attribute("textContent")
            if (textContent == '等待抢购'):
                print('还没开始，等待抢购！{}'.format(tag))
            elif (textContent == '立即抢购'):
                try:
                    # print('终于开始了，立即抢购!')
                    first_result.click()
                    self.wait.until(presence_of_element_located((By.ID, "GotoShoppingCart"))).click()
                    # print("去购物车结算！")
                    self.wait.until(presence_of_element_located((By.LINK_TEXT, "去结算"))).click()
                    # print('去结算。。。')
                    time.sleep(100)
                    break
                except common.exceptions.TimeoutException as e:
                    print('没赶上，明天再来吧！')
                    break
            time.sleep(random.randint(1, 3) * 0.01)
            tag += 1
            if (tag > 300):
                break

    def appointment(self):
        tag = 1
        while True:
            self.driver.get(self.url)
            first_result = self.wait.until(presence_of_element_located((By.ID, "btn-reservation")))
            textContent = first_result.get_attribute("textContent")
            if (textContent == '等待预约'):
                print('还没开始，等待预约！{}'.format(tag))
            elif (textContent == '立即预约'):
                print('终于开始了，立即预约')
                first_result.click()
                try:
                    first_result = self.wait.until(presence_of_element_located((By.ID, "yuyue_msg_p")))
                    textContent = first_result.get_attribute("textContent")
                    print(textContent)
                    break
                except common.exceptions.TimeoutException as e:
                    print('超时了1。。。')

                try:
                    first_result = self.wait.until(presence_of_element_located((By.CLASS_NAME, "bd-right-result")))
                    textContent = first_result.get_attribute("textContent")
                    print(textContent)
                    break
                except common.exceptions.TimeoutException as e:
                    print('超时了2。。。')

            time.sleep(random.randint(1, 3) * 0.1)
            tag += 1
            if (tag > 100):
                break


#<a class="btn-addtocart" href="//cart.jd.com/cart.action?r=0.0740403697874712" id="GotoShoppingCart" clstag="pageclick|keycount|201601152|4"><b></b>去购物车结算</a>

if __name__=='__main__':
    musk = JdMusk(RUSHBUY)
    musk.setCookie()
    musk.start()


