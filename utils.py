import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import json

def login(mail,password,browser):
    browser.get("https://twitter.com/login")
    sleep(3)
    element_mail = browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input')
    element_pass = browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input')
    element_mail.send_keys(mail)
    element_pass.send_keys(password)
    element_pass.send_keys(Keys.RETURN)
    
    
def get_tweet_info(card,browser):
    try:
        name = username = card.find_element_by_xpath('.//span').text
    except NoSuchElementException:
        return
    try:
        handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
    except NoSuchElementException:
        return
    try:
        postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
    except NoSuchElementException:
        return
    comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
    text = comment + responding
    reply_cnt = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
    retweet_cnt = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
    like_cnt = card.find_element_by_xpath('.//div[@data-testid="like"]').text
    
    return {
            "name":name,
            "handle":handle,
            "postdate":postdate,
            "text":text,
            "reply_cnt" :reply_cnt,
            "retweet_cnt":retweet_cnt,
            "like_cnt":like_cnt
            }