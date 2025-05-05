import streamlit as st
import time
from backend.db import connect_db, execute_query
from backend.game_logic import validate_query, update_game_state
from backend.utils import calculate_time_taken, format_time

# Game storyline with rich narrative
STORYLINE = {
    1: {
        "title": "Stage 1: Identify the Real Bomb",
        "description": "There are multiple bombs planted across the city. Use SQL queries to analyze the data and identify the real explosive device.",
        "story": """Agent, this is Commander Hayes from Central Command. We've detected multiple explosive devices across the city, but our intel suggests only one is real - the others are decoys designed to waste our time.

The Ace of Spades terrorist cell is known for their signature bomb design. Their devices always have cutting-edge components with high signal strength and battery levels. They also use a consistent frequency pattern to ensure detonation, and each bomb has a unique device signature code.

Most importantly, their bombs are always maintained right before deployment - usually within 24 hours. The timestamp in our database will help you identify when each bomb was last serviced.

Time is critical. Find the real bomb before it's too late.""",
        "hint": "INTELLIGENCE REPORT #A-7: Our bomb squad technicians report that the Ace of Spades' real bombs always have signal strength above 95, battery levels above 90, and a perfectly consistent frequency pattern (all values identical). Their device signatures typically start with 'B9Z'. Check maintenance logs for recent activity - likely within the last day or two."
    },
    2: {
        "title": "Stage 2: Defuse the Bomb",
        "description": "You've found the bomb! Now analyze its components to discover the defusal passcode.",
        "story": """Excellent work locating the real bomb, Agent! Our EOD (Explosive Ordnance Disposal) team is on site, but they need your help to safely defuse the device.

The bomb has multiple components, but our specialists believe the deactivation mechanism is connected to either the detonator or the main circuit board. Each component has an activation code, but only one will safely disarm the bomb.

The Ace of Spades always uses premium materials for their critical components - typically titanium or gold for the parts that control deactivation. The other components are made of cheaper materials to save costs.

Find the defusal code hidden in the activation_code field of the critical component before the timer reaches zero!""",
        "hint": "FIELD REPORT #C-12: I've analyzed the bomb's construction. Look for components made of either titanium or gold - those are the high-value parts. The defusal code will be in the activation_code field of either the Detonator or Circuit component. Be precise - entering the wrong code could trigger immediate detonation."
    },
    3: {
        "title": "Stage 3: Find the Culprit",
        "description": "The bomb has technical fingerprints. Trace them back to the suspect using maintenance records.",
        "story": """The bomb is defused! Great work, Agent. Now we need to catch whoever planted it before they escape the city.

Each bomb in the Ace of Spades' arsenal requires specialized knowledge to install. Our database contains access logs that record who interacted with each bomb and what actions they performed.

We believe the person who performed the 'Installation' action on our target bomb is the culprit. Cross-reference the access logs with our suspect database to identify who we're looking for.

This is our chance to finally bring a key member of the Ace of Spades to justice. Find the name of the person responsible for planting the bomb at the Airport.""",
        "hint": "CONFIDENTIAL MEMO #F-23: The access_logs table contains records of all interactions with the bombs. The action_performed field will show 'Installation' for the person who planted the device. You'll need to join the suspects table with access_logs and filter for the bomb_id you identified in Stage 1. The suspect's name is what we need to make an arrest."
    }
}

# Advanced sample queries that teach SQL concepts without revealing solutions
SAMPLE_QUERIES = {
    1: "-- Finding patterns in data\nSELECT location, signal_strength, battery_level, frequency_pattern\nFROM bombs\nWHERE signal_strength > 80 AND battery_level > 60\nORDER BY signal_strength DESC;",
    2: "-- Analyzing relationships between entities\nSELECT bc.component_name, bc.material, bc.activation_code\nFROM bomb_components bc\nJOIN bombs b ON bc.bomb_id = b.bomb_id\nWHERE b.location = 'Train Station'\nAND bc.material IN ('Steel', 'Copper');",
    3: "-- Complex multi-table join with filtering\nSELECT s.name, s.access_level, a.action_performed, b.location\nFROM suspects s\nJOIN access_logs a ON s.suspect_id = a.suspect_id\nJOIN bombs b ON a.bomb_id = b.bomb_id\nWHERE s.access_level >= 3\nAND a.access_time > '2025-03-01'\nORDER BY a.access_time DESC;"
}

# Character profiles to enhance the storyline
CHARACTERS = {
    "commander": {
        "name": "Commander Hayes",
        "role": "Your mission director at Central Command",
        "description": "A veteran intelligence officer with 25 years of experience. Known for his calm demeanor in crisis situations."
    },
    "tech": {
        "name": "Dr. Eliza Chen",
        "role": "Technical Specialist",
        "description": "The agency's leading expert on explosive devices and database forensics. She provides technical guidance throughout your mission."
    },
    "field": {
        "name": "Agent Rodriguez",
        "role": "Field Operative",
        "description": "Your eyes on the ground. Rodriguez is at the bomb sites, relaying information back to you as you work to solve the case."
    },
    "villain": {
        "name": "The Ace of Spades",
        "role": "Terrorist Organization",
        "description": "A sophisticated cyber-terrorist group known for combining explosive devices with digital triggers. They've evaded capture for years."
    }
}

def main_app():
    # Set page configuration for better layout
    st.set_page_config(
        page_title="SQL Bomb Defusal Challenge",
        page_icon="💣",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Add custom CSS for a simple, high-contrast dark theme
    st.markdown("""
    <style>
        /* Main container styling */
        .main .block-container {
            padding: 2rem;
            max-width: 1200px;
        }

        /* Base colors - dark theme with high contrast */
        :root {
            --primary: #4dabf7;
            --secondary: #69db7c;
            --danger: #ff6b6b;
            --warning: #ffd43b;
            --dark: #212529;
            --light: #f8f9fa;
            --card-bg: #343a40;
            --text: #f8f9fa;
            --bg-color: #212529;
        }

        /* Set background color for the entire app */
        .stApp {
            background-color: var(--bg-color);
            color: var(--text);
        }

        /* Typography */
        body {
            color: var(--text);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        h1, h2, h3 {
            color: var(--primary);
            font-weight: 600;
        }

        p {
            color: var(--text);
        }

        /* Card styling with high contrast */
        .card {
            background-color: var(--card-bg);
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid var(--primary);
            color: var(--text);
        }

        .card-danger {
            border-left-color: var(--danger);
        }

        .card-success {
            border-left-color: var(--secondary);
        }

        .card-warning {
            border-left-color: var(--warning);
        }

        /* Button styling */
        .stButton button {
            background-color: var(--primary);
            color: var(--dark);
            font-weight: bold;
            border: none;
            padding: 0.7rem 1.5rem;
            border-radius: 5px;
            transition: all 0.3s ease;
        }

        .stButton button:hover {
            background-color: #228be6;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            transform: translateY(-2px);
        }

        /* Timer styling */
        .timer-normal {
            color: var(--primary);
            font-weight: bold;
            font-size: 1.5rem;
        }

        .timer-warning {
            color: var(--warning);
            font-weight: bold;
            font-size: 1.5rem;
        }

        .timer-danger {
            color: var(--danger);
            font-weight: bold;
            font-size: 1.5rem;
            animation: blinker 1s linear infinite;
        }

        @keyframes blinker {
            50% { opacity: 0.7; }
        }

        /* Code and SQL styling */
        .sql-editor {
            border: 1px solid #495057;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            background-color: #212529;
            color: #f8f9fa;
        }

        /* Schema table styling with high contrast */
        .schema-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 10px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            border: 1px solid #495057;
        }

        .schema-table th {
            background-color: #495057;
            color: white;
            text-align: left;
            padding: 10px;
            font-weight: bold;
        }

        .schema-table td {
            border: 1px solid #495057;
            padding: 10px;
            background-color: #343a40;
            color: #f8f9fa;
        }

        .schema-table tr:nth-child(even) td {
            background-color: #2b3035;
        }

        /* Certificate styling */
        .certificate {
            background: #343a40;
            border: 2px solid var(--primary);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            position: relative;
            overflow: hidden;
            color: var(--text);
        }

        .certificate h3 {
            color: var(--primary);
            margin-bottom: 10px;
        }

        .certificate h2 {
            color: var(--text);
            font-size: 24px;
            margin: 15px 0;
        }

        /* Fix Streamlit elements */
        .css-1kyxreq {
            color: var(--text) !important;
        }

        .stTextInput > div > div > input {
            color: var(--text);
            background-color: #343a40;
        }

        .stTextArea > div > div > textarea {
            color: var(--text);
            background-color: #343a40;
        }

        .stDataFrame {
            color: var(--text);
        }

        .stMarkdown {
            color: var(--text);
        }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state first
    if 'game_state' not in st.session_state:
        st.session_state.game_state = {
            'start_time': None,
            'current_stage': 1,
            'bomb_id': None,
            'clues_found': [],
            'game_completed': False,
            'last_query_results': None,
            'last_query': None,
            'last_query_error': None,
            'last_refresh': time.time()
        }

    # Simple, clean header - only show on landing page
    if st.session_state.game_state['start_time'] is None and not st.session_state.game_state['game_completed']:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="font-size: 2.5rem; margin-bottom: 0;">💣 SQL Bomb Defusal Challenge</h1>
            <p style="font-size: 1.2rem; opacity: 0.8;">Use your SQL skills to save the city!</p>
        </div>
        """, unsafe_allow_html=True)

    # Initialize additional session state variables
    if 'verification_needed' not in st.session_state:
        st.session_state.verification_needed = False

    if 'verification_stage' not in st.session_state:
        st.session_state.verification_stage = 0

    if 'verification_answer' not in st.session_state:
        st.session_state.verification_answer = ""

    # Timer implementation using Streamlit's native auto-refresh
    # We'll use a simpler approach that's more reliable
    if st.session_state.game_state['start_time'] is not None and not st.session_state.game_state['game_completed']:
        # Store the current time in the session state for comparison
        current_time = time.time()
        last_refresh = st.session_state.game_state.get('last_refresh', 0)

        # Calculate elapsed time directly
        elapsed_time = int(current_time - st.session_state.game_state['start_time'])
        st.session_state.elapsed_time = elapsed_time

        # Only trigger rerun if enough time has passed (every second)
        if current_time - last_refresh >= 1:
            st.session_state.game_state['last_refresh'] = current_time
            # Use Streamlit's rerun mechanism
            time.sleep(0.1)  # Small delay to prevent excessive CPU usage
            st.rerun()

    # Game Overview with simple dark theme
    if st.session_state.game_state['start_time'] is None:
        # Create a dramatic storyline intro with card-themed design
        st.markdown("""
        <div style="background-color: #343a40; padding: 25px; border-radius: 5px; border-left: 4px solid #ff6b6b; margin: 20px 0; text-align: center;">
            <h2 style="color: #ff6b6b; margin-top: 0;">EMERGENCY ALERT</h2>
            <p style="color: #f8f9fa; font-size: 18px; margin: 15px 0;">The Ace of Spades terrorist organization has planted bombs across the city.</p>
            <p style="color: #f8f9fa; font-size: 18px; margin: 15px 0;">You are our last hope. Use your SQL skills to save thousands of lives.</p>
        </div>
        """, unsafe_allow_html=True)

        # Create a prominent start button at the top
        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            if st.button("🚀 START MISSION", key="start_mission", use_container_width=True):
                st.session_state.game_state['start_time'] = time.time()
                st.rerun()

        # Mission briefing with storyline elements
        st.markdown("""
        <div style="background-color: #343a40; padding: 20px; border-radius: 5px; border-left: 4px solid #4dabf7; margin: 20px 0;">
            <h3 style="color: #4dabf7; margin-top: 0;">📋 Mission Briefing</h3>
            <p style="color: #f8f9fa; margin-bottom: 15px;">
                <span style="font-weight: bold; color: #ffd43b;">CLASSIFIED COMMUNICATION - PRIORITY ALPHA</span><br>
                From: Commander Hayes, Counter-Terrorism Unit<br>
                To: Special Agent Database Analyst<br>
                Subject: Operation Card Shark
            </p>
            <p style="color: #f8f9fa;">
                Agent, we've intercepted intelligence that the notorious "Ace of Spades" terrorist cell has planted multiple explosive devices across the city. Our field teams have located several suspicious devices, but we believe only one is real - the others are decoys.
            </p>
            <p style="color: #f8f9fa;">
                You've been selected for this mission because of your exceptional SQL skills. You'll need to analyze our database to identify the real bomb, find its defusal code, and track down the culprit.
            </p>
            <p style="color: #f8f9fa;">
                The clock is ticking. You have 10 minutes before detonation.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Create a card-themed 3-column layout for the mission stages
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div style="background-color: #343a40; padding: 15px; border-radius: 5px; border-left: 4px solid #ff6b6b; height: 100%;">
                <div style="text-align: center; margin-bottom: 10px;">
                    <span style="font-size: 24px; color: #ff6b6b;">♠</span>
                    <h3 style="color: #ff6b6b; margin-top: 5px;">Stage 1</h3>
                </div>
                <h4 style="color: #f8f9fa; text-align: center;">Identify the Real Bomb</h4>
                <p style="color: #f8f9fa;">Use database analysis to distinguish the real explosive from the decoys planted across the city.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="background-color: #343a40; padding: 15px; border-radius: 5px; border-left: 4px solid #ffd43b; height: 100%;">
                <div style="text-align: center; margin-bottom: 10px;">
                    <span style="font-size: 24px; color: #ffd43b;">♥</span>
                    <h3 style="color: #ffd43b; margin-top: 5px;">Stage 2</h3>
                </div>
                <h4 style="color: #f8f9fa; text-align: center;">Defuse the Bomb</h4>
                <p style="color: #f8f9fa;">Analyze the bomb's components to discover the critical defusal code hidden in the database.</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div style="background-color: #343a40; padding: 15px; border-radius: 5px; border-left: 4px solid #69db7c; height: 100%;">
                <div style="text-align: center; margin-bottom: 10px;">
                    <span style="font-size: 24px; color: #69db7c;">♣</span>
                    <h3 style="color: #69db7c; margin-top: 5px;">Stage 3</h3>
                </div>
                <h4 style="color: #f8f9fa; text-align: center;">Catch the Culprit</h4>
                <p style="color: #f8f9fa;">Cross-reference access logs and suspect data to identify and apprehend the terrorist responsible.</p>
            </div>
            """, unsafe_allow_html=True)

        # Game details with card-themed design
        st.markdown("<br>", unsafe_allow_html=True)

        # Time limit and tools in a 2-column layout with card theme
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div style="background-color: #343a40; padding: 15px; border-radius: 5px; border-left: 4px solid #ff6b6b;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 28px; margin-right: 15px;">⏱️</span>
                    <div>
                        <h3 style="color: #ff6b6b; margin-top: 0;">Time Limit</h3>
                        <p style="color: #f8f9fa;">10 minutes before detonation</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="background-color: #343a40; padding: 15px; border-radius: 5px; border-left: 4px solid #4dabf7;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 28px; margin-right: 15px;">💻</span>
                    <div>
                        <h3 style="color: #4dabf7; margin-top: 0;">Your Weapon</h3>
                        <p style="color: #f8f9fa;">SQL queries against the CTU database</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Database schema in an expander to make it less prominent
        with st.expander("📊 Database Schema (Click to expand)"):
            schema_html = """
            <table class="schema-table">
                <tr>
                    <th>Table</th>
                    <th>Columns</th>
                </tr>
                <tr>
                    <td><b>bombs</b></td>
                    <td>bomb_id, location, voltage_readings, last_maintained, signal_strength, battery_level, frequency_pattern, device_signature</td>
                </tr>
                <tr>
                    <td><b>bomb_components</b></td>
                    <td>component_id, bomb_id, component_name, material, activation_code</td>
                </tr>
                <tr>
                    <td><b>suspects</b></td>
                    <td>suspect_id, name, access_level, last_login</td>
                </tr>
                <tr>
                    <td><b>access_logs</b></td>
                    <td>log_id, suspect_id, bomb_id, access_time, action_performed</td>
                </tr>
            </table>
            """
            st.markdown(schema_html, unsafe_allow_html=True)

        # Second start button at the bottom for convenience
        st.markdown("<br>", unsafe_allow_html=True)
        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            if st.button("🚀 START MISSION", key="start_mission_bottom", use_container_width=True):
                st.session_state.game_state['start_time'] = time.time()
                st.rerun()

    # Game completed screen with simple dark theme
    elif st.session_state.game_state['game_completed']:
        time_taken = calculate_time_taken(st.session_state.game_state['start_time'])
        formatted_time = format_time(time_taken)

        # Show balloons for celebration
        st.balloons()

        # Create a story-based mission completion screen with card theme
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <div style="font-size: 40px; margin-bottom: 10px;">♠ ♥ ♣ ♦</div>
            <h1 style="color: #69db7c;">🎉 Mission Accomplished!</h1>
            <p style="font-size: 20px; color: #f8f9fa; margin-bottom: 30px;">The bomb has been defused and the city is safe!</p>
        </div>
        """, unsafe_allow_html=True)

        # Mission conclusion story - using separate elements instead of a single HTML block
        st.markdown("""
        <div style="background-color: #343a40; padding: 20px; border-radius: 5px; border-left: 4px solid #4dabf7; margin-bottom: 20px;">
            <h3 style="color: #4dabf7; margin-top: 0;">Mission Debriefing</h3>
        </div>
        """, unsafe_allow_html=True)

        # Create a styled container for the report
        st.markdown("""
        <div style="background-color: #212529; padding: 15px; border-radius: 5px; margin-bottom: 20px; font-family: 'Courier New', monospace;">
        """, unsafe_allow_html=True)

        # Report header
        st.markdown("<p style='font-weight: bold; color: #ffd43b; margin-bottom: 15px;'>CLASSIFIED COMMUNICATION - MISSION REPORT</p>", unsafe_allow_html=True)
        st.markdown("<p>From: Commander Hayes, Counter-Terrorism Unit</p>", unsafe_allow_html=True)
        st.markdown("<p>To: Director of Operations</p>", unsafe_allow_html=True)
        st.markdown("<p style='margin-bottom: 15px;'>Subject: Operation Card Shark - SUCCESSFUL</p>", unsafe_allow_html=True)

        # Report body
        st.markdown(f"<p style='margin-bottom: 15px;'>I'm pleased to report that our database specialist successfully completed all objectives of Operation Card Shark in {formatted_time}. The agent demonstrated exceptional SQL skills under extreme pressure.</p>", unsafe_allow_html=True)

        st.markdown("<p style='margin-bottom: 15px;'>The real bomb was identified at the Airport location, defused with the correct activation code, and the suspect - Sarah Connor, a known associate of the Ace of Spades - has been apprehended by our field team.</p>", unsafe_allow_html=True)

        st.markdown("<p style='margin-bottom: 15px;'>This operation has dealt a significant blow to the Ace of Spades organization. Forensic analysis of the defused device is already providing valuable intelligence on their methods and technology.</p>", unsafe_allow_html=True)

        st.markdown("<p>I'm recommending our agent for the CTU Medal of Excellence for their outstanding performance in this mission.</p>", unsafe_allow_html=True)

        # Close the container
        st.markdown("</div>", unsafe_allow_html=True)

        # Create a two-column layout for mission summary and stats with card theme
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div style="background-color: #343a40; padding: 20px; border-radius: 5px; border-left: 4px solid #69db7c;">
                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                    <span style="font-size: 28px; margin-right: 15px;">♣</span>
                    <h3 style="color: #69db7c; margin: 0;">Mission Objectives</h3>
                </div>
                <ul style="color: #f8f9fa; list-style-type: none; padding-left: 0;">
                    <li style="padding: 8px 0; font-size: 16px;">✅ Successfully identified the real bomb at the Airport</li>
                    <li style="padding: 8px 0; font-size: 16px;">✅ Found the correct defusal code: 221</li>
                    <li style="padding: 8px 0; font-size: 16px;">✅ Identified the culprit: Sarah Connor</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="background-color: #343a40; padding: 20px; border-radius: 5px; border-left: 4px solid #4dabf7;">
                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                    <span style="font-size: 28px; margin-right: 15px;">♦</span>
                    <h3 style="color: #4dabf7; margin: 0;">Mission Stats</h3>
                </div>
                <p style="color: #f8f9fa; font-size: 16px;"><b>⏱️ Time taken:</b> {formatted_time}</p>
                <p style="color: #f8f9fa; font-size: 16px;"><b>🏆 Status:</b> Success</p>
                <p style="color: #f8f9fa; font-size: 16px;"><b>🔍 Evidence:</b> Collected</p>
                <p style="color: #f8f9fa; font-size: 16px;"><b>👮 Suspect:</b> In custody</p>
            </div>
            """, unsafe_allow_html=True)

        # Certificate with card theme
        _, cert_col, _ = st.columns([1, 3, 1])
        with cert_col:
            st.markdown("""
            <div style="margin: 30px auto; width: 100%; background-color: #343a40; border: 2px solid #4dabf7; border-radius: 10px; padding: 20px; text-align: center;">
                <div style="font-size: 24px; margin-bottom: 10px; letter-spacing: 10px;">♠ ♥ ♣ ♦</div>
                <h3 style="color: #4dabf7; margin-top: 0;">Certificate of Achievement</h3>
                <h2 style="color: #f8f9fa; margin: 15px 0; font-size: 28px;">SQL EXPERT</h2>
                <p style="color: #f8f9fa; font-size: 16px;">has successfully completed</p>
                <h3 style="color: #ff6b6b; margin: 10px 0;">OPERATION CARD SHARK</h3>
                <p style="font-style: italic; margin-top: 20px; color: #adb5bd;">Awarded for exceptional database skills under pressure</p>
                <p style="color: #ffd43b; margin-top: 15px;">Counter-Terrorism Unit</p>
            </div>
            """, unsafe_allow_html=True)

        # Play Again button - better centered with more emphasis
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)  # Add some space

        # Use a narrower column for better centering
        _, center_col, _ = st.columns([2, 1, 2])
        with center_col:
            if st.button("🔄 PLAY AGAIN", key="play_again", use_container_width=True):
                # Reset game state
                st.session_state.game_state = {
                    'start_time': None,
                    'current_stage': 1,
                    'bomb_id': None,
                    'clues_found': [],
                    'game_completed': False,
                    'last_query_results': None,
                    'last_query': None,
                    'last_query_error': None,
                    'last_refresh': time.time()
                }

                # Reset verification state
                st.session_state.verification_needed = False
                st.session_state.verification_stage = 0
                st.session_state.verification_answer = ""

                # Reset timer state
                if 'elapsed_time' in st.session_state:
                    del st.session_state.elapsed_time

                st.rerun()

    # Gameplay
    else:
        # Calculate time remaining using the elapsed time from session state
        # This ensures more accurate and consistent timer updates
        elapsed_time = getattr(st.session_state, 'elapsed_time', 0)
        if elapsed_time == 0:  # Fallback if elapsed_time is not set yet
            elapsed_time = calculate_time_taken(st.session_state.game_state['start_time'])

        time_remaining = max(0, 600 - elapsed_time)
        mins, secs = divmod(time_remaining, 60)

        # Current stage info
        current_stage = st.session_state.game_state['current_stage']
        stage = STORYLINE[current_stage]

        # Create a header with stage number and timer
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <div style="display: flex; align-items: center;">
                <div style="background-color: #ff6b6b; color: white; width: 40px; height: 40px;
                    border-radius: 50%; display: flex; align-items: center; justify-content: center;
                    margin-right: 15px; font-weight: bold; font-size: 18px;">
                    {current_stage}
                </div>
                <h2 style="margin: 0; color: #4dabf7;">Stage {current_stage}: {stage['title'].split(': ')[1]}</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Create columns for timer layout
        timer_col1, timer_col2 = st.columns([3, 1])

        with timer_col1:
            # Progress bar for timer - more efficient implementation
            progress_percent = max(0, min(1, time_remaining / 600))  # Ensure value is between 0 and 1
            st.progress(progress_percent)

        with timer_col2:
            # Display timer with color based on time remaining - more efficient implementation
            timer_class = "timer-normal"
            if time_remaining <= 120:
                timer_class = "timer-danger"
            elif time_remaining <= 300:
                timer_class = "timer-warning"

            st.markdown(f"<div class='{timer_class}' style='text-align: center;'>⏳ {mins:02}:{secs:02}</div>", unsafe_allow_html=True)

        # Check if verification is needed
        if st.session_state.verification_needed:
            # Create a verification form
            st.markdown("""
            <div style="background-color: #343a40; padding: 20px; border-radius: 5px; border-left: 4px solid #ffd43b; margin: 20px 0;">
                <h3 style="color: #ffd43b; margin-top: 0; text-align: center;">🔍 VERIFICATION REQUIRED</h3>
                <p style="color: #f8f9fa; text-align: center;">Based on your query results, what did you discover?</p>
            </div>
            """, unsafe_allow_html=True)

            # Create verification questions based on stage
            verification_stage = st.session_state.verification_stage

            if verification_stage == 1:
                verification_question = "Which location contains the real bomb? (Enter the exact location)"
                correct_answer = "Airport"
            elif verification_stage == 2:
                verification_question = "What is the defusal code for the bomb? (Enter the exact code)"
                correct_answer = "221"
            elif verification_stage == 3:
                verification_question = "Who is the culprit behind the bomb? (Enter the exact name)"
                correct_answer = "Sarah Connor"

            # Display the verification form
            verification_answer = st.text_input(verification_question, key="verification_input")

            # Verify button
            if st.button("VERIFY", key="verify_button", use_container_width=True):
                if verification_answer.strip() == correct_answer:
                    # Correct answer
                    st.success(f"✅ Correct! Moving to the next stage...")

                    # Reset verification state
                    st.session_state.verification_needed = False
                    st.session_state.verification_stage = 0

                    # Update game state
                    if verification_stage < 3:
                        st.session_state.game_state['current_stage'] += 1
                    else:
                        # Game completed
                        st.session_state.game_state['game_completed'] = True

                    # Rerun to update the UI
                    time.sleep(1)
                    st.rerun()
                else:
                    # Incorrect answer
                    st.error("❌ Incorrect. Please review your query results and try again.")

        # Create a two-column layout with sidebar and main content
        left_col, main_col = st.columns([1, 3])

        # Left sidebar with tabbed interface for better organization
        with left_col:
            # Create tabs for different types of information
            story_tab, hints_tab, examples_tab, schema_tab = st.tabs(["📖 Story", "🔍 Hints", "📝 Examples", "📊 Schema"])

            # STORY TAB - Contains mission storyline and character information
            with story_tab:
                # Current mission storyline
                st.markdown(f"""
                <div style="background-color: #343a40; padding: 15px; border-radius: 5px; border-left: 4px solid #4dabf7; margin-bottom: 15px;">
                    <h3 style="color: #4dabf7; margin-top: 0;">Mission Briefing</h3>
                    <p style="color: #f8f9fa; white-space: pre-line;">{stage['story']}</p>
                </div>
                """, unsafe_allow_html=True)

                # Character information relevant to current stage
                if current_stage == 1:
                    character = CHARACTERS["commander"]
                    color = "#ff6b6b"  # Red for stage 1
                elif current_stage == 2:
                    character = CHARACTERS["tech"]
                    color = "#ffd43b"  # Yellow for stage 2
                else:
                    character = CHARACTERS["field"]
                    color = "#69db7c"  # Green for stage 3

                st.markdown(f"""
                <div style="background-color: #343a40; padding: 15px; border-radius: 5px; border-left: 4px solid {color};">
                    <h3 style="color: {color}; margin-top: 0;">{character['name']}</h3>
                    <p style="color: #adb5bd; font-style: italic; margin-bottom: 10px;">{character['role']}</p>
                    <p style="color: #f8f9fa;">{character['description']}</p>
                </div>
                """, unsafe_allow_html=True)

                # Villain information (always shown)
                st.markdown("""
                <div style="background-color: #343a40; padding: 15px; border-radius: 5px; border-left: 4px solid #ff6b6b; margin-top: 15px;">
                    <h3 style="color: #ff6b6b; margin-top: 0;">Target Profile</h3>
                """, unsafe_allow_html=True)

                villain = CHARACTERS["villain"]
                st.markdown(f"""
                    <p style="color: #adb5bd; font-style: italic; margin-bottom: 10px;">{villain['name']} - {villain['role']}</p>
                    <p style="color: #f8f9fa;">{villain['description']}</p>
                </div>
                """, unsafe_allow_html=True)

                # Clues found
                if st.session_state.game_state['clues_found']:
                    st.markdown("""
                    <div style="background-color: #343a40; padding: 15px; border-radius: 5px; border-left: 4px solid #69db7c; margin-top: 15px;">
                        <h3 style="color: #69db7c; margin-top: 0;">Intelligence Gathered</h3>
                    """, unsafe_allow_html=True)

                    for clue in st.session_state.game_state['clues_found']:
                        st.markdown(f"<p style='color: #f8f9fa;'>✅ {clue}</p>", unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)

            # HINTS TAB - Contains story-based hints and mission objectives
            with hints_tab:
                # Current objective
                st.markdown(f"""
                <div style="background-color: #343a40; padding: 15px; border-radius: 5px; border-left: 4px solid #ffd43b; margin-bottom: 15px;">
                    <h3 style="color: #ffd43b; margin-top: 0;">Current Objective</h3>
                    <p style="color: #f8f9fa; font-weight: bold;">{stage['title'].split(': ')[1]}</p>
                    <p style="color: #f8f9fa;">{stage['description']}</p>
                </div>
                """, unsafe_allow_html=True)

                # Hint styled as an intelligence report
                st.markdown(f"""
                <div style="background-color: #343a40; padding: 15px; border-radius: 5px; border-left: 4px solid #4dabf7;">
                    <h3 style="color: #4dabf7; margin-top: 0;">Intelligence Report</h3>
                    <p style="color: #f8f9fa; white-space: pre-line;">{stage['hint']}</p>
                </div>
                """, unsafe_allow_html=True)

            # EXAMPLES TAB - Contains sample queries with explanations
            with examples_tab:
                # Basic sample query for current stage
                st.markdown("""
                <div style="background-color: #343a40; padding: 15px; border-radius: 5px; border-left: 4px solid #4dabf7; margin-bottom: 15px;">
                    <h3 style="color: #4dabf7; margin-top: 0;">Sample Query</h3>
                    <p style="color: #f8f9fa;">This query demonstrates techniques that might be helpful:</p>
                </div>
                """, unsafe_allow_html=True)

                st.code(SAMPLE_QUERIES[current_stage], language="sql")

                # Basic queries reference
                st.markdown("""
                <div style="background-color: #343a40; padding: 15px; border-radius: 5px; border-left: 4px solid #69db7c; margin-top: 15px;">
                    <h3 style="color: #69db7c; margin-top: 0;">Basic SQL Reference</h3>
                </div>
                """, unsafe_allow_html=True)

                # Basic queries for all stages
                st.code("-- View all bombs\nSELECT * FROM bombs;", language="sql")
                st.code("-- View all suspects\nSELECT * FROM suspects;", language="sql")

                # Stage-specific examples
                if current_stage >= 2:
                    st.code("-- View bomb components\nSELECT * FROM bomb_components;", language="sql")

                if current_stage >= 3:
                    st.code("-- View access logs\nSELECT * FROM access_logs;", language="sql")

                # Advanced queries for higher stages
                if current_stage >= 2:
                    st.markdown("""
                    <div style="background-color: #343a40; padding: 15px; border-radius: 5px; border-left: 4px solid #ffd43b; margin-top: 15px;">
                        <h3 style="color: #ffd43b; margin-top: 0;">Advanced Techniques</h3>
                    </div>
                    """, unsafe_allow_html=True)

                    st.code("-- Filtering with multiple conditions\nSELECT * FROM bombs\nWHERE signal_strength > 90\nAND battery_level > 80\nAND location LIKE '%Station%';", language="sql")

                    if current_stage >= 2:
                        st.code("-- Joining tables with relationship filters\nSELECT b.location, bc.component_name, bc.material\nFROM bombs b\nJOIN bomb_components bc ON b.bomb_id = bc.bomb_id\nWHERE bc.material IN ('Titanium', 'Gold')\nORDER BY b.signal_strength DESC;", language="sql")

                    if current_stage >= 3:
                        st.code("-- Complex multi-table join with time filtering\nSELECT s.name, a.action_performed, b.location, a.access_time\nFROM suspects s\nJOIN access_logs a ON s.suspect_id = a.suspect_id\nJOIN bombs b ON a.bomb_id = b.bomb_id\nWHERE a.action_performed = 'Installation'\nAND a.access_time > '2025-03-01'\nORDER BY a.access_time DESC;", language="sql")

            # SCHEMA TAB - Contains database schema information
            with schema_tab:
                schema_html = """
                <table class="schema-table">
                    <tr>
                        <th>Table</th>
                        <th>Columns</th>
                    </tr>
                    <tr>
                        <td><b>bombs</b></td>
                        <td>bomb_id, location, voltage_readings, last_maintained, signal_strength, battery_level, frequency_pattern, device_signature</td>
                    </tr>
                    <tr>
                        <td><b>bomb_components</b></td>
                        <td>component_id, bomb_id, component_name, material, activation_code</td>
                    </tr>
                    <tr>
                        <td><b>suspects</b></td>
                        <td>suspect_id, name, access_level, last_login</td>
                    </tr>
                    <tr>
                        <td><b>access_logs</b></td>
                        <td>log_id, suspect_id, bomb_id, access_time, action_performed</td>
                    </tr>
                </table>
                """
                st.markdown(schema_html, unsafe_allow_html=True)

                # Table relationships diagram (text-based for simplicity)
                st.markdown("""
                <div style="background-color: #343a40; padding: 15px; border-radius: 5px; margin-top: 15px;">
                    <h3 style="color: #4dabf7; margin-top: 0;">Table Relationships</h3>
                    <pre style="color: #f8f9fa; background-color: #212529; padding: 10px; border-radius: 5px;">
bombs
  ↑
  | bomb_id
  ↓
bomb_components

suspects
  ↑
  | suspect_id
  ↓
access_logs → bombs (via bomb_id)
                    </pre>
                </div>
                """, unsafe_allow_html=True)

                # Data types explanation
                st.markdown("""
                <div style="background-color: #343a40; padding: 15px; border-radius: 5px; margin-top: 15px;">
                    <h3 style="color: #4dabf7; margin-top: 0;">Data Types</h3>
                    <ul style="color: #f8f9fa;">
                        <li><b>bomb_id, component_id, suspect_id, log_id:</b> INTEGER (Primary Keys)</li>
                        <li><b>location, name, material, action_performed:</b> TEXT</li>
                        <li><b>signal_strength, battery_level, access_level:</b> INTEGER</li>
                        <li><b>last_maintained, last_login, access_time:</b> TEXT (Date/Time format: 'YYYY-MM-DD HH:MM')</li>
                        <li><b>frequency_pattern, voltage_readings:</b> TEXT (Comma-separated values)</li>
                        <li><b>device_signature, activation_code:</b> TEXT (Alphanumeric codes)</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

        # Main column with SQL query input and execution - using full width
        with main_col:
            # SQL Terminal - make it more prominent
            st.markdown("""
            <div style="background-color: #343a40; padding: 15px; border-radius: 5px; border-left: 4px solid #4dabf7; margin-bottom: 15px;">
                <h3 style="color: #4dabf7; margin-top: 0; text-align: center;">💻 SQL TERMINAL</h3>
            </div>
            """, unsafe_allow_html=True)

            # SQL editor with syntax highlighting - make it larger
            query = st.text_area(
                "Enter your SQL query:",
                height=200,
                placeholder=SAMPLE_QUERIES[current_stage],
                key="sql_query_input",
                help="Write a SQL query to solve the current mission stage"
            )

            # Execute button - make it more prominent
            execute_btn = st.button("⚡ EXECUTE QUERY", key="execute_query_button", use_container_width=True)

            # Display previous query results if they exist
            if st.session_state.game_state.get('last_query') and st.session_state.game_state.get('last_query_results') is not None:
                st.markdown("""
                <div style="background-color: #343a40; padding: 15px; border-radius: 5px; border-left: 4px solid #4dabf7; margin-top: 20px;">
                    <h3 style="color: #4dabf7; margin-top: 0; text-align: center;">📊 QUERY RESULTS</h3>
                """, unsafe_allow_html=True)

                # Display the query that was executed
                st.markdown("""
                <div style="background-color: #2b3035; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
                    <p style="margin-bottom: 5px; color: #f8f9fa;"><b>Executed Query:</b></p>
                """, unsafe_allow_html=True)
                st.code(st.session_state.game_state['last_query'], language="sql")
                st.markdown("</div>", unsafe_allow_html=True)

                # Get the results
                results = st.session_state.game_state['last_query_results']

                # Check if we have results to display
                if results and len(results) > 0:
                    try:
                        # Display results in a styled dataframe
                        st.markdown("<p style='color: #f8f9fa;'><b>Results:</b></p>", unsafe_allow_html=True)
                        st.dataframe(data=results, use_container_width=True, height=400)
                    except Exception as e:
                        st.error(f"Error displaying results: {str(e)}")
                        st.json(results)  # Fallback to JSON display
                else:
                    st.info("Query executed successfully, but returned no results.")

                # Display error if there was one
                if st.session_state.game_state.get('last_query_error'):
                    st.markdown("""
                    <div style="background-color: #2b3035; padding: 10px; border-radius: 5px; margin-top: 15px; border-left: 4px solid #ff6b6b;">
                        <p style="color: #ff6b6b; margin: 0;"><b>Error:</b> {}</p>
                    </div>
                    """.format(st.session_state.game_state['last_query_error']), unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

        # Execute Query button logic
        if execute_btn:
            try:
                conn = connect_db()

                if validate_query(query):
                    # Store the query for display
                    st.session_state.game_state['last_query'] = query
                    st.session_state.game_state['last_query_error'] = None

                    # Execute the query
                    results = execute_query(conn, query)

                    # Store the results in session state
                    st.session_state.game_state['last_query_results'] = results

                    if results:
                        # Create a success message
                        st.markdown("""
                        <div style='background-color: #d4edda; border-radius: 5px; padding: 10px; margin-top: 10px;'>
                            <p style='color: #28a745; font-weight: bold;'>✅ Query Successful!</p>
                        </div>
                        """, unsafe_allow_html=True)

                        # Update game state based on query results
                        stage_completed = update_game_state(
                            current_stage,
                            results,
                            st.session_state.game_state
                        )

                        # Handle stage completion with verification step
                        if stage_completed:
                            # Set verification needed flag
                            st.session_state.verification_needed = True
                            st.session_state.verification_stage = current_stage

                            # Show verification form
                            st.success(f"🎯 You've found something important! Please verify your findings to proceed.")
                            st.rerun()
                    else:
                        st.info("Query executed successfully, but returned no results.")
                else:
                    st.error("Invalid query. Only SELECT statements are allowed, and certain operations are restricted for security.")
            except Exception as e:
                error_msg = str(e)
                st.error(f"Error executing query: {error_msg}")
                # Store the error in session state
                st.session_state.game_state['last_query_results'] = []
                st.session_state.game_state['last_query_error'] = error_msg
            finally:
                if 'conn' in locals():
                    conn.close()

            # Force a rerun to update the display
            st.rerun()

        # Game Over Condition - more efficient implementation
        if time_remaining <= 0:
            # Create a prominent game over message
            st.error("⏰ Time's up! The bomb has detonated.")

            # Reset the game state
            st.session_state.game_state = {
                'start_time': None,
                'current_stage': 1,
                'bomb_id': None,
                'clues_found': [],
                'game_completed': False,
                'last_query_results': None,
                'last_query': None,
                'last_query_error': None,
                'last_refresh': time.time()
            }

            # Reset verification state
            st.session_state.verification_needed = False
            st.session_state.verification_stage = 0
            st.session_state.verification_answer = ""

            # Reset timer state
            if 'elapsed_time' in st.session_state:
                del st.session_state.elapsed_time

            # Use a small delay to ensure the message is displayed before rerunning
            time.sleep(0.5)
            st.rerun()


# Run the app

if __name__ == "__main__":

    main_app()

