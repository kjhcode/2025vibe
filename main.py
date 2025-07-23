import streamlit as st
import random
import pandas as pd

# Sample lunch menu
menu_data = [
    {"name": "Bibimbap", "type": "Korean", "diet": "vegetarian"},
    {"name": "Kimchi Stew", "type": "Korean", "diet": "regular"},
    {"name": "Sushi", "type": "Japanese", "diet": "regular"},
    {"name": "Tempura Udon", "type": "Japanese", "diet": "vegetarian"},
    {"name": "Burger", "type": "Western", "diet": "regular"},
    {"name": "Caesar Salad", "type": "Western", "diet": "vegetarian"},
    {"name": "Pad Thai", "type": "Thai", "diet": "vegetarian"},
    {"name": "Green Curry", "type": "Thai", "diet": "regular"},
    {"name": "Vegan Burrito", "type": "Mexican", "diet": "vegan"},
    {"name": "Beef Tacos", "type": "Mexican", "diet": "regular"},
]

menu_df = pd.DataFrame(menu_data)

# App title
st.title("🥢 What Should I Eat for Lunch?")
st.write("Feeling indecisive? Let me help you pick a lunch menu!")

# User input: Cuisine type
cuisine = st.multiselect(
    "Pick your preferred cuisine(s):",
    options=menu_df["type"].unique(),
    default=menu_df["type"].unique().tolist()
)

# User input: Dietary preference
diet = st.selectbox(
    "Select your dietary preference:",
    options=["any", "regular", "vegetarian", "vegan"]
)

# Filter menu based on user input
filtered_menu = menu_df[menu_df["type"].isin(cuisine)]
if diet != "any":
    filtered_menu = filtered_menu[filtered_menu["diet"] == diet]

# Suggestion
if st.button("🎲 Suggest Lunch"):
    if not filtered_menu.empty:
        choice = random.choice(filtered_menu["name"].tolist())
        st.success(f"How about **{choice}**?")
    else:
        st.error("No menu matches your criteria. Try adjusting your filters!")

# Show full menu (optional)
with st.expander("📋 View Full Menu"):
    st.dataframe(menu_df)
