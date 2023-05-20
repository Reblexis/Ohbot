from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    print(os.getcwd())
    return render_template('menu.html')


if __name__ == "__main__":
    app.run(debug=True)
