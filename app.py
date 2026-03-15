import json 
import pickle
import numpy as np
from flask import Flask, jsonify , request,render_template
 
from onlinefrauddetection.utils import onlinefrauddetection

app = Flask(__name__)

@app.route("/")
def get_home():
    return render_template("payment.html")

@app.route("/predict_Transaction", methods=["POST"])
def check():
    data = request.form

    try:
        step = int(data.get("step"))
        amount = float(data.get("amount"))
        oldbalanceOrg = float(data.get("oldbalanceOrg"))
        newbalanceOrig = float(data.get("newbalanceOrig"))
        oldbalanceDest = float(data.get("oldbalanceDest"))
        newbalanceDest = float(data.get("newbalanceDest"))
        transaction_type = data.get("type").upper()
    except Exception as e:
        return f"Invalid input: {e}", 400

    obj = onlinefrauddetection(
        step, amount, oldbalanceOrg, newbalanceOrig,
        oldbalanceDest, newbalanceDest, transaction_type
    )

    result = obj.check()  # numeric 0 or 1

    # Convert numeric to string
    if result == 1:
        type_of_transaction = "Fraudulent Transaction"
    else:
        type_of_transaction = "Legitimate Transaction"

    return render_template(
        "payment.html",
        type_of_transaction=type_of_transaction
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0",port = 8000,debug= True)

