from flask import Flask, render_template, request, redirect
import json, os

app = Flask(__name__)
FILE = "data.json"

income = 0
expenses = {"Need": [], "Want": [], "Save": []}
budget = {"Need": 0, "Want": 0, "Save": 0}

def load():
    global income, expenses, budget
    try:
        if os.path.exists(FILE):
            with open(FILE, "r") as f:
                data = json.load(f)

                income = data.get("income", 0)
                expenses = data.get("expenses") or {"Need": [], "Want": [], "Save": []}
                budget = data.get("budget") or {"Need": 0, "Want": 0, "Save": 0}

    except Exception as e:
        print("LOAD ERROR:", e)
        income = 0
        expenses = {"Need": [], "Want": [], "Save": []}
        budget = {"Need": 0, "Want": 0, "Save": 0}
def save():
    json.dump({
        "income": income,
        "expenses": expenses,
        "budget": budget
    }, open(FILE, "w"))

load()

@app.route("/")
def home():
    summary = {}
    for c in budget:
        spent = sum(i[1] for i in expenses[c])
        summary[c] = {
            "budget": budget[c],
            "spent": spent,
            "remaining": budget[c] - spent
        }
    return render_template("index.html",
                           income=income,
                           budget=budget,
                           expenses=expenses,
                           summary=summary)

@app.route("/income", methods=["POST"])
def set_income():
    global income
    income = float(request.form["income"])
    save()
    return redirect("/")

@app.route("/budget", methods=["POST"])
def set_budget():
    budget["Need"] = float(request.form["need"])
    budget["Want"] = float(request.form["want"])
    budget["Save"] = float(request.form["save"])
    save()
    return redirect("/")

@app.route("/add", methods=["POST"])
def add():
    cat = request.form["cat"]
    name = request.form["name"]
    amt = float(request.form["amt"])
    expenses[cat].append((name, amt))
    save()
    return redirect("/")

@app.route("/delete/<cat>/<int:index>")
def delete(cat, index):
    if 0 <= index < len(expenses[cat]):
        expenses[cat].pop(index)
        save()
    return redirect("/")

@app.route("/edit", methods=["POST"])
def edit():
    cat = request.form["cat"]
    index = int(request.form["index"])
    name = request.form["name"]
    amt = float(request.form["amt"])
    if 0 <= index < len(expenses[cat]):
        expenses[cat][index] = (name, amt)
        save()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
