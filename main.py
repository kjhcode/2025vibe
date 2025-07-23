import streamlit as st
import random
import time
import pandas as pd

st.set_page_config(page_title="Lunch Roulette 🎯", page_icon="🍽")

st.title("🎯 Lunch Roulette")
st.subheader("Can't decide what to eat? Spin the wheel!")

st.markdown("👉 **Step 1:** Enter your lunch options below:")

# Input section
with st.form("menu_input_form"):
    menu_text = st.text_area(
        "Enter one menu item per line. Optionally add calories and price separated by commas.\n\n"
        "**Example:** `Bibimbap, 550, 8000`",
        height=200,
        placeholder="Bibimbap, 550, 8000\nKimchi Stew, 600, 8500\nSushi"
    )
    submitted = st.form_submit_button("✅ Submit Menu")

# Parse menu
menu_items = []
if submitted or menu_text:
    for line in menu_text.strip().splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) == 1:
            menu_items.append({"name": parts[0], "calories": None, "price": None})
        elif len(parts) == 2:
            menu_items.append({"name": parts[0], "calories": parts[1], "price": None})
        else:
            menu_items.append({"name": parts[0], "calories": parts[1], "price": parts[2]})

# Convert to DataFrame
if menu_items:
    df = pd.DataFrame(menu_items)
    st.markdown("📋 **Your Menu:**")
    st.dataframe(df)

    # Spin button
    if st.button("🎰 Spin the Roulette!"):
        with st.spinner("Spinning the wheel... 🎡"):
            for _ in range(10):
                random_item = random.choice(menu_items)
                st.markdown(f"### 👉 {random_item['name']}")
                time.sleep(0.2)
            final_choice = random.choice(menu_items)
            st.success("🎉 Your lunch today is:")
            st.markdown(f"## 🥢 **{final_choice['name']}**")
            if final_choice["calories"]:
                st.markdown(f"- 🔥 Calories: {final_choice['calories']} kcal")
            if final_choice["price"]:
                st.markdown(f"- 💸 Price: ₩{int(final_choice['price']):,}")
