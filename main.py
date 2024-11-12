import streamlit as st
import pandas as pd

# Step 1: Display "How cooked is your nutrition? College Edition" and Bentley menu
def step_1_select_college():
    st.title("How cooked is your nutrition? College Edition")
    st.write("### Pick your College:")
    college = st.selectbox("College", ["Bentley University"])  # Only Bentley for now
    
    st.write("### Bentley's Menu")
    
    menu_data = {
        'Food Item': [
            'Egg & Cheese Bagel With Sausage', 'Scrambled Egg & Cheese On Bagel', 'Scrambled Eggs', 
            'Oven Roasted Greek Potatoes', 'Grilled Kielbasa', 'French Waffle', 'Everything Omelet',
            'Grits', 'Oatmeal', 'Griddled Ham Steak', 'Potato & Kale Hash'
            # Add more items for lunch and dinner
        ],
        'Calories': [500, 300, 190, 100, 190, 180, 290, 90, 110, 70, 130],
        'Protein (g)': [22, 18, 13, 2, 9, 4, 16, 2, 5, 9, 4],  # Estimated values
        'Carbs (g)': [40, 30, 5, 20, 1, 40, 8, 18, 19, 2, 12],  # Estimated values
        'Fat (g)': [30, 15, 12, 3, 15, 10, 15, 1, 2, 4, 5]  # Estimated values
    }
    menu_df = pd.DataFrame(menu_data)
    st.write(menu_df)

    if st.button("Next"):
        st.session_state["step"] = 2
        st.session_state["menu_df"] = menu_df

# Step 2: Collect user personal details
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

# Step 3: Display and Customize Personalized Meal Plan
def step_3_personalized_meal_plan():
    st.title(f"{st.session_state['user_data']['name']}'s Personalized Meals")
    
    st.write("### Recommended Menu (Editable)")
    
    # Customizable meal plan for breakfast, lunch, and dinner
    meal_plan = {
        "Breakfast": st.multiselect("Breakfast", options=st.session_state["menu_df"]['Food Item'].tolist()),
        "Lunch": st.multiselect("Lunch", options=st.session_state["menu_df"]['Food Item'].tolist()),
        "Dinner": st.multiselect("Dinner", options=st.session_state["menu_df"]['Food Item'].tolist())
    }
    st.session_state["user_data"]["meal_plan"] = meal_plan

    # Calculate and display nutrition totals for each meal and daily totals
    st.write("### Meal Nutrition Totals")
    for meal, items in meal_plan.items():
        totals = calculate_totals(items)
        st.write(f"**{meal} Nutrition Totals:**")
        st.write(totals)

    daily_totals = calculate_totals(meal_plan["Breakfast"] + meal_plan["Lunch"] + meal_plan["Dinner"])
    st.write("### Daily Nutrition Totals")
    st.write(daily_totals)

    # Progress bars based on user goals
    target = get_target_macros(st.session_state["user_data"]["goal"])
    for nutrient in ["Calories", "Protein (g)", "Carbs (g)", "Fat (g)"]:
        if nutrient in daily_totals and nutrient in target:
            st.write(f"{nutrient}: {daily_totals[nutrient]} / {target[nutrient]}")
            st.progress(min(daily_totals[nutrient] / target[nutrient], 1.0))

    # PDF Export
    if st.button("Export to PDF"):
        export_pdf(st.session_state["user_data"], daily_totals)
    if st.button("Restart"):
        st.session_state.clear()
    if st.button("Edit Personal Information"):
        st.session_state["step"] = 2

# Helper Functions
def calculate_totals(selected_items):
    menu_df = st.session_state["menu_df"]
    # Initialize totals with all required keys, even if they will stay at 0
    totals = {"Calories": 0, "Protein (g)": 0, "Carbs (g)": 0, "Fat (g)": 0}
    for item in selected_items:
        food_data = menu_df[menu_df['Food Item'] == item].iloc[0]
        totals["Calories"] += food_data["Calories"]
        totals["Protein (g)"] += food_data["Protein (g)"]
        totals["Carbs (g)"] += food_data["Carbs (g)"]
        totals["Fat (g)"] += food_data["Fat (g)"]
    return totals

def get_target_macros(goal):
    # Define macro targets for various goals
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

def export_pdf(user_data, daily_totals):
    # Prepare HTML content for PDF
    html_content = f"""
    <h1>{user_data['name']}'s Personalized Meals</h1>
    <h2>Daily Nutrition Totals</h2>
    <p>Calories: {daily_totals['Calories']} cal</p>
    <p>Protein: {daily_totals['Protein (g)']} g</p>
    <p>Carbohydrates: {daily_totals['Carbs (g)']} g</p>
    <p>Fats: {daily_totals['Fat (g)']} g</p>
    <h3>Personal Information</h3>
    <p>Age: {user_data['age']}</p>
    <p>Weight: {user_data['weight']} lbs</p>
    <p>Fitness Level: {user_data['fitness_level']}</p>
    <p>Dietary Preference: {user_data['diet_pref']}</p>
    <p>Goal: {user_data['goal']}</p>
    """
    
    # Save HTML to PDF
    pdfkit.from_string(html_content, "Personalized_Meal_Plan.pdf")
    st.success("PDF exported as 'Personalized_Meal_Plan.pdf'!")

# Flow Control
if "step" not in st.session_state:
    st.session_state["step"] = 1

if st.session_state["step"] == 1:
    step_1_select_college()
elif st.session_state["step"] == 2:
    step_2_personal_details()
elif st.session_state["step"] == 3:
    step_
