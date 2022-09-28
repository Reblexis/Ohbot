import os
import music21 as m21
import random
import json
from keras.utils import to_categorical
import numpy as np
import sys
import pickle


tokens = ["START", "_", "END"]

def open_midi(midi_path):
    mf = m21.midi.MidiFile()
    mf.open(midi_path)
    mf.read()
    mf.close()
    for i in range(len(mf.tracks)):
      mf.tracks[i].events = [ev for ev in mf.tracks[i].events if ev.channel != 10]          

    return m21.midi.translate.midiFileToStream(mf)


seq_len = 30

probs = {}

data_path = r"C:\Users\Tadeas\Downloads\soundtracks"

for i in os.listdir(data_path):
  try:
    song = open_midi(data_path+"\\"+i)

  except:
    print(i)

  key = song.analyze("key")
  if key.mode == "major":
    interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("C"))
  elif key.mode == "minor":
    interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("A"))

  tranposed_song = song.transpose(interval)

  encoded_song = ["START"]


  notes_to_parse = tranposed_song.chordify().recurse().getElementsByClass('Chord')



  for event in notes_to_parse:
        
        symbol = None

        if isinstance(event, m21.chord.Chord):
            
            symbol = ""
            for n ,i in enumerate(event.notes):
              symbol += str(i.pitch.midi)
              if n!= len(event.notes) -1:
                symbol += " "
            if symbol not in tokens:
                tokens.append(symbol)

        
        elif isinstance(event, m21.note.Rest):
            symbol = "r"

        elif(isinstance(event, m21.note.Note)):
          symbol = str(event.pitch.midi)


        if symbol != None:
          if symbol not in tokens:
            tokens.append(symbol)
          
          steps = int(event.duration.quarterLength * 4)
          for step in range(steps):

            if step == 0:
                encoded_song.append(symbol)
            else:
                encoded_song.append("_")

  encoded_song.append("END")

  for j in range(len(encoded_song) - seq_len):
    encoder_sequence = "-".join(encoded_song[j:seq_len+j])
    target_data = encoded_song[j+seq_len]
    if encoder_sequence not in probs:
      probs[encoder_sequence] = {target_data: 1}

    else:
      if target_data in probs[encoder_sequence]:
        probs[encoder_sequence][target_data] += 1

      else:
        probs[encoder_sequence][target_data] = 1

for i in probs:
  den = sum(probs[i].values())
  for j in probs[i]:
    probs[i][j] = probs[i][j] / den
  
  sorted_dict = dict(sorted(probs[i].items(), key=lambda item: item[1], reverse=True))
  probs[i] = sorted_dict



with open("sondtracks_probs.pickle", "wb") as f:
  pickle.dump(probs, f)









  


    


  
