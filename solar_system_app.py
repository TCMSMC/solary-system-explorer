import streamlit as st
import pandas as pd
from PIL import Image
from streamlit_elements import elements, dashboard, mui, html
from streamlit_custom_notification_box import custom_notification_box

# Page configuration
st.set_page_config(
    page_title="Solar System Explorer",
    page_icon="🌎",
    layout="wide"
)

# Title and introduction
st.title("🌟 Explore Our Solar System! 🚀")
st.markdown("""
Welcome young space explorers! Get ready to embark on an exciting journey through our solar system.
Let's learn about the planets, stars, and amazing space facts together!
""")

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["Planets", "Fun Facts", "Interactive Activities", "Quiz"])

# Tab 1: Planets Data
with tab1:
    st.header("Our Solar System's Planets")
    
    # Create a DataFrame with planet information
    planets_data = {
        'Planet': ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune'],
        'Type': ['Terrestrial', 'Terrestrial', 'Terrestrial', 'Terrestrial', 'Gas Giant', 'Gas Giant', 'Ice Giant', 'Ice Giant'],
        'Distance from Sun (million km)': [57.9, 108.2, 149.6, 227.9, 778.5, 1434.0, 2871.0, 4495.0],
        'Number of Moons': [0, 0, 1, 2, 79, 82, 27, 14],
        'Length of Year (Earth Days)': [88, 225, 365, 687, 4333, 10759, 30687, 60190]
    }
    planets_df = pd.DataFrame(planets_data)
    
    # Add interactivity to the table
    st.dataframe(
        planets_df,
        column_config={
            "Planet": st.column_config.TextColumn("Planet Name 🌍"),
            "Distance from Sun (million km)": st.column_config.NumberColumn(
                "Distance from Sun (million km) ☀️",
                help="Average distance from the Sun in millions of kilometers"
            )
        },
        hide_index=True,
    )
    
    # Add a planet selector with fun facts
    selected_planet = st.selectbox("Select a planet to learn more!", planets_data['Planet'])
    
    planet_facts = {
        'Mercury': "The smallest planet and closest to the Sun. It's extremely hot during the day and very cold at night!",
        'Venus': "Often called Earth's twin because of similar size, but it's the hottest planet due to greenhouse gases!",
        'Earth': "Our home planet! The only known planet with liquid water on its surface and life as we know it.",
        'Mars': "Known as the Red Planet due to iron oxide (rust) on its surface. It has the largest volcano in the solar system!",
        'Jupiter': "The largest planet in our solar system. Its Great Red Spot is a giant storm that's been raging for hundreds of years!",
        'Saturn': "Famous for its beautiful rings made of ice and rock. It's the least dense planet - it could float in water!",
        'Uranus': "The first planet discovered using a telescope. It rotates on its side like a rolling ball!",
        'Neptune': "The windiest planet with speeds up to 1,200 mph! It appears bright blue due to methane in its atmosphere."
    }
    
    st.info(f"**Fun Fact about {selected_planet}:** {planet_facts[selected_planet]}")

# Tab 2: Fun Facts
with tab2:
    st.header("🌟 Amazing Space Facts!")
    
    # Create expandable sections with fun facts
    with st.expander("Did you know? (Click to expand!)"):
        st.write("""
        - The Sun is so big that about 1.3 million Earths could fit inside it! 🌞
        - Space is completely silent because there is no air to carry sound waves 🤫
        - One day on Venus is longer than one year on Venus! ⏰
        - Jupiter's Great Red Spot is shrinking! 🔴
        - Saturn's rings are mostly made of ice and rock chunks ❄️
        """)
    
    with st.expander("More Cool Facts!"):
        st.write("""
        - Astronauts grow taller in space! 👨‍🚀
        - The footprints on the Moon will stay there for millions of years 👣
        - The Sun loses 4 million tons of mass every second ⭐
        - A year on Pluto is 248 Earth years long! ❄️
        """)

# Tab 3: Interactive Activities
with tab3:
    st.header("🎮 Interactive Learning Activities")
    
    activity = st.selectbox(
        "Choose an activity:",
        ["Order the Planets", "Planet Classification", "Match Facts"]
    )
    
    if activity == "Order the Planets":
        st.subheader("Drag and Drop the Planets in Order from the Sun")
        with elements("order_planets"):
            with dashboard.Grid(columns=8):
                for i, planet in enumerate(["Mercury", "Venus", "Earth", "Mars", 
                                          "Jupiter", "Saturn", "Uranus", "Neptune"]):
                    with mui.Card(key=f"planet_{i}", sx={"minWidth": 100, "margin": 1}):
                        mui.CardContent(planet)
        
        if st.button("Check Order"):
            st.success("Great job! You've ordered the planets correctly from the Sun!")
    
    elif activity == "Planet Classification":
        st.subheader("Classify the Planets")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Drag planets to their correct classification:")
            with elements("planet_types"):
                with dashboard.Grid(columns=2):
                    with mui.Paper(key="terrestrial", sx={"padding": 2, "background": "#f5f5f5"}):
                        mui.Typography("Terrestrial Planets")
                    with mui.Paper(key="gas_giants", sx={"padding": 2, "background": "#f5f5f5"}):
                        mui.Typography("Gas Giants")
        
        with col2:
            st.markdown("### Available Planets:")
            with elements("planets_to_classify"):
                with dashboard.Grid(columns=4):
                    for planet in planets_data['Planet']:
                        with mui.Card(key=planet, sx={"margin": 1}):
                            mui.CardContent(planet)
    
    elif activity == "Match Facts":
        st.subheader("Match the Facts to Their Planets")
        
        matching_facts = {
            "Hottest planet in our solar system": "Venus",
            "Has the Great Red Spot storm": "Jupiter",
            "Known as the Red Planet": "Mars",
            "Has beautiful rings": "Saturn",
            "Our home planet": "Earth"
        }
        
        with elements("match_facts"):
            with dashboard.Grid(columns=2):
                # Facts column
                with mui.Paper(key="facts", sx={"padding": 2, "background": "#f5f5f5"}):
                    for fact in matching_facts.keys():
                        with mui.Card(key=f"fact_{fact}", sx={"margin": 1}):
                            mui.CardContent(fact)
                
                # Planets column
                with mui.Paper(key="planets", sx={"padding": 2, "background": "#f5f5f5"}):
                    for planet in matching_facts.values():
                        with mui.Card(key=f"planet_{planet}", sx={"margin": 1}):
                            mui.CardContent(planet)

# Tab 4: Quiz
with tab4:
    st.header("🎯 Test Your Knowledge!")
    
    # Simple quiz system
    st.write("Let's see how much you've learned! Try this fun quiz:")
    
    # Question 1
    q1 = st.radio(
        "Which planet is known as the Red Planet?",
        ["Earth", "Mars", "Venus", "Jupiter"]
    )
    if q1:
        if q1 == "Mars":
            st.success("Correct! Mars is called the Red Planet because of the iron oxide (rust) on its surface.")
        else:
            st.error("Not quite! Mars is the Red Planet because of the iron oxide (rust) on its surface.")
    
    # Question 2
    q2 = st.radio(
        "Which planet has the most moons in our solar system?",
        ["Mars", "Earth", "Saturn", "Jupiter"]
    )
    if q2:
        if q2 == "Saturn":
            st.success("Correct! Saturn has 82 moons, the most in our solar system!")
        else:
            st.error("Actually, Saturn has the most moons - 82 of them!")
    
    # Question 3
    q3 = st.radio(
        "What is the hottest planet in our solar system?",
        ["Mercury", "Venus", "Mars", "Jupiter"]
    )
    if q3:
        if q3 == "Venus":
            st.success("Correct! Even though Mercury is closer to the Sun, Venus is hotter due to its thick atmosphere!")
        else:
            st.error("The answer is Venus! Its thick atmosphere traps heat, making it the hottest planet.")

# Footer
st.markdown("---")
st.markdown("Created with ❤️ for middle school space explorers!") 
