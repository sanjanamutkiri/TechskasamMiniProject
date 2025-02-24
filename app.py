from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load food dataset (Sample dataset)
food_data = pd.DataFrame({
    "Meal": ["Breakfast", "Lunch", "Snack", "Dinner"],
    "Food": ["Oatmeal, Banana, Almonds", "Grilled Chicken, Rice, Salad", "Greek Yogurt, Nuts", "Salmon, Quinoa, Vegetables"],
    "Calories": [350, 600, 200, 500]
})

def calculate_calories(weight, height, age, gender, activity):
    """Calculate daily calorie needs using Mifflin-St Jeor Equation."""
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    return round(bmr * activity)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user input
    age = int(request.form['age'])
    gender = request.form['gender']
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    activity = float(request.form['activity'])

    # Calculate daily calorie needs
    daily_calories = calculate_calories(weight, height, age, gender, activity)

    # Recommend diet plan
    total_meal_calories = food_data["Calories"].sum()
    scale_factor = daily_calories / total_meal_calories
    recommended_foods = food_data.copy()
    recommended_foods["Calories"] = (recommended_foods["Calories"] * scale_factor).astype(int)

    return render_template('result.html', daily_calories=daily_calories, meals=recommended_foods.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(debug=True)
