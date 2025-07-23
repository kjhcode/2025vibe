import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Lunch Pie Roulette 🍽️", layout="centered")

st.title("🎡 Lunch Roulette Pie Wheel")
st.markdown("Prepare your menu and spin the animated wheel!")

# Input food items
menu_input = st.text_area(
    "🍜 Enter one food item per line (at least 2):",
    placeholder="Bibimbap\nSushi\nBurger\nPad Thai\nTacos",
    height=150
)

food_items = [line.strip() for line in menu_input.splitlines() if line.strip()]
if len(food_items) < 2:
    st.warning("Please enter at least two items to spin the wheel.")
else:
    # Generate the HTML + JS roulette
    num_items = len(food_items)
    angle_per_slice = 360 / num_items
    colors = [
        "#FFADAD", "#FFD6A5", "#FDFFB6", "#CAFFBF", "#9BF6FF",
        "#A0C4FF", "#BDB2FF", "#FFC6FF", "#FFFFFC"
    ]

    # Create slices in SVG
    slices_svg = ""
    text_svg = ""
    for i, item in enumerate(food_items):
        start_angle = i * angle_per_slice
        end_angle = start_angle + angle_per_slice
        color = colors[i % len(colors)]

        # Convert angle to radians for label position
        mid_angle = (start_angle + end_angle) / 2
        rad = (mid_angle - 90) * 3.1416 / 180
        label_x = 120 + 90 * (0.8 * st.math.cos(rad))
        label_y = 120 + 90 * (0.8 * st.math.sin(rad))

        path = f"""
            <path d="M120,120 L{120 + 120 * st.math.cos(start_angle * 3.1416 / 180)},{120 + 120 * st.math.sin(start_angle * 3.1416 / 180)} 
            A120,120 0 0,1 {120 + 120 * st.math.cos(end_angle * 3.1416 / 180)},{120 + 120 * st.math.sin(end_angle * 3.1416 / 180)} Z" 
            fill="{color}" />
        """
        text = f"""<text x="{label_x}" y="{label_y}" fill="black" font-size="12" text-anchor="middle" alignment-baseline="middle">{item}</text>"""
        slices_svg += path
        text_svg += text

    # JavaScript Wheel Spinner
    html_code = f"""
    <html>
    <head>
    <style>
        .wheel-container {{
            position: relative;
            width: 240px;
            height: 240px;
            margin: auto;
        }}
        .wheel {{
            transition: transform 5s cubic-bezier(0.33, 1, 0.68, 1);
        }}
        .pointer {{
            position: absolute;
            top: -20px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 10px solid transparent;
            border-right: 10px solid transparent;
            border-bottom: 20px solid red;
        }}
    </style>
    </head>
    <body>
        <div class="wheel-container">
            <div class="pointer"></div>
            <svg id="wheel" class="wheel" width="240" height="240" viewBox="0 0 240 240">
                {slices_svg}
                {text_svg}
            </svg>
        </div>
        <div style="text-align: center; margin-top: 20px;">
            <button onclick="spinWheel()">🎰 Spin</button>
            <h3 id="result">Waiting for spin...</h3>
        </div>

        <script>
        const foodItems = {food_items};
        let angle = 0;

        function spinWheel() {{
            const wheel = document.getElementById("wheel");
            const slices = foodItems.length;
            const anglePerSlice = 360 / slices;

            const randIndex = Math.floor(Math.random() * slices);
            const stopAngle = 360 * 5 + (360 - randIndex * anglePerSlice - anglePerSlice / 2);

            angle += stopAngle;
            wheel.style.transform = `rotate(${angle}deg)`;

            setTimeout(() => {{
                document.getElementById("result").innerText = "🍽️ You got: " + foodItems[randIndex];
            }}, 5200);
        }}
        </script>
    </body>
    </html>
    """

    components.html(html_code, height=400)
