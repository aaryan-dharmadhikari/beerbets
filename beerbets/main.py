# main.py

import panel as pn
import webbrowser
import pandas as pd
import plotly.express as px
from beerbets.bet_page import bet_page

# Initialize Panel extension with necessary dependencies and custom CSS
pn.extension('plotly', 'tabulator', css_files=['styles.css'])

# Define accent colors to maintain consistent styling
ACCENT = "#BB2649"
RED = "#D94467"
GREEN = "#5AD534"

# ================================
# Main Page Components
# ================================

# Widgets for the Main Page
bet_input = pn.widgets.TextInput(name="Your Bet", placeholder="Enter your bet here...", width=400)
submit_button = pn.widgets.Button(name="Place Bet", button_type="primary", width=200)
output_text = pn.pane.Markdown("### Your bet will appear here.", width=400)

# Navigation Button with custom CSS class (Removed 'button_color' parameter)
navigate_button = pn.widgets.Button(
    name="Go to Bet Page",
    button_type="primary",  # Use a base type
    css_classes=['custom-button'],  # Apply custom CSS class for additional styling
    width=200
)


# Define button click action for placing a bet on the Main Page
def place_bet(event):
    if bet_input.value:
        output_text.object = f"**You bet on:** {bet_input.value}"
    else:
        output_text.object = "⚠️ Please enter a bet!"


# Link button click to function
submit_button.on_click(place_bet)


# Define button click action for navigation
def navigate_to_bet(event):
    # Replace 'http://localhost:5007/' with the correct URL where bet.py is served
    webbrowser.open_new_tab('http://localhost:5007/')


navigate_button.on_click(navigate_to_bet)

# Layout for the Main Page (Using CSS class for centered text)
main_page = pn.Column(
    pn.pane.Markdown("# 🍺 BeerBets Prediction Market 🍺", css_classes=['centered-text']),
    bet_input,
    submit_button,
    output_text,
    pn.layout.Spacer(height=20),
    navigate_button
)

# ================================
# Betting Page Components (from bet.py)
# ================================

# [Betting page components remain unchanged]

# (Omitting for brevity; ensure no 'style' parameters are used in this section)

# ================================
# Combined Layout using Tabs
# ================================

# Create Tabs for Main Page and Betting Page
tabs = pn.Tabs(
    ("Home", main_page),
    ("Betting", bet_page),
    dynamic=True
)

# Define Template
template = pn.template.FastListTemplate(
    title="🍺 BeerBets Prediction Market 🍺",
    accent_base_color=ACCENT,
    header_background=ACCENT,
    theme_toggle=False,
    theme='dark',
    main=tabs  # Add Tabs to the main area of the template
)

# Serve the Template
if pn.state.served:
    template.servable()