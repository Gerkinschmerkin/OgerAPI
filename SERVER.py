from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/networth", methods=["POST"])
def get_networth():
    request_data = request.get_json()
    INGAMENAME = request_data.get("INGAMENAME")
    try:
        urlNW = f"https://sky.shiiyu.moe/stats/{INGAMENAME}"
        responseNW = requests.get(urlNW)

        if responseNW.status_code == 200:
            soup = BeautifulSoup(responseNW.text, "html.parser")
            stat_names = soup.select("span.stat-name")
            for span in stat_names:
                if span.text == "Networth: ":
                    networth_value = span.find_next_sibling("span", class_="stat-value").text
                    NW = networth_value
                    break
            else:
                NW = "not found."
        return jsonify({"networth": NW})
    except Exception as e:
        NW = "not found."
        return jsonify({"networth": NW})

@app.route("/")
def hello_world():
    return "Hello, World!"

