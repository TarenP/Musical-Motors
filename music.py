import os
import glob
from music21 import *
import re
import pandas as pd
import mido
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import shutil
import csv
import threading

filetype = int(input("1 for .mid filetype, 2 for .wav filetype "))

if filetype == 2:
    files = glob.glob("*.wav")

    number = 0
    for x in files:
        number += 1
        print(str(number) + '.' + " for " + str(x))

    file_num = int(input("File: "))
    file = files[file_num - 1]
    os.system("omnizart music transcribe "  + file)
    file = re.sub(".wav", ".mid", file)
    print(file)
else:
    files = glob.glob("*.mid")

    number = 0
    for x in files:
        number += 1
        print(str(number) + '.' + " for " + str(x))

    file_num = int(input("choose: "))
    file = files[file_num - 1]
    print(file)
try:
    os.remove("music.csv")
except:
    print("no csv file.")
    
f = open("music.csv", "a", newline="")

#Upload newly generated midi file to a midi editor webpage and then create file that contains the contents of each row of the table
driver = webdriver.Chrome('chromedriver.exe')
driver.get('https://www.onlinemidi.com/Editor.php')

element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "idDivTitle"))
)
time.sleep(5)
element = driver.find_element(By.XPATH, '//*[@id="filereader"]')
element.send_keys("C:\\Users\\taren\Documents\\GitHub Repositories\\Musical-Motors\\" + file)
time.sleep(2)
mid = mido.MidiFile(file)
num = 1
try:
    for msg in mid.play():
        MBT = driver.find_element(By.XPATH, '//*[@id="idTbodyMidiData"]/tr['+ str(num) + ']/td[1]').text
        M = (MBT.split(":")[0])
        B = (MBT.split(":")[1])
        T = (MBT.split(":")[2])
        #print(MBT)
        Pitch = driver.find_element(By.XPATH, '//*[@id="idTbodyMidiData"]/tr['+ str(num) + ']/td[2]').text
        #print(Pitch)
        Velocity = driver.find_element(By.XPATH, '//*[@id="idTbodyMidiData"]/tr['+ str(num) + ']/td[3]').text
        #print(Velocity)
        Duration = driver.find_element(By.XPATH, '//*[@id="idTbodyMidiData"]/tr['+ str(num) + ']/td[4]').text
        Duration = (MBT.split(":")[0])
        #print(Duration)
        tup1 = (M)
        tup2 = (B)
        tup3 = (T)
        tup4 = (Pitch)
        tup5 = (Velocity)
        tup6 = (Duration)
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow([tup1, tup2, tup3, tup4, tup5, tup6])
        num += 1
except:
    print("done filling out csv")

web_tempo = driver.find_element(By.XPATH, '//*[@id="idTxtTempo"]')
tempo = web_tempo.get_attribute("value")
print(tempo)
time.sleep(2)


#used for downloading midi file, renaming it, and moving it into this folder from website

#driver.find_element(By.XPATH, '//*[@id="idDivMain"]/table/tbody/tr/td[3]/div[1]/table/tbody/tr/td[2]/input').click()

# prevName = 'D:\\taren\\Downloads\\OnlineMidi.mid'
# newName = 'D:\\taren\\Downloads\\' + file
# os.rename(prevName, newName)
# os.remove('C:\\Users\\taren\\Documents\\GitHub Repositories\\Musical-Motors\\' + file)
# shutil.move('D:\\taren\\Downloads\\' + file, 'C:\\Users\\taren\Documents\\GitHub Repositories\\Musical-Motors')


#bps = beats per second
# bps = int(tempo) / 60#seconds

with open('music.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    consecutive = [0]
    num_threads = 0
    for line in csv_reader:
        if line[1] != consecutive[0]:
            current = len(consecutive)
            if current >= num_threads:
                num_threads = current
            consecutive = [line[1]]
        else:
            consecutive.append(line[1])

#Create sorting algo to make sure each note in a chord has its own thread

def music_thread(thread):
    print(sdad)

    
for i in num_threads:
    "T" + str(i) = threading.Thread(target=music_thread, args=("T" + str(i), "list" + str(i)))

