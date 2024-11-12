import streamlit as st
import matplotlib.pyplot as plt

# Step 1: Define food items and their macros per serving
food_items = {
    'Chicken Breast': {'protein': 30, 'carbs': 0, 'fat': 3},
    'Rice': {'protein': 2, 'carbs': 45, 'fat': 0},
    'Broccoli': {'protein': 2, 'carbs': 7, 'fat': 0.5},
    'Almonds': {'protein': 6, 'carbs': 6, 'fat': 14},
    'Apple': {'protein': 0, 'carbs': 25, 'fat': 0.3},
    'Egg': {'protein': 6, 'carbs': 1, 'fat': 5},
    'Salmon': {'protein': 25, 'carbs': 0, 'fat': 13},
    'Yogurt': {'protein': 10, 'carbs': 15, 'fat': 5},
    'Sweet Potato': {'protein': 2, 'carbs': 27, 'fat': 0.1},
    'Tofu': {'protein': 8, 'carbs': 2, 'fat': 4}
}

# Title of the app
st.title("Health Universe Macro Tracker")
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

# Step 4: Generate a pie chart
labels = list(total_macros.keys())
values = list(total_macros.values())

fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct='%1.1f%%')
ax.set_title("Macro Breakdown")

# Display chart
st.pyplot(fig)

# Step 5: Provide recommendations
st.write("### Recommendations for a Balanced Meal")
protein_target = 50  # Example target; adjust based on dietary guidelines
carb_target = 200    # Example target
fat_target = 70      # Example target

recommendations = []
if total_macros['protein'] < protein_target:
    recommendations.append("Consider adding more protein-rich foods like chicken or tofu.")
if total_macros['carbs'] < carb_target:
    recommendations.append("Consider adding more carbohydrates like rice or sweet potatoes.")
if total_macros['fat'] < fat_target:
    recommendations.append("Consider adding more healthy fats like almonds or salmon.")

if recommendations:
    st.write("\n".join(recommendations))
else:
    st.write("Great job! You've achieved a balanced macro intake for today.")
