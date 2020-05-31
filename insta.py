# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import time 
from selenium import webdriver
import pyperclip
import pyautogui
import random
import csv
import instaloader
from users import GetFollowees

chromedriver = "chromedriver"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--incognito")

class UsersBase:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def makeUsersList(self):
        arquivo = open('input.txt', 'r+')
        texto = arquivo.readlines()
        texto.append(self.username)
        arquivo.writelines(texto)
        arquivo.close()
        
        insta = instaloader.Instaloader()
        insta.login(self.username, self.password)  # (login)
        
        # followees = GetFollowees(insta)
        # followees.makeFolloweesCSV()
        users_list = []
        with open('downloads/'+self.username+'.csv') as csvf:
            reader = csv.reader(csvf)
            for row in reader:
                users_list.append(row[0])
        return users_list

class PostPage:
    def __init__(self, driver, page, username, password):
        self.page = page
        self.driver = driver
        self.username = username
        self.password = password
    
    def comment(self):
        self.driver.get(self.page)
        time.sleep(1)
        users_base = UsersBase(self.username, self.password)
        users_list = users_base.makeUsersList()
        for user in users_list:
            try:
                form = self.driver.find_element_by_tag_name('form')
                comment_input = form.find_element_by_tag_name('textarea')
                button = form.find_element_by_tag_name('button')
                comment_input.click()
                pyperclip.copy('@'+str(user))
                pyautogui.hotkey('ctrl','v')
                button.click()
                time.sleep(3)
            except:
                form = self.driver.find_element_by_tag_name('form')
                comment_input = form.find_element_by_tag_name('textarea')
                button = form.find_element_by_tag_name('button')
                time.sleep(40)
                button.click()
                time.sleep(10)
        
class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        time.sleep(1)
        label = self.driver.find_elements_by_tag_name('label')
        username_input = label[0].find_element_by_tag_name('input')
        password_input = label[1].find_element_by_tag_name('input')
        username_input.send_keys(username)
        password_input.send_keys(password)
        button = self.driver.find_elements_by_tag_name('button')
        login_button = button[1]
        login_button.click()
        time.sleep(5)

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get('https://www.instagram.com/')

    def go_to_login_page(self):
        return LoginPage(self.driver)

def main(link, username, password):
    driver = webdriver.Chrome(chromedriver, chrome_options=options)
    home_page = HomePage(driver)
    login_page = home_page.go_to_login_page()
    login_page.login(username, password)

    errors = driver.find_elements_by_css_selector('#error_message')
    assert len(errors) == 0
    
    post_page = PostPage(driver, link, username, password)
    post_page.comment()
    

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Você deve passar usuario e senha como parametros')
    else:
        link = input("Passe o link da postagem: ")
        main(link ,str((sys.argv)[1]), str((sys.argv)[2]))
