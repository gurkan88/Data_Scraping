from bs4 import BeautifulSoup as bs
from datetime import datetime
from selenium import webdriver
import pandas as pd
import numpy as np
import time


start = datetime.now()

driver = webdriver.Chrome(executable_path='chromedriver.exe')

url = "https://www.nytimes.com/crosswords/game/mini"
driver.get(url)

time.sleep(5)

driver.find_element_by_css_selector('button.xwd__modal--subtle-button').click()

element = driver.find_element_by_css_selector('section.xwd__layout--cluelists')
text_html = bs(element.get_attribute('innerHTML'), 'html.parser')

driver.close()

end = datetime.now()

print(f'Runtime of the program is: {end - start}')

data_dict = {data.h3.text: [[label.text for label in data.find_all(class_='xwd__clue--label')],\
    [clue.text for clue in data.find_all(class_='xwd__clue--text xwd__clue-format')]] for data in text_html.contents}

groups = [group for group in list(data_dict.keys()) for i in range(5)]
numbers = [j for i in ['Across', 'Down'] for j in data_dict[i][0]]
strings = [j for i in ['Across', 'Down'] for j in data_dict[i][1]]

df = pd.DataFrame(data={'group': groups, 'number': numbers, 'string': strings})
df.to_json('ny_times_cw.json')


for k, v in data_dict.items():
    print(f'=== {k} ===')
    for label, clue in zip(v[0], v[1]):
        print(label+'.', clue)
