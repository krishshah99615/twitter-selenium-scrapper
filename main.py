import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import json
from utils import login,get_tweet_info
SEARCH_QUERY = "#Cars"
MAX_TWEETS=25
browser = webdriver.Chrome('chromedriver')
password,mail = json.load(open("pass.json"))['pass'],json.load(open("pass.json"))['mail']
login(mail,password,browser)
browser.get('https://twitter.com/explore')
sleep(3)
element_search = browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/form/div[1]/div/div/div[2]/input')
element_search.send_keys(SEARCH_QUERY)
element_search.send_keys(Keys.RETURN)
sleep(3)
browser.find_element_by_link_text('Latest').click()
sleep(3)
data=[]
tweet_ids=set()

last_position = browser.execute_script("return window.pageYOffset;")
scrolling = True

while(True):
    tweet_blocks = browser.find_elements_by_xpath('//div[@data-testid="tweet"]')
    for card in tweet_blocks:
        tweet = get_tweet_info(card,browser)
        if tweet:
            tweet_identifier = tweet['name']+tweet['handle']+tweet['text']
            if tweet_identifier not in tweet_ids:
                tweet_ids.add(tweet_identifier)
                MAX_TWEETS =MAX_TWEETS -1

                print(MAX_TWEETS)
                data.append(tweet)
                if MAX_TWEETS <= 0:
                    break
    if MAX_TWEETS <= 0:
        break
    scroll_attempt = 0
    while True:
        # check scroll position
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(2)
        curr_position = browser.execute_script("return window.pageYOffset;")
        if last_position == curr_position:
            scroll_attempt += 1
            
            # end of scroll region
            if scroll_attempt >= 3:
                scrolling = False
                break
            else:
                sleep(2) # attempt another scroll
        else:
            last_position = curr_position
            break
browser.close()
with open('TWEETS.json', 'w') as fout:
    json.dump(data , fout)

