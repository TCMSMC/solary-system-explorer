import streamlit as st
import pandas as pd
from PIL import Image
import random
import base64
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Solar System Explorer",
    page_icon="🌎",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #0a192f;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #172a45;
        padding: 10px 10px 0 10px;
        border-radius: 10px 10px 0 0;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #172a45;
        color: white;
        border-radius: 5px 5px 0 0;
        padding: 10px 20px;
        gap: 2px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2d3a4f;
    }
    .stMarkdown {
        color: #8892b0;
    }
    .stButton button {
        background-color: #64ffda;
        color: #0a192f;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #45e6c6;
    }
    .stSelectbox [data-baseweb="select"] {
        background-color: #172a45;
        color: white;
    }
    .planet-card {
        background-color: #172a45;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-message {
        background-color: #064e3b;
        color: #34d399;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-message {
        background-color: #7f1d1d;
        color: #fca5a5;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    h1, h2, h3 {
        color: #ccd6f6 !important;
    }
    .stDataFrame {
        background-color: #172a45;
        padding: 10px;
        border-radius: 10px;
    }
    .planet-container {
        display: flex;
        gap: 20px;
        margin-bottom: 30px;
        flex-wrap: wrap;
    }
    .planet-draggable {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        cursor: move;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: #172a45;
        color: #64ffda;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .planet-draggable img {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        margin-bottom: 5px;
    }
    .planet-draggable:hover {
        transform: scale(1.1);
        box-shadow: 0 0 15px rgba(100, 255, 218, 0.3);
    }
    .solar-system {
        background: linear-gradient(to right, #000000, #0a192f, #000000);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        min-height: 150px;
        display: flex;
        align-items: center;
        gap: 20px;
        overflow-x: auto;
    }
    .drop-zone {
        width: 90px;
        height: 90px;
        border: 2px dashed #64ffda;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #64ffda;
        font-size: 12px;
        transition: all 0.3s ease;
    }
    .drop-zone.dragover {
        background: rgba(100, 255, 218, 0.1);
        transform: scale(1.1);
    }
    .sun {
        width: 100px;
        height: 100px;
        background: #FFD700;
        border-radius: 50%;
        box-shadow: 0 0 30px #FFD700;
        flex-shrink: 0;
    }
</style>
""", unsafe_allow_html=True)

# Define planet data at the top level so it's available everywhere
PLANETS = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

# Planet emojis for visual enhancement
PLANET_EMOJIS = {
    'Mercury': '☿',
    'Venus': '♀',
    'Earth': '🌍',
    'Mars': '♂',
    'Jupiter': '♃',
    'Saturn': '♄',
    'Uranus': '⛢',
    'Neptune': '♆'
}

# Update PLANET_IMAGES with actual NASA images
PLANET_IMAGES = {
    'Mercury': 'https://science.nasa.gov/wp-content/uploads/2023/09/mercury.png',
    'Venus': 'https://science.nasa.gov/wp-content/uploads/2023/09/venus.png',
    'Earth': 'https://science.nasa.gov/wp-content/uploads/2023/09/earth.png',
    'Mars': 'https://science.nasa.gov/wp-content/uploads/2023/09/mars.png',
    'Jupiter': 'https://science.nasa.gov/wp-content/uploads/2023/09/jupiter.png',
    'Saturn': 'https://science.nasa.gov/wp-content/uploads/2023/09/saturn.png',
    'Uranus': 'https://science.nasa.gov/wp-content/uploads/2023/09/uranus.png',
    'Neptune': 'https://science.nasa.gov/wp-content/uploads/2023/09/neptune.png'
}

# Function to get shuffled planets
def get_shuffled_planets():
    shuffled = PLANETS.copy()
    random.shuffle(shuffled)
    return shuffled

# Initialize session state for activities if not exists
if 'shuffled_planets' not in st.session_state:
    st.session_state.shuffled_planets = get_shuffled_planets()

# Title and introduction with enhanced styling
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h1 style='color: #64ffda; font-size: 3em;'>🌟 Explore Our Solar System! 🚀</h1>
    <p style='color: #8892b0; font-size: 1.2em;'>
        Welcome young space explorers! Get ready to embark on an exciting journey through our solar system.
        Let's learn about the planets, stars, and amazing space facts together!
    </p>
</div>
""", unsafe_allow_html=True)

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["🌍 Planets", "⭐ Fun Facts", "🎮 Activities", "🎯 Quiz"])

# Tab 1: Planets Data
with tab1:
    st.markdown("<h2 style='text-align: center;'>Our Solar System's Planets</h2>", unsafe_allow_html=True)
    
    # Create a DataFrame with planet information
    planets_data = {
        'Planet': [f"{PLANET_EMOJIS[planet]} {planet}" for planet in PLANETS],
        'Type': ['Terrestrial', 'Terrestrial', 'Terrestrial', 'Terrestrial', 'Gas Giant', 'Gas Giant', 'Ice Giant', 'Ice Giant'],
        'Distance from Sun (million km)': [57.9, 108.2, 149.6, 227.9, 778.5, 1434.0, 2871.0, 4495.0],
        'Number of Moons': [0, 0, 1, 2, 79, 82, 27, 14],
        'Length of Year (Earth Days)': [88, 225, 365, 687, 4333, 10759, 30687, 60190]
    }
    planets_df = pd.DataFrame(planets_data)
    
    st.dataframe(
        planets_df,
        column_config={
            "Planet": st.column_config.TextColumn("Planet Name", help="Planet names with their astronomical symbols"),
            "Distance from Sun (million km)": st.column_config.NumberColumn(
                "Distance from Sun (million km) ☀️",
                help="Average distance from the Sun in millions of kilometers"
            ),
            "Number of Moons": st.column_config.NumberColumn("🛸 Number of Moons"),
            "Length of Year (Earth Days)": st.column_config.NumberColumn("📅 Length of Year (Earth Days)")
        },
        hide_index=True,
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    selected_planet = st.selectbox(
        "Select a planet to learn more! 🔭",
        [f"{PLANET_EMOJIS[planet]} {planet}" for planet in PLANETS]
    )
    selected_planet = selected_planet.split()[-1]  # Get just the planet name
    
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
    
    st.markdown(f"""
    <div class='planet-card'>
        <h3>{PLANET_EMOJIS[selected_planet]} {selected_planet}</h3>
        <p style='color: #8892b0; font-size: 1.1em;'>{planet_facts[selected_planet]}</p>
    </div>
    """, unsafe_allow_html=True)

# Tab 2: Fun Facts
with tab2:
    st.markdown("<h2 style='text-align: center;'>Amazing Space Facts!</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='planet-card'>
            <h3>🌟 Did you know?</h3>
            <ul style='color: #8892b0;'>
                <li>The Sun is so big that about 1.3 million Earths could fit inside it! 🌞</li>
                <li>Space is completely silent because there is no air to carry sound waves 🤫</li>
                <li>One day on Venus is longer than one year on Venus! ⏰</li>
                <li>Jupiter's Great Red Spot is shrinking! 🔴</li>
                <li>Saturn's rings are mostly made of ice and rock chunks ❄️</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='planet-card'>
            <h3>🚀 More Cool Facts!</h3>
            <ul style='color: #8892b0;'>
                <li>Astronauts grow taller in space! 👨‍🚀</li>
                <li>The footprints on the Moon will stay there for millions of years 👣</li>
                <li>The Sun loses 4 million tons of mass every second ⭐</li>
                <li>A year on Pluto is 248 Earth years long! ❄️</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Tab 3: Interactive Activities
with tab3:
    st.markdown("<h2 style='text-align: center;'>Interactive Learning Activities</h2>", unsafe_allow_html=True)
    
    activity = st.selectbox(
        "Choose your space adventure! 🚀",
        ["Order the Planets", "Planet Classification", "Match Facts"]
    )
    
    # Reset shuffled planets when activity changes
    if 'current_activity' not in st.session_state or st.session_state.current_activity != activity:
        st.session_state.shuffled_planets = get_shuffled_planets()
        st.session_state.current_activity = activity
    
    if activity == "Order the Planets":
        st.markdown("""
        <div class='planet-card'>
            <h3>🌠 Put the Planets in Order from the Sun</h3>
            <p style='color: #8892b0;'>Select the planets in order, starting from the closest to the Sun!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create columns for planet selection
        cols = st.columns(4)
        user_order = []
        
        # Initialize session state for selected planets if not exists
        if 'selected_planets' not in st.session_state:
            st.session_state.selected_planets = set()
        
        # Create selectboxes for planet positions
        for i in range(8):
            with cols[i % 4]:
                # Filter out already selected planets
                available_planets = ["Select a planet"] + [
                    planet for planet in st.session_state.shuffled_planets 
                    if planet not in st.session_state.selected_planets
                ]
                
                # Create selectbox for this position
                selected = st.selectbox(
                    f"Position {i + 1}",
                    available_planets,
                    key=f"position_{i}"
                )
                
                # Update selected planets
                if selected != "Select a planet":
                    st.session_state.selected_planets.add(selected)
                    user_order.append(selected)
                
                # Show planet image if selected
                if selected != "Select a planet":
                    st.image(
                        PLANET_IMAGES[selected],
                        caption=selected,
                        width=100
                    )
        
        # Add a reset button
        if st.button("🔄 Reset Selections", key="reset_order"):
            st.session_state.selected_planets = set()
            st.rerun()
        
        # Add a check button
        if st.button("🔍 Check Order", use_container_width=True):
            if len(user_order) < 8:
                st.warning("🚨 Please select all planets before checking!")
            elif user_order == PLANETS:
                st.markdown("""
                <div class='success-message'>
                    <h3>🎉 Fantastic! You've ordered the planets correctly!</h3>
                    <p>You're a true space explorer!</p>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
            else:
                incorrect_positions = []
                for i, (user_planet, correct_planet) in enumerate(zip(user_order, PLANETS)):
                    if user_planet != correct_planet:
                        incorrect_positions.append(i + 1)
                
                positions_str = ", ".join(str(pos) for pos in incorrect_positions)
                st.markdown(f"""
                <div class='error-message'>
                    <h4>Positions {positions_str} are not correct. Check these positions!</h4>
                    <p>Hint: Think about each planet's distance from the Sun. ☀️</p>
                </div>
                """, unsafe_allow_html=True)
                
        # Show the current order diagram
        if len(user_order) > 0:
            st.markdown("### Current Order:")
            cols = st.columns(8)
            for i, planet in enumerate(user_order):
                with cols[i]:
                    st.image(PLANET_IMAGES[planet], width=50)
                    st.caption(f"{i+1}. {planet}")

    elif activity == "Planet Classification":
        st.subheader("Classify the Planets")
        st.write("Select which planets belong in each category:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Terrestrial Planets")
            terrestrial = st.multiselect(
                "Select all terrestrial planets:",
                st.session_state.shuffled_planets,
                key="terrestrial",
                help="Rocky planets closer to the Sun"
            )
        
        with col2:
            st.markdown("### Gas Giants")
            gas_giants = st.multiselect(
                "Select all gas giants:",
                st.session_state.shuffled_planets,
                key="gas_giants",
                help="Very large planets made mostly of hydrogen and helium"
            )
            
        with col3:
            st.markdown("### Ice Giants")
            ice_giants = st.multiselect(
                "Select all ice giants:",
                st.session_state.shuffled_planets,
                key="ice_giants",
                help="Planets with icy compositions like water, ammonia, and methane"
            )
        
        if st.button("Check Classification"):
            correct_terrestrial = ["Mercury", "Venus", "Earth", "Mars"]
            correct_gas_giants = ["Jupiter", "Saturn"]
            correct_ice_giants = ["Uranus", "Neptune"]
            
            if (set(terrestrial) == set(correct_terrestrial) and 
                set(gas_giants) == set(correct_gas_giants) and 
                set(ice_giants) == set(correct_ice_giants)):
                st.success("🎉 Perfect classification! You're a planet expert!")
                st.balloons()
            else:
                st.error("Some planets are not correctly classified. Try again!")
                st.info("""Hint: 
                - Terrestrial planets are rocky and smaller (closest to the Sun)
                - Gas giants are huge planets made mostly of hydrogen and helium
                - Ice giants have more ices like water, ammonia, and methane""")
    
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
                ["Select a planet"] + st.session_state.shuffled_planets,
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
                st.success(f"🎉 Amazing! You matched all {len(facts)} correctly!")
                st.balloons()
            else:
                st.info(f"You got {correct_count} out of {len(facts)} correct. Keep trying!")

# Tab 4: Quiz
with tab4:
    st.markdown("<h2 style='text-align: center;'>Test Your Knowledge!</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='planet-card'>
        <h3>🎯 Space Quiz Challenge</h3>
        <p style='color: #8892b0;'>Let's see how much you've learned! Try this fun quiz:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Question 1
    st.markdown("""
    <div class='planet-card'>
        <h4>Question 1 🤔</h4>
    """, unsafe_allow_html=True)
    q1 = st.radio(
        "Which planet is known as the Red Planet?",
        ["Earth", "Mars", "Venus", "Jupiter"],
        index=None,
        key='quiz_q1'
    )
    if q1:
        if q1 == "Mars":
            st.markdown("""
            <div class='success-message'>
                <p>🎉 Correct! Mars is called the Red Planet because of the iron oxide (rust) on its surface.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='error-message'>
                <p>Not quite! Try again! 🔄</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Question 2
    st.markdown("""
    <div class='planet-card'>
        <h4>Question 2 🤔</h4>
    """, unsafe_allow_html=True)
    q2 = st.radio(
        "Which planet has the most moons in our solar system?",
        ["Mars", "Earth", "Saturn", "Jupiter"],
        index=None,
        key='quiz_q2'
    )
    if q2:
        if q2 == "Saturn":
            st.markdown("""
            <div class='success-message'>
                <p>🎉 Correct! Saturn has 82 moons, the most in our solar system!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='error-message'>
                <p>Not quite! Try again! 🔄</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Question 3
    st.markdown("""
    <div class='planet-card'>
        <h4>Question 3 🤔</h4>
    """, unsafe_allow_html=True)
    q3 = st.radio(
        "What is the hottest planet in our solar system?",
        ["Mercury", "Venus", "Mars", "Jupiter"],
        index=None,
        key='quiz_q3'
    )
    if q3:
        if q3 == "Venus":
            st.markdown("""
            <div class='success-message'>
                <p>🎉 Correct! Even though Mercury is closer to the Sun, Venus is hotter due to its thick atmosphere!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='error-message'>
                <p>Not quite! Try again! 🔄</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; color: #8892b0;'>
    Created with ❤️ for middle school space explorers!
    <br>
    <small>Explore the cosmos and never stop learning! 🌟</small>
</div>
""", unsafe_allow_html=True)

# Add this function after the get_shuffled_planets function
def create_solar_system_diagram(positions):
    """Create a visual representation of the solar system with planet positions"""
    html = """
    <div style="background: linear-gradient(to right, #000000, #0a192f, #000000); 
                padding: 20px; border-radius: 15px; margin: 20px 0; 
                position: relative; height: 200px; overflow: hidden;">
        <div style="position: absolute; left: 20px; top: 50%; transform: translateY(-50%);">
            <div style="width: 50px; height: 50px; background: #FFD700; 
                     border-radius: 50%; box-shadow: 0 0 20px #FFD700;">
            </div>
        </div>
    """
    
    for i, planet in enumerate(positions.values(), 1):
        if planet != "Select a planet":
            left_pos = 70 + (i * 80)  # Spacing between planets
            html += f"""
            <div style="position: absolute; left: {left_pos}px; top: 50%; 
                        transform: translateY(-50%); text-align: center;">
                <div style="font-size: 12px; color: #64ffda; margin-bottom: 5px;">
                    Position {i}
                </div>
                <img src="{PLANET_IMAGES[planet]}" 
                     style="width: 40px; height: 40px; border-radius: 50%;">
                <div style="font-size: 12px; color: #8892b0; margin-top: 5px;">
                    {planet}
                </div>
            </div>
            """
        else:
            left_pos = 70 + (i * 80)
            html += f"""
            <div style="position: absolute; left: {left_pos}px; top: 50%; 
                        transform: translateY(-50%); text-align: center;">
                <div style="font-size: 12px; color: #64ffda; margin-bottom: 5px;">
                    Position {i}
                </div>
                <div style="width: 40px; height: 40px; border: 2px dashed #64ffda; 
                           border-radius: 50%; margin: 0 auto;">
                </div>
            </div>
            """
    
    html += "</div>"
    return html 

# Add this function after your other functions
def get_planet_order():
    return st.session_state.get('planet_order', {}) 

# Add after imports
DRAG_DROP_HTML = '''
<div style="margin-bottom: 20px;">
    <div class="planet-container" id="planetSource">
        %s
    </div>
    <div class="solar-system" id="solarSystem">
        <div class="sun"></div>
        %s
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const draggables = document.querySelectorAll('.planet-draggable');
    const dropZones = document.querySelectorAll('.drop-zone');
    
    draggables.forEach(draggable => {
        draggable.addEventListener('dragstart', function(e) {
            e.dataTransfer.setData('text/plain', draggable.id);
            this.style.opacity = '0.4';
        });
        
        draggable.addEventListener('dragend', function() {
            this.style.opacity = '1';
        });
    });
    
    dropZones.forEach(zone => {
        zone.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('dragover');
        });
        
        zone.addEventListener('dragleave', function() {
            this.classList.remove('dragover');
        });
        
        zone.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
            const planetId = e.dataTransfer.getData('text/plain');
            const planetDiv = document.getElementById(planetId);
            
            if (planetDiv) {
                this.innerHTML = planetDiv.innerHTML;
                this.setAttribute('data-planet', planetId);
                
                // Update Streamlit
                const order = {};
                dropZones.forEach((zone, index) => {
                    const planetName = zone.getAttribute('data-planet');
                    if (planetName) {
                        order[index + 1] = planetName;
                    }
                });
                window.Streamlit.setComponentValue(order);
            }
        });
    });
});
</script>
''' 
