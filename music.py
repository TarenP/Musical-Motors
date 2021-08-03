import os
import glob
from music21 import *
import re
import pandas as pd
import mido
import pygame
from selenium import webdriver

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




driver = webdriver.Chrome('chromedriver.exe')
driver.get('https://www.onlinemidi.com/Editor.php')





keyboard_instruments = ["KeyboardInstrument", "Piano", "Harpsichord", "Clavichord", "Celesta", ]
path = file
def get_notes_chords_rests(instrument_type, path):
    try:
        midi = converter.parse(path)
        parts = instrument.partitionByInstrument(midi)
        note_list = []
        for music_instrument in range(len(parts)):
            if parts.parts[music_instrument].id in instrument_type:
                for element_by_offset in stream.iterator.OffsetIterator(parts[music_instrument]):
                    for entry in element_by_offset:
                        if isinstance(entry, note.Note):
                            note_list.append(str(entry.pitch))
                        elif isinstance(entry, chord.Chord):
                            note_list.append('.'.join(str(n) for n in entry.normalOrder))
                        elif isinstance(entry, note.Rest):
                            note_list.append('Rest')
        return note_list
    except Exception as e:
        print("failed on ", path)
        pass

 #create a function for taking parsing and extracting the notes
def extract_notes(path):
    mid = mido.MidiFile(path)
    num = 0
    for msg in mid.play():
        if num > 0:
            print(msg.note)
        num += 1

#  #write to csv
# def to_csv(notes_array):
#      df = pd.DataFrame(notes_array, index=None, columns=None)
#      df.to_csv("pirates.csv")

 #using the functions
notes_array = extract_notes(path)
#print(notes_array)

#notes = get_notes_chords_rests(keyboard_instruments, path)
#print(notes)

