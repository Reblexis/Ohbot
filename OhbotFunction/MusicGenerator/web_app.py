from flask import Flask, render_template, request
import random

app = Flask("__main__", static_folder="C:\\own programs\\music_generator\\static")

genres = []
genresGen = {
  "cllasical": {
    "default": True,
    "title": "Classical music",
  },
  "folk": {
    "default": True,
    "title": "Folk",
  },
  "rap": {
    "default": False,
    "title": "Rap",
  },
  "rock": {
    "default": False,
    "title": "Rock",
  },
  "soundtrack": {
    "default": False,
    "title": "Soundtrack",
  },
  "country": {
    "default": False,
    "title": "Country",
  },
}

for k, v in genresGen.items():
  genres.append(k)
start_dg = random.randint(1, 101)

@app.route("/", methods=["POST", "GET"])
def home():
  #start_dg = random.randint(1, 101)
  to_use = ["classical", "folk", "country"]
  checkBoxes = {}
  for i in genres:
    checkBoxes[i] =""
  if request.method == "POST":
    dg =  request.form["dgf"]
    new_to_use = []
    for i in genres:
      try:
        request.form[i]
        checkBoxes[i] = "checked"
        new_to_use.append(i)
      
      except:
        pass

    to_use = new_to_use
    start_dg = dg
  
  else:
    start_dg = random.randint(1, 101)
    

   

  return render_template("home.html", start_dgf=start_dg, checkBoxes=checkBoxes, genresGen=genresGen)


if __name__ == "__main__":
  app.run(debug=True)




