from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_emi(loan_amount, annual_rate, tenure_years):
    monthly_rate = annual_rate / (12 * 100)
    tenure_months = tenure_years * 12

    emi = (loan_amount * monthly_rate * (1 + monthly_rate) ** tenure_months) / \
          ((1 + monthly_rate) ** tenure_months - 1)

    total_payment = emi * tenure_months
    total_interest = total_payment - loan_amount

    return round(emi, 2), round(total_interest, 2), round(total_payment, 2)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        total_amount = float(request.form["total_amount"])
        down_payment = float(request.form["down_payment"])
        interest_rate = float(request.form["interest_rate"])
        duration = int(request.form["duration"])

        loan_amount = total_amount - down_payment

        emi, interest, total_payment = calculate_emi(
            loan_amount, interest_rate, duration
        )

        result = {
            "loan_amount": loan_amount,
            "emi": emi,
            "interest": interest,
            "total_payment": total_payment
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
