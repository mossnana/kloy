# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import re
import csv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

lyric_paths = [
  '/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[1]/div[2]',
  '/html/body/div[7]/div/div[8]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[1]/div[2]',
]
button_path=  '/html/body/div[4]/div[2]/form/div[1]/div[1]/div[2]/button'
def url(title):
  return 'https://www.google.com/search?q={}+{}'.format(title, 'เนื้อเพลง')

dc = DesiredCapabilities.CHROME
dc['goog:loggingPrefs'] = { 'browser':'ALL' }
driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=dc)
driver.get("https://google.com")
words = [
  "ไม่เคย",
  "หากฉันตาย",
  "ไม่ผิดหรอกเธอ","แค่ได้รักเธอ","ทั้งที่ผิดก็ยังรัก","นอกจากชื่อฉัน","ก็ยังเป็นเธอ","ขอเวลาลืม","ไม่บอกเธอ","กอดไม่ได้","รักมือสอง","ไม่เดียงสา","ลมเปลี่ยนทิศ","อยากเจอ","KoisuruFortuneCookieคุกกี้เสี่ยงทาย","คนบาป","สาธุ","ต่าง","ปฏิเสธไม่ได้ว่ารักเธอ","ปล่อยMiss","คุกเข่า","เธอ","ช่างมัน","โปรดเถิดรัก","คู่ชีวิต","เธอทำให้ฉันเสียใจ","ดึงดัน","หมอก","ขัดใจ","ยอมปล่อย","ไม่เหมือนใคร","Galaxy","กลับตัวกลับใจ","จำเลยรัก","เสือสิ้นลาย","มีแค่เรา","โอเคป่ะ?YesorNo","คนโดนเท","ห้องนอน","เกาะสวาทหาดสวรรค์","รักได้ป่าว","ความเงียบดังที่สุด","คำถามซึ่งไร้คนตอบ","ไกลแค่ไหนคือใกล้","อยู่ตรงนี้นานกว่านี้","คนไม่จำเป็น","คนทางนั้น","ถอย","แผลในใจ","เพราะเธอยังลืมเขาไม่ได้","วาฬเกยตื้น","Unfriend","รักติดไซเรน","ถ้าฉันเป็นเขา","ขอโทษหัวใจ","ปลิว","คนละชั้น","เธอเก่ง","สิ่งของ","คำยินดี","ให้นานกว่าที่เคย","ใจกลางเมือง","พลังงานจน","แพ้ทาง","ฉันก็คง","เชือกวิเศษ","Morning","กฎของคนแพ้","สะใจเธอแล้วใช่ไหมสาใจเธอพอหรือยัง","ขอ","ซมซาน","เรื่องที่ขอ","ไวน์","วันหนึ่งฉันเดินเข้าป่า","หมายความว่าอะไร","ซาโยนาระ","ใจความสำคัญ","อยากให้เธอลอง","ปล่อย","ปล่อยมือฉัน","ตามตะวัน","ทุ่มหมดตัว","รู้ทั้งรู้","เป็นไรไหม?","ByeBye","ซ่อนกลิ่น","ทิ้งไว้กลางทาง","ทางผ่าน","เหนื่อยไหมหัวใจ","ความจริง","อย่าให้ฉันคิด","เป็นทุกอย่าง","บอกตัวเอง","ฉันมาบอกว่า","พูดไม่คิด","Event","แหลก","เรื่องจริง","เคลิ้ม","ขอวอน2Togetherii","ทน","คิดถึงฉันไหมเวลาที่เธอ","ThankYouForYourLove","เจ็บที่ต้องรู้","I'msorryสีดา","ลาลาลอย100%","ที่ระทึกReminder","เตือนแล้วนะLoveWarning","คิดแต่ไม่ถึง","คำหวานที่เธอไม่เอา","เค้าก่อน","แบกไม่ไหว","วายร้าย","ช่วยไม่ได้","เก็บทรงไม่อยู่","ถามหน่อย","เอ็นดู","อยากรู้หัวใจตัวเอง","ลืมไป","เจ็บจนพอ","อยู่ดีๆก็…","เฉยเมย","ธารารัตน์","ดูไว้","หัวใจทศกัณฐ์Devil'sHeart","หนังสือเล่มเก่า","มือลั่น","24พฤษภา","การเดินทาง","รักเธอคนเดียวONELOVE","เธอมีฉันฉันมีใคร","สองใจ","เมาทุกขวดเจ็บปวดทุกเพลง","อยากนอนกับเธอ","ไม่สนโลก","แต่งงานกันนะ","รักเราไม่เก่าเลย","ช่วยกอดฉันที","นานานานานา","ปิดตาข้างนึง","ตายก่อน","ขาดเธอขาดใจ","ไม่ไหวบอกไหว","เธอเปลี่ยนไป","พื้นที่ทับซ้อน","ยังไกล","ภาพจำ","Undo","ปล่อย","ทุกคนเคยร้องไห้","ภูมิแพ้กรุงเทพ","กรรม","คนมีเสน่ห์","สะพานไม้ไผ่","ตราบธุลีดิน","แลรักนิรันดร์กาล","ขอโทษ","ใครคนนั้น","ลูกอม","รักกินไม่ได้","หรือมันไม่มีอยู่จริง","คงไม่ทัน","ช้ำคือเรา","รถของเล่น","อ้าว","PLEASE","ทางของฝุ่นDust","เก็บรัก","ชู้ทางไลน์","เมรี","ขอใจเธอแลกเบอร์โทร","มะล่องก่องแก่ง","เต่างอย","เลิกคุยทั้งอำเภอเพื่อเธอคนเดียว","บักแตงโม","คำแพง","ผู้สาวขาเลาะ"
]
lyrics = []
words_and_lyrics = []
csv = ''

for word in words:
  lyric = ''
  driver.get(url(word))
  sleep(3)
  for lyric_path in lyric_paths:
    try:
      lyric_node = driver.find_element_by_xpath(lyric_path)
    except:
      pass
  try:
    spans = lyric_node.find_elements_by_tag_name('span')
    for span in spans:
      lyric = "{}{}".format(lyric, span.get_attribute('innerHTML'))
  except:
    pass
  lyrics.append(lyric)
  sleep(2)
file = open("xxx3.csv", "w")
count = 0
for word in words:
    file.write("{},{}\n".format(word,lyrics[count]))
    count += 1
file.close()
