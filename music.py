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
import math


notes2 = [165, 110,  73, 69, 55, 35, 28, 21, 14]
noteskey2 = ["dotted1/8",  "1/8", "tripletnote", "dotted1/16", "1/16", "dotted1/32", "1/32", "dotted1/64", "1/64"]


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




def closest(lst, K):
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]




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
# try:
for msg in mid.play():
    Pitch = driver.find_element(By.XPATH, '//*[@id="idTbodyMidiData"]/tr['+ str(num) + ']/td[2]').text
    Velocity = driver.find_element(By.XPATH, '//*[@id="idTbodyMidiData"]/tr['+ str(num) + ']/td[3]').text
    Duration = driver.find_element(By.XPATH, '//*[@id="idTbodyMidiData"]/tr['+ str(num) + ']/td[4]').text
    if (Duration.find(':') != -1):
        Duration1 = (Duration.split(":")[0])
        Duration2 = (Duration.split(":")[1])
        if 0 < int(Duration1):
            Note1 = int(Duration1) * 220
        else:
            Note1 = 0
        
        if 0 < int(Duration2):
            Note2 = (closest(notes2, int(Duration2)))
        else:
            Note2 = 0

        Note = (Note1 + Note2)
    else:
        if 0 < int(Duration):
            Note = (closest(notes2, int(Duration)))
        else:
            Note = 0

    MBT = driver.find_element(By.XPATH, '//*[@id="idTbodyMidiData"]/tr['+ str(num) + ']/td[1]').text
    M = (MBT.split(":")[0])
    B = (MBT.split(":")[1])
    T = (MBT.split(":")[2])
    new_MBT = int(T) + int(Note)
    if new_MBT >= 220:
        new_B = math.floor(new_MBT / 220 + int(B))
        new_T = new_MBT % 220
        if new_B > 4:
            new_M = int(M) + 1 #Fix this, new_B isn't always 1, it needs to be able to be higher that 1. M needs to work with multiple measure changes
            new_B = 1
        else:
            new_M = M
    else:
        new_M = int(M)
        new_B = int(T)
        new_T = int(T) + int(Note)

    tup1 = (M)
    tup2 = (B)
    tup3 = (T)
    tup4 = (Pitch)
    tup5 = (Velocity)
    tup6 = (Note)
    tup7 = (new_M)
    tup8 = (new_B)
    tup9 = (new_T)
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writerow([tup1, tup2, tup3, tup4, tup5, tup6, tup7, tup8, tup9])
    num += 1
    # web_tempo = driver.find_element(By.XPATH, '//*[@id="idTxtTempo"]')
    # tempo = web_tempo.get_attribute("value")
    # print(tempo)
    # time.sleep(2)
# except:
#     print("done filling out csv")




#used for downloading midi file, renaming it, and moving it into this folder from website

#driver.find_element(By.XPATH, '//*[@id="idDivMain"]/table/tbody/tr/td[3]/div[1]/table/tbody/tr/td[2]/input').click()

# prevName = 'D:\\taren\\Downloads\\OnlineMidi.mid'
# newName = 'D:\\taren\\Downloads\\' + file
# os.rename(prevName, newName)
# os.remove('C:\\Users\\taren\\Documents\\GitHub Repositories\\Musical-Motors\\' + file)
# shutil.move('D:\\taren\\Downloads\\' + file, 'C:\\Users\\taren\Documents\\GitHub Repositories\\Musical-Motors')


#bps = beats per second
# bps = int(tempo) / 60#seconds



# with open('music.csv', 'r') as csv_file:
#     csv_reader = csv.reader(csv_file)
#     consecutive = [0]
#     num_threads = 0
#     new_MBT = 0
#     for line in csv_reader:
        





    #     if line[1] != consecutive[0]:
    #         current = len(consecutive)
    #         if current >= num_threads:
    #             num_threads = current
    #         consecutive = [line[1]]
    #     else:
    #         consecutive.append(line[1])

    # for i in range(num_threads):
    #     globals()[f"list{i}"] = []
    

# with open('music.csv', 'r') as csv_:
#     reader = csv.reader(csv_)
#     consecutiveM = [0]
#     consecutiveB = [0]
#     for line in reader:
#         if line[0] == consecutiveM[0]:
#             if line[1] == consecutiveB[0]:
#                 globals()[f"list{len(consecutiveB)}"].append(line)
#         else:
#             globals()[f"list{0}"].append(line)
#             consecutiveM = [line[0]]
#             consecutiveB = [line[1]]
#     print(globals()[f"list{0}"])
#     print(globals()[f"list{1}"])
#     print(globals()[f"list{2}"])
#     print(globals()[f"list{3}"])
#     print(globals()[f"list{4}"])
#     print(globals()[f"list{5}"])


#Create sorting algo to make sure each note in a chord has its own thread

# def music_thread(thread):
#     print(sdad)


# for i in num_threads:
#     "T" + str(i) = threading.Thread(target=music_thread, args=("T" + str(i), globals()['list%s' % i]))

