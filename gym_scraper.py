# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 16:43:17 2018

@author: Habib K
"""
import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os    

chromedriver = "/Users/anoopsana/Downloads/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

# driver = webdriver.PhantomJS(executable_path='C:\phantomjs-2.1.1-windows\\bin\phantomjs.exe')
gym_url = "https://recsports.virginia.edu/#expand-"
gyms = ['NGRC', 'AFC', 'MG', 'SRC', 'Snyder', 'Squash']

#with open('result.csv', 'w') as f:
 #   f.write("Gym, Phone, Address, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday \n")
    
driver.get(gym_url+gyms[0])
number = driver.find_elements_by_xpath('//span[@class="phone-number"]') 
address = driver.find_elements_by_xpath('//span[@class="address"]') 
time = driver.find_elements_by_xpath('//div[@class="facility-hours"]') 
monday = []
tuesday = []
wednesday = []
thursday = []
friday = []
saturday = []
sunday = []
ng = []
afc = []
mem = []
src = []
a = []  
p= []  
ngp = []

for s in range(len(time)):
    a.append(time[s].get_attribute('textContent').split("\n")[2])
    # print(time[s].get_attribute('textContent').split("\n")[2])
    if s<7:
        ng.append(time[s].get_attribute('textContent').split("\n")[2])
    elif s<14:
        afc.append(time[s].get_attribute('textContent').split("\n")[2])
    elif s<21:
        mem.append(time[s].get_attribute('textContent').split("\n")[2])
    else:
        src.append(time[s].get_attribute('textContent').split("\n")[2])
        
#with open('result.csv', 'a') as f:
for i in range(6):
    n = number[i].get_attribute('textContent')
    addy = address[i].get_attribute('textContent').split(",")[0]
    if i == 0:
        North_Grounds = {'name': gyms[i], 'phone number': n, 'address': 'Address: 510 Massie Rd', 'monday': ng[0], 'tuesday': ng[1], 'wednesday': ng[2], 'thursday': ng[3], 'friday': ng[4], 'saturday': ng[5], 'sunday':ng[6]}
            #f.write(gyms[i] + "," + n + "," + "510 Massie Rd" + "," + ng[0] + "," + ng[1] + "," + ng[2] + "," + ng[3] + "," + ng[4] + "," + ng[5] + "," + ng[6] + "\n")
    elif i == 1:
        Aquatic_Fitness_Center = {'name': gyms[i], 'phone number': n, 'address': addy, 'monday': afc[0], 'tuesday': afc[1], 'wednesday': afc[2], 'thursday': afc[3], 'friday': afc[4], 'saturday': afc[5], 'sunday':afc[6]}
            #f.write(gyms[i] + "," + n + "," + addy + "," + afc[0] + "," + afc[1] + "," + afc[2] + "," + afc[3] + "," + afc[4] + "," + afc[5] + "," + afc[6] + "\n")
    elif i == 2:
        Memorial_Gym = {'name': gyms[i], 'phone number': n, 'address': addy, 'monday': mem[0], 'tuesday': mem[1], 'wednesday': mem[2], 'thursday': mem[3], 'friday': mem[4], 'saturday': mem[5], 'sunday':mem[6]}
            #f.write(gyms[i] + "," + n + "," + addy + "," + mem[0] + "," + mem[1] + "," + mem[2] + "," + mem[3] + "," + mem[4] + "," + mem[5] + "," + mem[6] + "\n")
    elif i == 3:
        Slaughter = {'name': gyms[i], 'phone number': n, 'address': addy, 'monday': src[0], 'tuesday': src[1], 'wednesday': src[2], 'thursday': src[3], 'friday': src[4], 'saturday': src[5], 'sunday':src[6]}
            #f.write(gyms[i] + "," + n + "," + addy + "," + src[0] + "," + src[1] + "," + src[2] + "," + src[3] + "," + src[4] + "," + src[5] + "," + src[6] + "\n")
    elif i == 4:
        Snyder = {'name': gyms[i], 'phone number': 'Not Available', 'address': addy, 'monday': 'Dusk to Midnight', 'tuesday': 'Dusk to Midnight', 'wednesday': 'Dusk to Midnight', 'thursday': 'Dusk to Midnight', 'friday': 'Dusk to Midnight', 'saturday': 'Dusk to Midnight', 'sunday': 'Dusk to Midnight'}
# driver.close()


# driver = webdriver.Chrome(executable_path="C:\\Users\\Hobie\\Downloads\\chromedriver_win32\\chromedriver.exe")
driver.get(gym_url+gyms[1])
pool = driver.find_elements_by_xpath('//div[@class="pool-hours"]') 
for s in range(0,7):
    ngp.append(pool[s].get_attribute('textContent').split("\n")[2])
NGRC_pool = {'monday':ngp[0], 'tuesday':ngp[1], 'wednesday':ngp[2], 'thursday':ngp[3], 'friday':ngp[4], 'saturday':ngp[5], 'sunday':ngp[6]}
for s in range(7,14):
    p.append(pool[s].get_attribute('textContent').split("\n")[2])
AFC_pool = {'monday':p[0], 'tuesday':p[1], 'wednesday':p[2], 'thursday':p[3], 'friday':p[4], 'saturday':p[5], 'sunday':p[6]}
driver.close()
