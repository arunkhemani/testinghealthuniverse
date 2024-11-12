import streamlit as st
import pandas as pd

# Initialize session state for navigation and inputs if not already set
if "step" not in st.session_state:
    st.session_state["step"] = 1
if "user_data" not in st.session_state:
    st.session_state["user_data"] = {}

# Sample menu data for Bentley and Northeastern with nutritional information including calories
menus = {
    "Bentley University": pd.DataFrame({
        'Food Item': ['Grilled Chicken Breast', 'Brown Rice', 'Steamed Broccoli', 'Caesar Salad', 'Apple', 'Scrambled Eggs', 'Salmon Fillet', 'Greek Yogurt', 'Roasted Sweet Potatoes', 'Tofu Stir-Fry'],
        'Protein (g)': [30, 2, 2, 5, 0, 12, 25, 10, 2, 8],
        'Carbs (g)': [0, 45, 7, 12, 25, 1, 0, 15, 27, 20],
        'Fat (g)': [3, 1, 0.5, 10, 0.3, 9, 13, 5, 0.1, 4],
        'Fiber (g)': [0, 3.5, 2.4, 1.2, 4.4, 0, 0, 0, 4, 1.8],
        'Calories': [165, 215, 35, 180, 95, 90, 200, 120, 100, 150]
    }),
    "Northeastern University": pd.DataFrame({
        'Food Item': ['Turkey Sandwich', 'Quinoa Salad', 'Sautéed Spinach', 'Greek Salad', 'Banana', 'Avocado Toast', 'Grilled Fish', 'Chia Pudding', 'Baked Potato', 'Falafel Wrap'],
        'Protein (g)': [15, 8, 3, 6, 1, 4, 22, 5, 4, 7],
        'Carbs (g)': [30, 35, 4, 10, 27, 22, 0, 12, 37, 15],
        'Fat (g)': [6, 10, 0.5, 12, 0.3, 15, 14, 7, 0.1, 8],
        'Fiber (g)': [3, 5, 2, 1, 3, 4, 0, 8, 4, 5],
        'Calories': [300, 250, 25, 160, 105, 240, 180, 140, 120, 250]
    })
}

# Navigation function
def next_step():
    st.session_state["step"] += 1

def prev_step():
    st.session_state["step"] -= 1

# Step 1: Select College
if st.session_state["step"] == 1:
    st.title("Step 1: Select Your College")
    college = st.selectbox("Choose your college", options=["Bentley University", "Northeastern University"])
    st.session_state["user_data"]["college"] = college

    if st.button("Next"):
        next_step()

# Step 2: Enter Personal Information
elif st.session_state["step"] == 2:
    st.title("Step 2: Enter Your Information")
    st.session_state["user_data"]["name"] = st.text_input("Name")
    st.session_state["user_data"]["age"] = st.number_input("Age", min_value=1, max_value=100, value=18)
    st.session_state["user_data"]["weight"] = st.number_input("Weight (lbs)", min_value=50, max_value=400, value=150)
    st.session_state["user_data"]["fitness_level"] = st.selectbox("Fitness Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
    st.session_state["user_data"]["diet_pref"] = st.selectbox("Dietary Preference", ["No restrictions", "Vegan", "Vegetarian", "Pescetarian"])
    st.session_state["user_data"]["goal"] = st.selectbox("Goal", [
        "Gain Weight", "Lose Weight", "Gain Muscle", "Lose Muscle", "Tone", "More Vitamins", "Healthier Gut"
    ])

    if st.button("Previous"):
        prev_step()
    if st.button("Next"):
        next_step()

# Step 3: Custom Meal Plan
elif st.session_state["step"] == 3:
    st.title("Step 3: Customize Your Meal Plan")

    # Load the selected college's menu
    menu_df = menus[st.session_state["user_data"]["college"]]
    st.write(f"**{st.session_state['user_data']['college']} Menu**")
    st.write(menu_df)

    # Custom meal plan selection for each meal
    st.write("**Select items for each meal:**")
    st.session_state["user_data"]["meal_plan"] = {
        "Breakfast": st.multiselect("Breakfast", options=menu_df['Food Item'].tolist()),
        "Lunch": st.multiselect("Lunch", options=menu_df['Food Item'].tolist()),
        "Dinner": st.multiselect("Dinner", options=menu_df['Food Item'].tolist())
    }

    if st.button("Previous"):
        prev_step()
    if st.button("Next"):
        next_step()

# Step 4: Nutritional Analysis and Recommendations
elif st.session_state["step"] == 4:
    st.title("Step 4: Nutritional Analysis and Recommendations")

    # Calculate total macros and calories for the meal plan
    meal_plan = st.session_state["user_data"]["meal_plan"]
    menu_df = menus[st.session_state["user_data"]["college"]]
    daily_totals = {'Protein': 0, 'Carbs': 0, 'Fat': 0, 'Calories': 0}

    def calculate_macros(selected_items):
        totals = {'Protein': 0, 'Carbs': 0, 'Fat': 0, 'Calories': 0}
        for item in selected_items:
            food_data = menu_df[menu_df['Food Item'] == item].iloc[0]
            totals['Protein'] += food_data['Protein (g)']
            totals['Carbs'] += food_data['Carbs (g)']
            totals['Fat'] += food_data['Fat (g)']
            totals['Calories'] += food_data['Calories']
        return totals

    for meal, items in meal_plan.items():
        meal_totals = calculate_macros(items)
        daily_totals['Protein'] += meal_totals['Protein']
        daily_totals['Carbs'] += meal_totals['Carbs']
        daily_totals['Fat'] += meal_totals['Fat']
        daily_totals['Calories'] += meal_totals['Calories']

    # Display nutrient progress bars based on user goals
    st.write(f"**Daily Nutritional Totals**")
    target_macros = {"Gain Weight": {"Protein": 120, "Carbs": 300, "Fat": 80, "Calories": 2800},
                     "Lose Weight": {"Protein": 100, "Carbs": 150, "Fat": 50, "Calories": 1800},
                     "Gain Muscle": {"Protein": 140, "Carbs": 250, "Fat": 70, "Calories": 2500},
                     "Lose Muscle": {"Protein": 80, "Carbs": 200, "Fat": 60, "Calories": 2000},
                     "Tone": {"Protein": 100, "Carbs": 200, "Fat": 60, "Calories": 2200},
                     "More Vitamins": {"Protein": 80, "Carbs": 180, "Fat": 55, "Calories": 2000},
                     "Healthier Gut": {"Protein": 90, "Carbs": 220, "Fat": 65, "Calories": 2100}
                    }
    target = target_macros.get(st.session_state["user_data"]["goal"], {"Protein": 100, "Carbs": 200, "Fat": 60, "Calories": 2000})

    for macro in ["Protein", "Carbs", "Fat", "Calories"]:
        st.write(f"{macro}: {daily_totals[macro]} / {target[macro]}")
        st.progress(min(daily_totals[macro] / target[macro], 1.0))

    if st.button("Previous"):
        prev_step()
