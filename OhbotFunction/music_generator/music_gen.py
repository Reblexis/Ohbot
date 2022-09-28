import music21 as m21
import pickle
import random
import math


genre = "classical"

with open(f"{genre}_probs.pickle", "rb") as f:
  probs = pickle.load(f)

deg_freedom = 0.1

deg_freedom = 1-deg_freedom

stream = m21.stream.Stream()
start_symbol = None
step_counter = 1

print(len(probs))
to_predict_sequence = list(probs)[random.randint(0, len(probs))]

def predict(seq):
  prob = (random.randint(round(list(probs[seq].values())[-1], 2) * 100, 101) * deg_freedom)/100
  for i in probs[seq]:
    if prob >= probs[seq][i]:
        return i

  return random.choice(list(probs[seq]))




def add_to_stream(symbol, dur):
  if symbol == "START" or symbol=="END":
    return
  
  
  if symbol == "r":
    stream.append(m21.note.Rest(quarterLength=dur))


  elif len(symbol.split(" ")) > 1:
    stream.append(m21.chord.Chord([int(i) for i in symbol.split(" ")], quarterLength=dur))

  else:
    stream.append(m21.note.Note(int(symbol), quarterLength=dur))
            


cunter = 1

speed = random.randint(30, 35) /100



for i in to_predict_sequence.split("-"):
  
  if i != "_":
    add_to_stream(i, speed*cunter)
    cunter = 1

  else:
    cunter += 1

  
name = "music_generator\\asus2.mid"

while True:

          if start_symbol == "START" or start_symbol=="END" or len(stream)==2000:
            break

          symbol = predict(to_predict_sequence)
       
          if symbol != "_":

      
                if start_symbol is not None:

                    quarter_length_duration = speed * step_counter 

                    add_to_stream(start_symbol, quarter_length_duration)

                    step_counter = 1

                start_symbol = symbol

        
          else:
            step_counter += 1

          to_predict_sequence += "-"+symbol
          to_predict_sequence = "-".join(to_predict_sequence.split("-")[1:])


stream.write("midi", name)