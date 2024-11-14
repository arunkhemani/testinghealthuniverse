# Function to recommend foods based on deficiencies
def recommend_foods(totals, menu_df):
    # Set target levels as a percentage of the daily caloric needs
    recommended_protein = daily_caloric_needs * 0.15 / 4  # Protein: 15% of daily calories, 4 kcal/g
    recommended_fat = daily_caloric_needs * 0.25 / 9     # Fat: 25% of daily calories, 9 kcal/g
    recommended_carbs = daily_caloric_needs * 0.6 / 4    # Carbs: 60% of daily calories, 4 kcal/g
    
    # Calculate deficiencies
    deficiencies = {
        "Calories": max(0, daily_caloric_needs - totals["Calories"]),
        "Protein (g)": max(0, recommended_protein - totals["Protein (g)"]),
        "Total Fat (g)": max(0, recommended_fat - totals["Total Fat (g)"]),
        "Carbs (g)": max(0, recommended_carbs - totals["Carbs (g)"]),
    }
    
    recommendations = {}
    # Recommend foods that are high in the deficient nutrients
    if deficiencies["Calories"] > 0:
        high_calorie = menu_df[menu_df["Calories"] > 200].head(3)  # Suggest top 3 high-calorie items
        recommendations["High-Calorie Foods"] = high_calorie

    if deficiencies["Protein (g)"] > 0:
        high_protein = menu_df[menu_df["Protein (g)"] > 10].head(3)  # Suggest top 3 high-protein items
        recommendations["High-Protein Foods"] = high_protein

    if deficiencies["Total Fat (g)"] > 0:
        high_fat = menu_df[menu_df["Total Fat (g)"] > 10].head(3)  # Suggest top 3 high-fat items
        recommendations["High-Fat Foods"] = high_fat

    if deficiencies["Carbs (g)"] > 0:
        high_carbs = menu_df[menu_df["Carbs (g)"] > 20].head(3)  # Suggest top 3 high-carb items
        recommendations["High-Carb Foods"] = high_carbs

    return recommendations

# Generate recommendations based on current totals
recommendations = recommend_foods(totals, menu_df)

# Display the recommendations
st.write("### Recommended Foods to Balance Your Plan")
for nutrient, items in recommendations.items():
    st.write(f"**{nutrient}**")
    st.table(items[["Meal", "Calories", "Total Fat (g)", "Protein (g)", "Carbs (g)", "Fiber (g)"]])
