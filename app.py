from flask import Flask, render_template, request, redirect
import json, os

app = Flask(__name__)

FILE = "data.json"

# default data
income = 0
expenses = {"Need": [], "Want": [], "Save": []}
budget = {"Need": 0, "Want": 0, "Save": 0}

# SAFE LOAD
def load():
    global income, expenses, budget
    try:
        if os.path.exists(FILE):
            with open(FILE, "r") as f:
                data = json.load(f)

                income = data.get("income", 0)
                expenses = data.get("expenses", {"Need": [], "Want": [], "Save": []})
                budget = data.get("budget", {"Need": 0, "Want": 0, "Save": 0})
    except Exception as e:
        print("Error loading:", e)

# SAFE SAVE
def save():
    try:
        with open(FILE, "w") as f:
            json.dump({
                "income": income,
                "expenses": expenses,
                "budget": budget
            }, f)
    except Exception as e:
        print("Error saving:", e)

load()

@app.route("/")
def home():
    summary = {}

    for c in ["Need", "Want", "Save"]:
        spent = sum(i[1] for i in expenses.get(c, []))
        summary[c] = {
            "budget": budget.get(c, 0),
            "spent": spent,
            "remaining": budget.get(c, 0) - spent
        }

    return render_template("index.html",
                           income=income,
                           summary=summary,
                           expenses=expenses)

@app.route("/income", methods=["POST"])
def set_income():
    global income
    try:
        income = float(request.form.get("income", 0))
        save()
    except:
        pass
    return redirect("/")

@app.route("/budget", methods=["POST"])
def set_budget():
    try:
        budget["Need"] = float(request.form.get("need", 0))
        budget["Want"] = float(request.form.get("want", 0))
        budget["Save"] = float(request.form.get("save", 0))
        save()
    except:
        pass
    return redirect("/")

@app.route("/add", methods=["POST"])
def add():
    try:
        cat = request.form.get("cat")
        name = request.form.get("name")
        amt = float(request.form.get("amt", 0))

        if cat in expenses:
            expenses[cat].append((name, amt))
            save()
    except:
        pass

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
