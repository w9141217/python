# encoding:utf-8
import requests
import re
import selenium.webdriver.support.ui as ui

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

brower = webdriver.Chrome()#选择打开的浏览器
wait = ui.WebDriverWait(brower, 10)  # 设置浏览器最长的加载时间

#查找内容
def search():
    try:
        brower.get('http://gou.jd.com/')  # 打开URL地址
        imput = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#inputkey'))# 查找输入框   元件的存在presence_of_element_located    使用CSS_SELECTOR选择器

        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        '#search_2015 > div.search_box_2015.clearfix > a')))  # 点击按钮框    可以点击的元素element_to_be_clickable

        imput.send_keys('魅族手机')  # 输入查找关键字
        submit.click()  # 点击查找
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#page > span > b')))  # 关于查找小辣椒手机所有的页数
        return total.text
    except TimeoutError:#判定失败继续返回执行查找
        return search()

#翻页操作
def next_page(page_number):
    try:
        imput = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#page_text')))#填写页面框

        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'#page_btn')))  # 点击确定按钮

        imput.clear()#先清除输入框内的内容
        imput.send_keys(page_number)#输入要查找的页数
        submit.click()#点击确定换页

        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#page > a.curr'),str(page_number)))#确定当前页面并判定页面    text_to_be_present_in_element确定文本中的文本信息  比如页码信息
    except TimeoutError:#如果判定出错继续返回执行翻页操作
        next_page(page_number)

#主页面
def main():
    total = search()
    total = int(re.compile('(\d+)').search(total).group(1))#转码
    for i in range(1 ,total + 1):
        next_page(i)


if __name__ == '__main__':
    main()
