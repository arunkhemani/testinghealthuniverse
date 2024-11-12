import streamlit as st
import pandas as pd
import plotly.express as px

# Step 1: Define a sample menu with items and key nutritional values
menu_data = {
    'Food Item': [
        'Grilled Chicken Breast', 'Brown Rice', 'Steamed Broccoli', 'Caesar Salad',
        'Apple', 'Scrambled Eggs', 'Salmon Fillet', 'Greek Yogurt', 'Roasted Sweet Potatoes', 'Tofu Stir-Fry'
    ],
    'Protein (g)': [30, 2, 2, 5, 0, 12, 25, 10, 2, 8],
    'Carbs (g)': [0, 45, 7, 12, 25, 1, 0, 15, 27, 20],
    'Fat (g)': [3, 1, 0.5, 10, 0.3, 9, 13, 5, 0.1, 4],
    'Fiber (g)': [0, 3.5, 2.4, 1.2, 4.4, 0, 0, 0, 4, 1.8],
    'Vitamins': ['B6, B12', 'B, E', 'C, K', 'A, C', 'C', 'B12, D', 'D, B12', 'B, D', 'A, C', 'B, C']
}

menu_df = pd.DataFrame(menu_data)

# Title of the app
st.title("Bentley University Dining Menu Picker")

# Step 2: User selects nutritional goals
st.write("### Select Your Nutritional Goals")
nutritional_goals = st.multiselect(
    "Choose up to 3 nutritional factors to optimize for:",
    options=['Protein', 'Carbs', 'Fat', 'Fiber', 'Vitamins']
)

# Step 3: Filter menu items based on selected nutritional goals
st.write("### Recommended Food Items")

# Function to suggest foods based on goals
def recommend_foods(df, goals):
    recommendations = pd.DataFrame()
    for goal in goals:
        if goal in df.columns:
            recommendations = pd.concat([recommendations, df.nlargest(3, f"{goal} (g)")], axis=0)
        elif goal == "Vitamins":
            # Example filter for vitamin-rich foods
            recommendations = pd.concat([recommendations, df[df['Vitamins'].str.contains('C')]], axis=0)
    return recommendations.drop_duplicates().reset_index(drop=True)

# Show recommendations
recommendations_df = recommend_foods(menu_df, nutritional_goals)
if not recommendations_df.empty:
    st.write(recommendations_df[['Food Item'] + [f"{goal} (g)" for goal in nutritional_goals if goal != "Vitamins"] + ['Vitamins']])
else:
    st.write("Select at least one nutritional factor to get recommendations.")

# Step 4: Display Pie Chart for Chosen Nutritional Goals
if not recommendations_df.empty:
    st.write("### Nutritional Breakdown of Recommended Foods")
    nutrients_total = recommendations_df[[f"{goal} (g)" for goal in nutritional_goals if goal != "Vitamins"]].sum()
    fig = px.pie(
        values=nutrients_total,
        names=nutrients_total.index,
        title="Nutritional Breakdown",
        hole=0.3
    )
    st.plotly_chart(fig)
