#!/bin/bash

mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

echo "\
[theme]\n\
primaryColor = \"#4dabf7\"\n\
backgroundColor = \"#212529\"\n\
secondaryBackgroundColor = \"#343a40\"\n\
textColor = \"#f8f9fa\"\n\
" >> ~/.streamlit/config.toml

# Initialize the database
python init_database.py
