import streamlit as st
import pandas as pd
import random

# Provided menu data with confirmed lengths of 96 items each
sample_menu_data = {
    'Food Item': ['Sample Item 1', 'Sample Item 2', 'Sample Item 3'],
    'Calories': [100, 200, 300],
    'Protein (g)': [10, 20, 30],
    'Carbs (g)': [15, 25, 35],
    'Fat (g)': [5, 10, 15]
}

# Convert menu data to a DataFrame
menu_df = pd.DataFrame(menu_data)

# Step 1: Select college and display menu
def step_1_select_college():
    st.title("How cooked is your nutrition? College Edition")
    st.write("### Pick your College:")
    st.selectbox("College", ["Bentley University"])  # Only Bentley for now
    st.write("### Bentley's Menu")
    st.write(menu_df)
    if st.button("Next"):
        st.session_state["step"] = 2

# Step 2: Enter personal details
def step_2_personal_details():
    st.title("Enter Your Personal Information")
    st.session_state["user_data"] = {
        "name": st.text_input("Name"),
        "age": st.number_input("Age", min_value=1, max_value=100, value=18),
        "weight": st.number_input("Weight (lbs)", min_value=50, max_value=400, value=150),
        "fitness_level": st.selectbox("Fitness Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"]),
        "diet_pref": st.selectbox("Dietary Preference", ["No restrictions", "Vegan", "Vegetarian", "Pescetarian"]),
        "goal": st.selectbox("Goal", ["Gain Weight", "Lose Weight", "Gain Muscle", "Lose Muscle", "Tone", "More Vitamins", "Healthier Gut"])
    }
    if st.button("Generate"):
        st.session_state["step"] = 3

# Step 3: Generate personalized meal plan
def step_3_generate_meal_plan():
    st.title(f"{st.session_state['user_data']['name']}'s Personalized Meal Plan")
    target = get_target_macros(st.session_state["user_data"]["goal"])
    st.write("### Target Macronutrients")
    st.write(target)

    meal_plan = {
        "Breakfast": select_meals(menu_df, target),
        "Lunch": select_meals(menu_df, target),
        "Dinner": select_meals(menu_df, target)
    }

    st.write("### Generated Meal Plan")
    for meal, items in meal_plan.items():
        st.write(f"**{meal}**")
        st.write(items)

    daily_totals = calculate_totals(pd.concat(meal_plan.values()))
    st.write("### Daily Nutrition Totals")
    st.write(daily_totals)

    for nutrient in ["Calories", "Protein (g)", "Carbs (g)", "Fat (g)"]:
        st.write(f"{nutrient}: {daily_totals[nutrient]} / {target[nutrient]}")
        st.progress(min(daily_totals[nutrient] / target[nutrient], 1.0))

    if st.button("Restart"):
        st.session_state.clear()
    if st.button("Edit Personal Information"):
        st.session_state["step"] = 2

# Helper functions
def select_meals(menu_df, target):
    selected_items = pd.DataFrame(columns=menu_df.columns)
    nutrients = {k: 0 for k in target}
    while any(nutrients[n] < target[n] for n in target):
        item = menu_df.sample(1)
        selected_items = pd.concat([selected_items, item])
        for n in target:
            nutrients[n] += item[n].values[0]
    return selected_items

def calculate_totals(selected_items):
    return selected_items[["Calories", "Protein (g)", "Carbs (g)", "Fat (g)"]].sum().to_dict()

def get_target_macros(goal):
    targets = {
        "Gain Weight": {"Calories": 2800, "Protein (g)": 120, "Carbs (g)": 300, "Fat (g)": 80},
        "Lose Weight": {"Calories": 1800, "Protein (g)": 100, "Carbs (g)": 150, "Fat (g)": 50},
        "Gain Muscle": {"Calories": 2500, "Protein (g)": 140, "Carbs (g)": 250, "Fat (g)": 70},
        "Lose Muscle": {"Calories": 2000, "Protein (g)": 80, "Carbs (g)": 200, "Fat (g)": 60},
        "Tone": {"Calories": 2200, "Protein (g)": 100, "Carbs (g)": 200, "Fat (g)": 60},
        "More Vitamins": {"Calories": 2000, "Protein (g)": 80, "Carbs (g)": 180, "Fat (g)": 55},
        "Healthier Gut": {"Calories": 2100, "Protein (g)": 90, "Carbs (g)": 220, "Fat (g)": 65}
    }
    return targets.get(goal, {"Calories": 2000, "Protein (g)": 100, "Carbs (g)": 200, "Fat (g)": 60})

# Flow control
if "step" not in st.session_state:
    st.session_state["step"] = 1

if st.session_state["step"] == 1:
    step_1_select_college()
elif st.session_state["step"] == 2:
    step_2_personal_details()
elif st.session_state["step"] == 3:
    step_3_generate_meal_plan()
