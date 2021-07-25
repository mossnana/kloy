from selenium import webdriver
from time import sleep
import re
import csv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

print('Enter csv filename')
path = input()

dc = DesiredCapabilities.CHROME
dc['goog:loggingPrefs'] = { 'browser':'ALL' }
driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=dc)
driver.get("https://mossnana.github.io/kloy")
sleep(5)
filename = driver.find_element_by_xpath('/html/body/input')
lyric = driver.find_element_by_xpath('/html/body/textarea')
button = driver.find_element_by_xpath('/html/body/button')

songs = []

with open(path, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        songs.append({
          'title': row[0],
          'lyric': row[1],
        })

for song in songs:
  filename.clear()
  lyric.clear()
  filename.send_keys(song['title'])
  lyric.send_keys(song['lyric'])
  button.click()
  sleep(5)
