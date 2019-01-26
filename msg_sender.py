# whatapp messages sending, ohad baehr, python 3.6

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re

#------------------------------#
options = webdriver.ChromeOptions()
options.add_argument('--log-level=3') 
options.add_argument("user-data-dir=selenium") 
browser = webdriver.Chrome('chromedriver', chrome_options=options)
wait = WebDriverWait(browser, 30)
#------------------------------#
name_partial_search_disabled=False
phone_partial_search_disabled=False
contact_list=['name or phone number']
#------------------------------#


def send_msg(msg):
    message = browser.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
    message.send_keys(msg)
    send_button = browser.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')[0]
    send_button.click()


def click(con_elem):
    action = webdriver.common.action_chains.ActionChains(browser)
    action.move_to_element_with_offset(con_elem, 5, 5)
    action.click()
    action.perform()


def api_search(phone_num):
    browser.get(f"https://api.whatsapp.com/send?phone={phone_num}")
    try:
        bigB=browser.find_element_by_id('action-button')
        click(bigB)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.RLfQR")))
        browser.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
        return None , 3
    except Exception:
        print(f"phone number: {phone_num} is not valid")
        elem=browser.find_element_by_class_name("_1WZqU")
        click(elem)
        time.sleep(0.5)
        return None, 0


def unify_phone_num(phone_num):
    dic=['+','-',' ','(',')']
    for ch in dic:
        phone_num = phone_num.replace(ch, '')
    if phone_num[0]=='0' and len(phone_num)>1:
        phone_num = phone_num[1:]
    return phone_num


def search_for(contact):
    try:
        search = browser.find_element_by_class_name("jN-F5")
        search.clear()
        search.send_keys(contact)
        time.sleep(0.5)
    except Exception as e:
        print(e)


def search_by_phone(phone_num):
    try:
        phone_elem = browser.find_elements_by_xpath(f"//img[contains(@src,'{phone_num+ '%40' + 'c'}')]")
        index=0
        if len(phone_elem)>1:
            index=1
            print("messaging yourself is a sign of narcisistic behavior")
        if phone_partial_search_disabled:
            real_p_num = re.search('&u=(.*)%40', phone_elem[index].get_attribute('src')).group(1)
            if(real_p_num!=phone_num):
                return None
        return phone_elem[index]
    except Exception:
        return None


def search_by_contact(contact):
    try:
        con_elem = browser.find_element_by_xpath(f"//span[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{contact}')][@class='_1wjpf']")
        if name_partial_search_disabled:
            name_in_app= con_elem.get_attribute("title").lower()
            if contact!=name_in_app:
                return None
        return con_elem
    except Exception:
        return None


def ret_contact(contact):
    try:
        reset_search = browser.find_element_by_class_name("_1M3wR")
        click(reset_search)
        time.sleep(0.5)
    except Exception:
        pass
    phone_num = unify_phone_num(contact)
    if phone_num.isnumeric():
        ret=search_by_phone(phone_num)
        if ret:
            return ret,2
        search_for(phone_num)
        ret=search_by_contact(phone_num)
        if ret:
            return ret,2
        return api_search(phone_num)
    ret=search_by_contact(contact)
    if ret:
        return ret,1  
    search_for(contact)  
    ret=search_by_contact(contact)
    if ret:
        return ret,1
    print(f'no match for {contact}')
    return None, 0
    

def main():
    browser.get("https://web.whatsapp.com/")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.RLfQR")))
    for contact in contact_list:
        contact=contact.lower()
        con_elem, mType = ret_contact(contact)
        if con_elem:
            click(con_elem)
        if mType:
            if mType==1:
                msg= f"This is a msg for {contact}"
                send_msg(msg)
            else:
                msg= "This is a test msg"
                send_msg(msg)

    time.sleep(0.5)
    browser.quit()

        
        


if __name__=="__main__":
    main()
