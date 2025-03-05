import streamlit as st
import pandas as pd
from PIL import Image

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
        st.subheader("Put the Planets in Order from the Sun")
        st.write("Select the correct position for each planet:")
        
        # Create 8 columns for planet positions
        positions = {}
        for position in range(1, 9):
            planet = st.selectbox(
                f"Position {position} from the Sun:",
                ["Select a planet"] + planets_data['Planet'].tolist(),
                key=f"pos_{position}"
            )
            positions[position] = planet
        
        if st.button("Check Order"):
            correct_order = ["Mercury", "Venus", "Earth", "Mars", 
                           "Jupiter", "Saturn", "Uranus", "Neptune"]
            user_order = [p for p in positions.values() if p != "Select a planet"]
            
            if len(user_order) < 8:
                st.warning("Please select all planets before checking!")
            elif user_order == correct_order:
                st.success("🎉 Fantastic! You've ordered the planets correctly!")
                st.balloons()
            else:
                st.error("Not quite right. Try again! Hint: Mercury is closest to the Sun.")
    
    elif activity == "Planet Classification":
        st.subheader("Classify the Planets")
        st.write("Select which planets belong in each category:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Terrestrial Planets")
            terrestrial = st.multiselect(
                "Select all terrestrial planets:",
                planets_data['Planet'].tolist(),
                key="terrestrial"
            )
        
        with col2:
            st.markdown("### Gas Giants")
            gas_giants = st.multiselect(
                "Select all gas giants:",
                planets_data['Planet'].tolist(),
                key="gas_giants"
            )
        
        if st.button("Check Classification"):
            correct_terrestrial = ["Mercury", "Venus", "Earth", "Mars"]
            correct_gas_giants = ["Jupiter", "Saturn"]
            
            if set(terrestrial) == set(correct_terrestrial) and set(gas_giants) == set(correct_gas_giants):
                st.success("🎉 Perfect classification! You're a planet expert!")
                st.balloons()
            else:
                st.error("Some planets are not correctly classified. Try again!")
                st.info("Hint: Terrestrial planets are rocky and smaller, while gas giants are huge and made mostly of gas.")
    
    elif activity == "Match Facts":
        st.subheader("Match the Facts to Their Planets")
        
        facts = {
            "Hottest planet in our solar system": "Venus",
            "Has the Great Red Spot storm": "Jupiter",
            "Known as the Red Planet": "Mars",
            "Has beautiful rings": "Saturn",
            "Our home planet": "Earth"
        }
        
        user_answers = {}
        correct_count = 0
        
        for fact in facts.keys():
            answer = st.selectbox(
                f"Which planet: '{fact}'?",
                ["Select a planet"] + planets_data['Planet'].tolist(),
                key=f"fact_{fact}"
            )
            user_answers[fact] = answer
        
        if st.button("Check Matches"):
            all_correct = True
            for fact, correct_planet in facts.items():
                if user_answers[fact] == "Select a planet":
                    st.warning(f"Please select a planet for: '{fact}'")
                    all_correct = False
                    break
                elif user_answers[fact] == correct_planet:
                    correct_count += 1
                    st.success(f"Correct! '{fact}' matches with {correct_planet}!")
                else:
                    all_correct = False
                    st.error(f"'{fact}' is not correct. Try again!")
            
            if all_correct:
                st.success(f"🎉 Amazing! You matched all {len(facts)} facts correctly!")
                st.balloons()
            else:
                st.info(f"You got {correct_count} out of {len(facts)} correct. Keep trying!")

# Tab 4: Quiz
with tab4:
    st.header("🎯 Test Your Knowledge!")
    
    st.write("Let's see how much you've learned! Try this fun quiz:")
    
    q1 = st.radio(
        "Which planet is known as the Red Planet?",
        ["Earth", "Mars", "Venus", "Jupiter"]
    )
    if q1:
        if q1 == "Mars":
            st.success("Correct! Mars is called the Red Planet because of the iron oxide (rust) on its surface.")
        else:
            st.error("Not quite! Mars is the Red Planet because of the iron oxide (rust) on its surface.")
    
    q2 = st.radio(
        "Which planet has the most moons in our solar system?",
        ["Mars", "Earth", "Saturn", "Jupiter"]
    )
    if q2:
        if q2 == "Saturn":
            st.success("Correct! Saturn has 82 moons, the most in our solar system!")
        else:
            st.error("Actually, Saturn has the most moons - 82 of them!")
    
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
