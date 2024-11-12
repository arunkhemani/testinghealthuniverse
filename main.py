import streamlit as st
import plotly.express as px

# Step 1: Define Bentley University's Dining menu items and their macros per serving
food_items = {
    'Grilled Chicken Breast': {'protein': 30, 'carbs': 0, 'fat': 3},
    'Brown Rice': {'protein': 2, 'carbs': 45, 'fat': 1},
    'Steamed Broccoli': {'protein': 2, 'carbs': 7, 'fat': 0.5},
    'Caesar Salad': {'protein': 5, 'carbs': 12, 'fat': 10},
    'Apple': {'protein': 0, 'carbs': 25, 'fat': 0.3},
    'Scrambled Eggs': {'protein': 12, 'carbs': 1, 'fat': 9},
    'Salmon Fillet': {'protein': 25, 'carbs': 0, 'fat': 13},
    'Greek Yogurt': {'protein': 10, 'carbs': 15, 'fat': 5},
    'Roasted Sweet Potatoes': {'protein': 2, 'carbs': 27, 'fat': 0.1},
    'Tofu Stir-Fry': {'protein': 8, 'carbs': 20, 'fat': 4}
}

# Title of the app
st.title("Bentley University Dining Macro Tracker")
st.write("Select the food items you ate today and enter the number of servings.")

# Step 2: Collect servings for each item
daily_intake = {}
for food, macros in food_items.items():
    servings = st.number_input(f"Servings of {food}", min_value=0.0, max_value=10.0, step=0.1, value=0.0)
    if servings > 0:
        daily_intake[food] = servings

# Step 3: Calculate the total macros
total_macros = {'protein': 0, 'carbs': 0, 'fat': 0}
for food, servings in daily_intake.items():
    total_macros['protein'] += food_items[food]['protein'] * servings
    total_macros['carbs'] += food_items[food]['carbs'] * servings
    total_macros['fat'] += food_items[food]['fat'] * servings

# Display total macro breakdown
st.write("### Today's Macro Breakdown")
st.write(f"Protein: {total_macros['protein']}g")
st.write(f"Carbohydrates: {total_macros['carbs']}g")
st.write(f"Fat: {total_macros['fat']}g")

# Step 4: Generate a pie chart for macros using Plotly
labels = list(total_macros.keys())
values = list(total_macros.values())

fig = px.pie(
    names=labels, 
    values=values, 
    title="Macro Breakdown",
    hole=0.3
)

st.plotly_chart(fig)

# Step 5: Provide more specific recommendations for a balanced meal
protein_target = 50  # Example target; adjust based on dietary guidelines
carb_target = 200    # Example target
fat_target = 70      # Example target

recommendations = []
if total_macros['protein'] < protein_target:
    recommendations.append("Consider adding high-protein options like Grilled Chicken or Salmon to boost your protein intake.")
if total_macros['carbs'] < carb_target:
    recommendations.append("Consider adding more carbohydrates such as Brown Rice or Roasted Sweet Potatoes for sustained energy.")
if total_macros['fat'] < fat_target:
    recommendations.append("Consider healthy fats like Greek Yogurt or Caesar Salad to reach your fat target.")

if recommendations:
    st.write("### Meal Recommendations")
    st.write("\n".join(recommendations))
else:
    st.write("Great job! You've achieved a balanced macro intake for today.")
