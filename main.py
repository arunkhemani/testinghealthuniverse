import streamlit as st
import pandas as pd
import random

# Provided menu_data with confirmed lengths of 96 items each
menu_data = {
    'Food Item': [
        'Egg & Cheese Bagel With Sausage', 'Scrambled Egg & Cheese On Bagel', 'Scrambled Eggs', 
        'Oven Roasted Greek Potatoes', 'Grilled Kielbasa', 'French Waffle', 'Everything Omelet',
        'Grits', 'Oatmeal', 'Griddled Ham Steak', 'Potato & Kale Hash', 'Chocolate Strawberry Chia Seed Pudding', 
        'Strawberry Banana Smoothie', 'Mango Banana Smoothie', 'Mango Pineapple Smoothie', 'Fresh Melons, Strawberries & Grapes', 
        'Scrambled Vegan Egg Substitute', 'Shredded Hash Browns', 'Roasted Carrots', 'Steamed Italian Vegetable Medley', 
        'Rosemary Grilled Pork Chop', 'Steamed Broccoli', 'Simply Roasted Cauliflower', 'Lentils & Swiss Chard', 
        'Extra Firm Tofu', 'Mashed Potatoes', 'Steamed Green Beans', 'Jasmine Rice', 'Garlic Rice', 'Beef Top Round Machaca', 
        'Southern Style Green Beans', 'Chicken Bacon Club Loafer Sandwich', 'French Fries', 'Grilled Garlic Chicken', 
        'Black Bean Burger', 'Hamburger On Bun', 'Cheeseburger On Bun', 'Italian Turkey And Ham Loafer Sandwich', 
        'Cumin Shrimp And Spicy Pinto Bean Bowl', 'Pepperoni Pizza', 'Cheese Pizza', 'Vegetable Lovers Feast Pizza', 
        'Green Bean Casserole', 'Garlic Breadstick', 'Hot Italian Sausage Pizza', 'Country-style Potato Salad', 
        'Latin Chipotle Quinoa Salad', 'Salsa', 'Pico De Gallo', 'Beef Tacos', 'Refried Pinto Beans', 'Sour Cream', 
        'Mexican Brown Rice With Red Pepper', 'Charred Corn With Chili & Garlic', 'Vegetarian Sausage Crumbles', 
        'Black Beans Frijoles Negros', 'Avocado Salsa Verde Cruda', 'Gluten Free Penne', 'Stuffed Peppers', 
        'Spicy Slow Roasted Peppers & Onions', 'Tomato Basil Marinara', 'Old Fashioned Chicken Noodle Soup', 
        'American Bounty Vegetable Soup', 'Two Oatmeal Raisin Cookies', 'Cinnamon Roll', 'Two Chocolate Chip Cookies', 
        'Roasted Tandoori Cauliflower', 'Tofu Vegetable Curry', 'Simple Grilled Fresh Cod', 'Simple Baked Chicken', 
        'Chive And Garlic Mashed Potatoes', 'Roasted Brussels Sprouts', 'Tuna Cheddar Melt', 'Alfredo Sauce', 
        'Cavatappi Pasta', 'Marinara Sauce', 'Vegetable Lovers Feast Pizza', 'Broccoli Cheddar Ranch Pizza', 
        'Garlic Breadstick', 'Margherita Pizza With Garlic Crust', 'Lemony Chickpea Salad', 'Mexican Brown Rice', 
        'Refried Pinto Beans', 'Beef Tacos', 'Santa Fe Black Bean', 'Simple Vegetable Polenta And Tomato Coulis', 
        'Three Bean Salad', 'Orange Angel Cupcake', 'Tapioca Pudding', 'Mediterranean Mixed Greens', 
        'Lemon Tahini Dressing', 'Plain Cooked Farro', 'Cumin Shrimp And Spicy Pinto Bean Bowl', 'Beef Top Round Machaca', 
        'Jasmine Rice', 'Simple Grilled Fresh Cod'
    ],
    'Calories': [
        500, 300, 190, 100, 190, 180, 290, 90, 110, 70, 130, 290, 100, 100, 110, 25, 100, 260, 40,
        45, 300, 10, 30, 90, 30, 70, 30, 100, 160, 140, 90, 150, 240, 200, 370, 720, 250, 250, 290, 
        80, 160, 300, 110, 130, 10, 0, 210, 110, 30, 130, 130, 30, 70, 10, 170, 300, 60, 20, 100, 45, 
        210, 160, 240, 230, 30, 160, 150, 10, 70, 45, 100, 30, 180, 160, 200, 370, 290, 100, 160, 330, 
        180, 150, 160, 300, 190, 250, 110, 45, 15, 50, 60, 50, 150, 80, 100, 150, 350
    ],
    'Protein (g)': [
        22, 18, 13, 2, 9, 4, 16, 2, 5, 9, 4, 8, 5, 4, 5, 1, 10, 3, 1, 5, 28, 22, 5, 4, 8, 20, 12, 6, 8, 15, 
        13, 16, 15, 10, 18, 25, 10, 11, 9, 3, 15, 10, 3, 8, 12, 14, 7, 5, 7, 5, 4, 12, 16, 13, 20, 17, 8, 
        5, 15, 6, 9, 12, 5, 5, 4, 3, 6, 15, 20, 18, 6, 9, 15, 4, 7, 12, 5, 7, 15, 4, 10, 15, 10, 8, 15, 20, 
        25, 18, 12, 5, 15, 10, 6, 5, 9, 7
    ],
    'Carbs (g)': [
        40, 30, 5, 20, 1, 40, 8, 18, 19, 2, 12, 35, 22, 24, 18, 10, 8, 14, 6, 12, 30, 35, 8, 5, 3, 12, 10, 
        10, 12, 10, 10, 15, 8, 12, 5, 6, 8, 8, 6, 7, 8, 12, 5, 12, 6, 8, 8, 10, 10, 12, 4, 15, 14, 10, 8, 
        12, 6, 10, 18, 15, 14, 9, 5, 6, 8, 7, 10, 6, 8, 5, 6, 5, 15, 6, 8, 6, 8, 7, 10, 5, 4, 5, 5, 6, 8, 
        12, 5, 7, 8, 10, 8, 8, 6, 4, 10, 9
    ],
    'Fat (g)': [
        30, 15, 12, 3, 15, 10, 15, 1, 2, 4, 5, 9, 5, 4, 3, 1, 6, 7, 0.5, 8, 10, 8, 2, 1, 1.5, 7, 6, 4, 7, 
        9, 12, 15, 10, 8, 5, 15, 4, 6, 7, 5, 6, 3, 5, 7, 8, 9, 4, 8, 9, 8, 4, 7, 10, 12, 8, 6, 5, 6, 10, 9, 
        6, 7, 5, 8, 12, 7, 8, 7, 6, 8, 7, 6, 7, 5, 5, 6, 6, 7, 8, 5, 9, 7, 10, 5, 6, 7, 9, 10, 5, 8, 4, 7, 
        9, 6, 10, 7
    ]
}

# Step 1: Select college and display menu
def step_1_select_college():
    st.title("How cooked is your nutrition? College Edition")
    st.write("### Pick your College:")
    st.selectbox("College", ["Bentley University"])  # Only Bentley for now
    st.write("### Bentley's Menu")
    
    # Attempt to create DataFrame by concatenating separate DataFrames
    try:
        food_df = pd.DataFrame({'Food Item': menu_data['Food Item']})
        calories_df = pd.DataFrame({'Calories': menu_data['Calories']})
        protein_df = pd.DataFrame({'Protein (g)': menu_data['Protein (g)']})
        carbs_df = pd.DataFrame({'Carbs (g)': menu_data['Carbs (g)']})
        fat_df = pd.DataFrame({'Fat (g)': menu_data['Fat (g)']})
        
        menu_df = pd.concat([food_df, calories_df, protein_df, carbs_df, fat_df], axis=1)
        
        st.write("DataFrame created successfully!")
        st.write(menu_df)
    except ValueError as e:
        st.write(f"Error creating DataFrame: {e}")

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
