from flask import Flask, render_template, request, make_response
from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)
app.debug = True

booking = [
    {
        "booking_id": "1021",
        "name": "John Smith",
        "date": "01-11-2022",
        "time": "12:00"
    }
]

@app.route("/")
def index():
  return render_template("homepage.html")

@app.route("/thank")
def thank():
  return render_template("thank.html")

@app.route("/book", methods=["POST"])
def foo():
    return "Got POST request to /book endpoint", 201
    

if __name__ == "__main__":
  app.run()
