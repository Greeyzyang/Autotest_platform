import time
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class PageObject:
    driver = None

    def sleep(self, second):
        if str(second).isdigit():
            time.sleep(int(second))
        else:
            time.sleep(0.5)

    def wait(self, seconds):
        self.driver.implicitly_wait(seconds)

    def find_elementby(self, *loc):
        try:
            WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element(*loc).is_displayed())             #隐式等待
            count = 1
            while len(self.driver.find_element(*loc).text) == 0:
                time.sleep(0.5)
                count = count + 1
                if count >= 40:                                         #超过20秒退出循环
                    break
            return self.driver.find_element(*loc)
        except:
            raise BaseException(u'app页面未能找到该元素')


    def assert_connect_status(self):
        text = self.find_elementby(By.XPATH, "//*[@class='android.widget.TextView' and @resource-id='com.ryeex.sdk.demo:id/tv_connect_status']").text
        if len(text.encode("utf-8")) != 0:
            state = text[-3:]
            try:
                assert(state == u'已连接')
            except:
                raise BaseException(u'设备已断开连接%s' % text)
        else:
            raise BaseException(u'设备回调为空值')

    def input_data(self, value):
        self.find_elementby(By.XPATH, '//*[@text="数据输入"]').click()
        self.find_elementby(By.XPATH, '//*[@text="数据输入"]').send_keys(value)

    def clear_text(self):
        self.driver.press_keycode(29, 28672)                                                                            #键盘模拟选中所有删除
        self.driver.press_keycode(112)

    def assert_in_text(self, expecttext):
        text = self.find_elementby(By.XPATH, "//*[@resource-id='com.ryeex.sdk.demo:id/tv_result']").text
        text = text.encode("utf-8")
        if len(text) != 0:
            try:
                assert expecttext in text
            except:
                raise BaseException(u'Response验证失败，实际返回结果%s，预期返回结果%s' % (text, expecttext))
        else:
            raise BaseException('设备回调为空值')

    def assert_getdevicepagename(self, target_pagename):
        self.device_clickDID()
        self.assert_in_text(expecttext='page_name')
        if self.getdevice():
            page_name = self.getdevice()[1]
            try:
                assert(target_pagename == page_name)
            except:
                raise BaseException(u'验证失败：当前页面为%s，预期页面为%s' %(page_name, target_pagename))
        else:
            raise BaseException(u'page_name为空')

    def getdevice(self):
        text = self.find_elementby(By.XPATH, "//*[@resource-id='com.ryeex.sdk.demo:id/tv_result']").text
        text = text.encode("utf-8")
        if len(text) != 0:
            try:
                delta_ms = text.split(',')[1].split(':')[2]               #delta_ms:ui线程上次进入的时间戳距离现在过了多久
                page_name = text.split(',')[3].split(':')[1]
                rebort_cnt = text.split(',')[4].split(':')[1]
                # if page_name == 'remind':                                                                                 #退出提醒页面
                #     self.device_home()
                return delta_ms, page_name, rebort_cnt
            except:
                raise BaseException(u'获取delta_ms/page_name/rebort_cnt失败%s' % text)
        else:
            raise BaseException(u'设备回调为空值')

    def saturn_inputclick(self, sx, sy, ex, ey):
        self.assert_connect_status()
        self.input_data('{"method":"tp_move","sx":"' + sx + '","sy":"' + sy + '","ex":"' + ex + '","ey":"' + ey + '","duration":"50","interval":"50"}')
        self.find_elementby(By.XPATH, "//android.widget.Button[@text='坐标点击/滑动']").click()
        self.clear_text()
        self.assert_in_text(expecttext='ok')

    def saturn_inputslide(self, sx, sy, ex, ey):
        self.assert_connect_status()
        self.input_data('{"method":"tp_move","sx":"' + sx + '","sy":"' + sy + '","ex":"' + ex + '","ey":"' + ey + '","duration":"2000","interval":"50"}')
        self.find_elementby(By.XPATH, "//android.widget.Button[@text='坐标点击/滑动']").click()
        self.clear_text()
        self.assert_in_text(expecttext='ok')

    def device_upslide(self):
        self.assert_connect_status()
        self.find_elementby(By.XPATH, "//android.widget.Button[@text='上滑']").click()
        self.assert_in_text(expecttext='ok')

    def device_downslide(self):
        self.assert_connect_status()
        self.find_elementby(By.XPATH, "//android.widget.Button[@text='下滑']").click()
        self.assert_in_text(expecttext='ok')

    def device_leftslide(self):
        self.assert_connect_status()
        self.find_elementby(By.XPATH, "//android.widget.Button[@text='左滑']").click()
        self.assert_in_text(expecttext='ok')

    def device_rightslide(self):
        self.assert_connect_status()
        self.find_elementby(By.XPATH, "//android.widget.Button[@text='右滑']").click()
        self.assert_in_text(expecttext='ok')

    def device_home(self):
        self.assert_connect_status()
        self.find_elementby(By.XPATH, "//android.widget.Button[@text='HOME']").click()
        self.assert_in_text(expecttext='ok')

    def device_longhome(self):
        self.assert_connect_status()
        self.find_elementby(By.XPATH, "//android.widget.Button[@text='LONG HOME']").click()
        self.assert_in_text(expecttext='ok')
        self.device_clickDID()
        self.assert_getdevicepagename("power")

    def device_longpress(self):
        self.assert_connect_status()
        self.find_elementby(By.XPATH, "//android.widget.Button[@text='长按']").click()
        self.assert_in_text(expecttext='ok')
        time.sleep(2)
        self.assert_getdevicepagename("face_pick_page")

    def device_clickDID(self):
        self.find_elementby(By.XPATH, "//android.widget.Button[@text='获取设备标识']").click()

    def devices_click(self, text):
        self.find_elementby(By.XPATH, '//*[@text="' + text + '"]').click()



    @staticmethod
    def find_element(driver, locator, more=False, timeout=20):
        message = locator
        if isinstance(locator, dict):
            locator = (locator.get("by", None), locator.get("locator", None))
            message = locator
        elif isinstance(locator, list) and len(locator) > 2:
            locator = (locator[0], locator[1])
            message = locator
        elif isinstance(locator, Element):
            message = locator.name
            locator = (locator.by, locator.locator)
        elif isinstance(locator, str):
            locator = tuple(locator.split(".", 1))
            message = locator
        else:
            raise TypeError("element参数类型错误: type:" + str(type(locator)))
        try:
            try:
                if more:
                    return WebDriverWait(driver, timeout).until(ec.visibility_of_all_elements_located(locator))
                else:
                    return WebDriverWait(driver, timeout).until(ec.visibility_of_element_located(locator))
            except:
                if more:
                    return WebDriverWait(driver, timeout).until(ec.presence_of_all_elements_located(locator))
                else:
                    return WebDriverWait(driver, timeout).until(ec.presence_of_element_located(locator))
        except Exception:
            raise RuntimeError("找不到元素:" + str(message))