from selenium import webdriver

# change the path

import os    

chromedriver = "/Users/anoopsana/Downloads/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

# driver = webdriver.PhantomJS(executable_path='C:\phantomjs-2.1.1-windows\\bin\phantomjs.exe')

driver.get("https://apm.activecommunities.com/recsportsvirginia/Facility_Search")


facility_court={}
facilities = [] # added to keep track of each facility
text_list=[]
sele_list=(driver.find_element_by_css_selector('table').find_elements_by_css_selector('td'))
for text in sele_list:
    text_list.append(text.text.strip())


for i in range(int(len(text_list)/4)):
    court=text_list[4*i].split("\n")[0]
    facility=text_list[4*i+2]
    type = text_list[4 * i + 1]
    if facility not in facility_court:
        facility_court[facility]=[[court, type]]
        facilities.append([facility]) # added to keep track of each facility
    else:
        facility_court[facility].append([court, type])


try:
    j=2
    while True:
        driver.get("https://apm.activecommunities.com/recsportsvirginia/Facility_Search?Page="+str(j))
        sele_list=(driver.find_element_by_css_selector('table').find_elements_by_css_selector('td'))
        for text in sele_list:
            text_list.append(text.text.strip())


        for i in range(int(len(text_list)/4)):
            court=text_list[4*i].split("\n")[0]
            type=text_list[4*i+1]
            facility=text_list[4*i+2]
            if facility not in facility_court:
                facility_court[facility]=[[court, type]]
                facilities.append([facility]) # added to keep track of each facility
            else:
                facility_court[facility].append([court, type])
        j+=1

except:
    1


driver.close()

cor = []
cor2 = []
courts = []
fac_count = []

# this loop gets each court out without repetitions and puts into cor
for i in range(0, len(facility_court)):
        facility = facilities[i][0]
        for j in range(0, len(facility_court.get(facility) )):
            curr = ((facility_court.get(facility))[j])
            if(curr[0] not in cor):
                cor.append(curr[0])
                cor2.append(curr[1])
                fac_count.append(facility)
                # courts[j].append(curr[1])

# this loops actually puts them into courts as list format
for i in range(0, len(cor)):
    courts.append([cor[i]])
    courts[i].insert(0, i+10)
    courts[i].append(cor2[i])
    courts[i].append(0)
    courts[i].append(fac_count[i])
    


