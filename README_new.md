# SQL Bomb Defusal Game

A game where players use SQL queries to defuse a virtual bomb. Test your SQL skills while racing against the clock to save the city!

## Game Overview

In this game, you play as a special agent tasked with:

1. Identifying the real bomb from several decoys using SQL queries
2. Finding the defusal code by analyzing bomb components
3. Identifying the culprit by cross-referencing access logs and suspect data

You have 10 minutes to complete all three stages before the bomb detonates!

## Play Online

You can play the game online at: [SQL Bomb Defusal Game on Streamlit Cloud](https://sqlbomb.streamlit.app/)

## Local Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/Praso28/SQLBomb.git
   cd SQLBomb
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Initialize the SQLite database (this will create the database file, schema, and sample data):
   ```
   python init_database.py
   ```

4. Run the app:
   ```
   streamlit run app.py
   ```

## Deployment Instructions

### Deploying to Streamlit Cloud

1. Fork this repository to your GitHub account.

2. Sign up for [Streamlit Cloud](https://streamlit.io/cloud) using your GitHub account.

3. Create a new app in Streamlit Cloud:
   - Connect to your GitHub repository
   - Set the main file path to `app.py`
   - Click "Deploy"

4. Your app will be deployed and accessible at a URL like `https://yourusername-sqlbomb-randomstring.streamlit.app`

### Advanced Deployment Options

For more control over your deployment, you can:

1. Modify the `.streamlit/config.toml` file to customize the appearance and behavior
2. Update the `setup.sh` script if you need to set environment variables or perform other setup tasks
3. Edit the `Procfile` if you need to change the startup command

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
- Streamlit for the frontend and user interface
- SQLite for the database (no installation required)
- Card-themed design with engaging storyline

## Features

- Immersive storyline with character profiles
- Tabbed interface for better organization of game elements
- Story-based hints that provide guidance without giving away solutions
- Advanced SQL examples that teach valuable database skills
- Card-themed visual design for a cohesive gaming experience
