import os
from flask import Flask, render_template, request, session
import requests

app = Flask(__name__)
app.secret_key = "raihanxsk" 
API_KEY = "799c8b7ad273ae589402bde2966c077f" 

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None

    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        city = request.form["city"]
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "city": city.title(),
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"].title(),
                "icon": data["weather"][0]["icon"]
            }

            if city.title() not in session["history"]:
                session["history"].append(city.title())
                session.modified = True
        else:
            weather_data = {"error": "City not found."}

    return render_template("index.html", weather=weather_data, history=session["history"])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
