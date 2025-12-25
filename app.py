from flask import Flask, render_template, request, redirect, url_for
from model_functions import predict_state_places
import pickle
from urllib.parse import urlencode

app = Flask(__name__)

# Load dataset
with open("tourism_df.pkl", "rb") as f:
    df = pickle.load(f)

# Dropdown options
WEATHER_OPTIONS = ["Pleasant", "Warm", "Cool"]
CROWD_OPTIONS = ["Low", "Medium", "High"]
BUDGET_OPTIONS = ["Low", "Medium", "High"]
FAMOUS_OPTIONS = sorted(df["Famous_For"].dropna().unique())

@app.route("/", methods=["GET","POST"])
def welcome():
    return render_template("welcome.html")

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    # Get query params
    selected = {
        "weather": request.args.get("weather",""),
        "crowd": request.args.get("crowd",""),
        "famous_for": request.args.get("famous_for",""),
        "budget": request.args.get("budget","")
    }
    result = {}

    if request.method == "POST":
        # Update selected from form
        selected["weather"] = request.form.get("weather")
        selected["crowd"] = request.form.get("crowd")
        selected["famous_for"] = request.form.get("famous_for")
        selected["budget"] = request.form.get("budget")

        # Redirect with query params to preserve fields
        query = urlencode(selected)
        return redirect(url_for("dashboard")+"?"+query)

    # Predict only if all fields are selected
    if all(selected.values()):
        result = predict_state_places(df,
                    weather=selected["weather"],
                    crowd=selected["crowd"],
                    famous_for=selected["famous_for"],
                    budget=selected["budget"])

        if not result:
            # No suggestions found
            return render_template("no_result.html", selected=selected)

    return render_template("dashboard.html",
                           result=result,
                           selected=selected,
                           weather_options=WEATHER_OPTIONS,
                           crowd_options=CROWD_OPTIONS,
                           budget_options=BUDGET_OPTIONS,
                           famous_options=FAMOUS_OPTIONS)

@app.route("/state/<state>")
def state_page(state):
    state = state.replace("%20"," ")  # decode spaces

    # Preserve filters
    selected = {
        "weather": request.args.get("weather",""),
        "crowd": request.args.get("crowd",""),
        "famous_for": request.args.get("famous_for",""),
        "budget": request.args.get("budget","")
    }

    result = predict_state_places(df)
    places = result.get(state, [])

    return render_template("state.html",
                           state=state,
                           places=places,
                           selected=selected)

if __name__=="__main__":
    app.run(debug=True)
