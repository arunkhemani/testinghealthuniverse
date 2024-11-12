import streamlit as st
import pandas as pd
import plotly.express as px

# Step 1: College selection
st.title("Health Universe Dining Menu Tracker")
college = st.selectbox("Select Your College", ["Bentley University", "Northeastern University"])

# Define sample menus with nutritional information, including calories
bentley_menu = {
    'Food Item': [
        'Grilled Chicken Breast', 'Brown Rice', 'Steamed Broccoli', 'Caesar Salad',
        'Apple', 'Scrambled Eggs', 'Salmon Fillet', 'Greek Yogurt', 'Roasted Sweet Potatoes', 'Tofu Stir-Fry'
    ],
    'Protein (g)': [30, 2, 2, 5, 0, 12, 25, 10, 2, 8],
    'Carbs (g)': [0, 45, 7, 12, 25, 1, 0, 15, 27, 20],
    'Fat (g)': [3, 1, 0.5, 10, 0.3, 9, 13, 5, 0.1, 4],
    'Fiber (g)': [0, 3.5, 2.4, 1.2, 4.4, 0, 0, 0, 4, 1.8],
    'Calories': [165, 215, 35, 180, 95, 90, 200, 120, 100, 150],
    'Vitamins': ['B6, B12', 'B, E', 'C, K', 'A, C', 'C', 'B12, D', 'D, B12', 'B, D', 'A, C', 'B, C']
}

northeastern_menu = {
    'Food Item': [
        'Turkey Sandwich', 'Quinoa Salad', 'Sautéed Spinach', 'Greek Salad',
        'Banana', 'Avocado Toast', 'Grilled Fish', 'Chia Pudding', 'Baked Potato', 'Falafel Wrap'
    ],
    'Protein (g)': [15, 8, 3, 6, 1, 4, 22, 5, 4, 7],
    'Carbs (g)': [30, 35, 4, 10, 27, 22, 0, 12, 37, 15],
    'Fat (g)': [6, 10, 0.5, 12, 0.3, 15, 14, 7, 0.1, 8],
    'Fiber (g)': [3, 5, 2, 1, 3, 4, 0, 8, 4, 5],
    'Calories': [300, 250, 25, 160, 105, 240, 180, 140, 120, 250],
    'Vitamins': ['B6, B12', 'C, K', 'A', 'A, C', 'C', 'B, E', 'D', 'B, E', 'A, C', 'B6, C']
}

menu_df = pd.DataFrame(bentley_menu if college == "Bentley University" else northeastern_menu)
st.write(f"### {college} Menu")
st.write(menu_df)

# Step 2: User information input
st.write("### Enter Your Information")
name = st.text_input("Name")
age = st.number_input("Age", min_value=1, max_value=100, value=18)
weight = st.number_input("Weight (lbs)", min_value=50, max_value=400, value=150)
fitness_level = st.selectbox("Fitness Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
diet_pref = st.selectbox("Dietary Preference", ["No restrictions", "Vegan", "Vegetarian", "Pescetarian"])
goal = st.selectbox("Goal", [
    "Gain Weight", "Lose Weight", "Gain Muscle", "Lose Muscle", "Tone", "More Vitamins", "Healthier Gut"
])

# Step 3: Sample menu and user customization
st.write("### Sample Menu")
meal_plan = {
    "Breakfast": st.multiselect("Select items for Breakfast", options=menu_df['Food Item'].tolist()),
    "Lunch": st.multiselect("Select items for Lunch", options=menu_df['Food Item'].tolist()),
    "Dinner": st.multiselect("Select items for Dinner", options=menu_df['Food Item'].tolist())
}

# Calculate macros and calories for selected items
def calculate_macros(selected_items, df):
    totals = {'Protein': 0, 'Carbs': 0, 'Fat': 0, 'Calories': 0}
    for item in selected_items:
        food_data = df[df['Food Item'] == item].iloc[0]
        totals['Protein'] += food_data['Protein (g)']
        totals['Carbs'] += food_data['Carbs (g)']
        totals['Fat'] += food_data['Fat (g)']
        totals['Calories'] += food_data['Calories']
    return totals

# Total macros for the day
daily_totals = {'Protein': 0, 'Carbs': 0, 'Fat': 0, 'Calories': 0}
for meal, items in meal_plan.items():
    meal_totals = calculate_macros(items, menu_df)
    daily_totals['Protein'] += meal_totals['Protein']
    daily_totals['Carbs'] += meal_totals['Carbs']
    daily_totals['Fat'] += meal_totals['Fat']
    daily_totals['Calories'] += meal_totals['Calories']

# Step 4: Display nutrient and calorie bars based on goals
st.write("### Nutritional Intake Based on Your Goal")
macros_targets = {
    "Gain Weight": {"Protein": 120, "Carbs": 300, "Fat": 80, "Calories": 2800},
    "Lose Weight": {"Protein": 100, "Carbs": 150, "Fat": 50, "Calories": 1800},
    "Gain Muscle": {"Protein": 140, "Carbs": 250, "Fat": 70, "Calories": 2500},
    "Lose Muscle": {"Protein": 80, "Carbs": 200, "Fat": 60, "Calories": 2000},
    "Tone": {"Protein": 100, "Carbs": 200, "Fat": 60, "Calories": 2200},
    "More Vitamins": {"Protein": 80, "Carbs": 180, "Fat": 55, "Calories": 2000},
    "Healthier Gut": {"Protein": 90, "Carbs": 220, "Fat": 65, "Calories": 2100}
}

target = macros_targets.get(goal, {"Protein": 100, "Carbs": 200, "Fat": 60, "Calories": 2000})

# Display bars for each macronutrient and calories
for macro in ["Protein", "Carbs", "Fat", "Calories"]:
    st.write(f"**{macro}:** {daily_totals[macro]}g / {target[macro]}g" if macro != "Calories" else f"**{macro}:** {daily_totals[macro]} / {target[macro]}")
    st.progress(daily_totals[macro] / target[macro] if target[macro] else 0)
