# SQL Bomb Defusal Game

A game where players use SQL queries to defuse a virtual bomb. Test your SQL skills while racing against the clock to save the city!

## Game Overview

In this game, you play as a special agent tasked with:

1. Identifying the real bomb from several decoys using SQL queries
2. Finding the defusal code by analyzing bomb components
3. Identifying the culprit by cross-referencing access logs and suspect data

You have 10 minutes to complete all three stages before the bomb detonates!

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/TicTicBomb.git
   cd TicTicBomb
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Initialize the SQLite database (this will create the database file, schema, and sample data):
   ```
   python init_database.py
   ```

5. Run the app:
   ```
   streamlit run app.py
   ```

## Database Schema

The game uses the following database tables:

- **bombs**: Information about bomb locations and characteristics
- **bomb_components**: Details about components that make up each bomb
- **suspects**: Information about potential culprits
- **access_logs**: Records of who accessed which bomb and when

## Gameplay Tips

- Use SQL SELECT statements to query the database
- Pay attention to the hints provided at each stage
- Look for patterns and anomalies in the data
- Use JOIN operations to connect related information across tables

## Technologies Used

- Python
- Streamlit for the frontend
- SQLite for the database (no installation required)
- Flask for backend services
