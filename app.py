from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_exchange_rates(base_currency="USD"):
    url = f"https://open.er-api.com/v6/latest/{base_currency.upper()}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    return data["rates"] if data["result"] == "success" else None

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    rates = get_exchange_rates("USD")  # Load default rates for dropdown
    currencies = sorted(rates.keys()) if rates else []

    if request.method == "POST":
        amount = float(request.form["amount"])
        base = request.form["base_currency"]
        target = request.form["target_currency"]
        rates = get_exchange_rates(base)
        if not rates:
            error = "Could not fetch exchange rates."
        elif base not in rates or target not in rates:
            error = "Invalid currency code."
        else:
            converted = amount * rates[target]
            result = f"{amount} {base} = {converted:.2f} {target}"

    return render_template("index.html", result=result, currencies=currencies, error=error)

if __name__ == "__main__":
    app.run(debug=True)