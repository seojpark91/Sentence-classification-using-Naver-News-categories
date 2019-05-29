from flask import *
import pickle
import numpy as np

app = Flask(__name__)

models = {}

def init():
    with open("./models/classification.pkl", "rb") as f:
        models["classification"] = pickle.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predic", methods=["POST","GET"])
def predic():
    result = {}
    result["category"] = [ "정치", "경제", "사회", "생활/문화", "세계", "IT/과학"]

    model = models["classification"]

    # URL Query - ?setence=문자열
    sentence = request.values.get("sentence")

    result["result"] = list(np.round_(model.predict_proba([sentence])[0]*100, 2))

    return jsonify(result)

init()

app.run(debug=True)
