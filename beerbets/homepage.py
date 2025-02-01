import panel as pn
import os
import pandas as pd
import random
from random import randint, choice  # Added choice for random emoji selection
from datetime import datetime, timedelta

# Start Panel extension
pn.extension()
random.seed(42)

# Define image directory
image_dir = os.path.join(os.getcwd(), "images")

# Dummy data: List of events and associated images
import panel as pn
import os
import pandas as pd
from random import randint, choice
from datetime import datetime, timedelta

# Start Panel extension
pn.extension()

# Define image directory
image_dir = os.path.join(os.getcwd(), "images")

# Generate dummy data with correctly assigned expiry dates
events_data = {
    "Event": [
        "Will Sumith be bald by 2030?", 
        "Will Ali find a girlfriend by the end of the year?", 
        "Will Johns fail Non-Euclidean methods?",
        "Will IC Hack 26 have more than 500 participants?",
        "Will the Department of Computing actually move to White City by 2028?"
    ],
    "Image": [
        os.path.join(image_dir, "rogaine.jpeg"),
        os.path.join(image_dir, "ali.png"),
        os.path.join(image_dir, "johns.png"),
        os.path.join(image_dir, "ichack.png"),
        os.path.join(image_dir, "doc.png"),
    ],
    "Ranking": sorted([randint(0, 100) for _ in range(5)], reverse=True),  # Sorted by popularity
    "Volume": sorted([randint(10, 200) for _ in range(5)]),  # Sorted for better UI ordering
    "Unit": [choice(["🍺 beers", "🍦 ice creams", "🍽️ dinner"]) for _ in range(5)],  # Random units
    "Expiry": [
        datetime(2031, 1, 1, 0, 0),  # Sumith bald -> Check on Jan 1, 2031
        datetime(datetime.now().year, 12, 31, 23, 59),  # Ali girlfriend -> End of this year
        datetime.now() + timedelta(days=randint(60, 120)),  # Johns failing -> A few months from now
        datetime(2026, 2, 1, 0, 0),  # IC Hack 26 -> Set after the hackathon
        datetime(2028, 12, 31, 23, 59)  # DoC move -> End of 2028
    ]
}

# Create a DataFrame
df = pd.DataFrame(events_data)

# Search widget
search_box = pn.widgets.TextInput(name='Search Event', placeholder='Search for an event', sizing_mode="stretch_width")

# Create Tabs (Make closeable, except for main tab)
tabs = pn.Tabs(("Home", None), closable=True, sizing_mode="stretch_width")

# Function to create event details view
def open_event_view(event_name):
    """Opens a new tab with event details."""
    for i in range(1, len(tabs)):  # Prevent duplicate tabs
        if tabs[i][0] == event_name:
            return

    new_tab = pn.Column(
        pn.pane.Markdown(f"# 📝 {event_name}", sizing_mode="stretch_width"),
        pn.pane.Markdown("### TODO: Event details and betting options will be displayed here.", sizing_mode="stretch_width"),
        sizing_mode="stretch_width"
    )
    tabs.append((event_name, new_tab))

# Function to display event cards
def create_event_cards(events_df):
    cards = []
    for _, row in events_df.iterrows():
        image = pn.pane.Image(row['Image'], width=200, sizing_mode="fixed")
        event_button = pn.widgets.Button(name=row['Event'], button_type="primary", sizing_mode="scale_width")
        event_button.on_click(lambda event, name=row['Event']: open_event_view(name))

        ranking = pn.pane.Markdown(f"**Bets Count**: {row['Ranking']}", sizing_mode="stretch_width")
        volume = pn.pane.Markdown(f"**Total Betting Volume**: {row['Volume']:,} {row['Unit']}", sizing_mode="stretch_width")  # Random emoji
        expiry_date = pn.pane.Markdown(f"**Expiry Date**: {row['Expiry'].strftime('%Y-%m-%d %H:%M:%S')}", sizing_mode="stretch_width")
        
        event_card = pn.Row(
            image, 
            pn.Column(
                event_button, 
                ranking, 
                volume, 
                expiry_date, 
                align="center",
                sizing_mode="scale_width"
            ),
            sizing_mode="scale_width"
        )
        cards.append(event_card)

    return pn.Column(*cards, sizing_mode="stretch_width")

def search_events(event):
    query = search_box.value.lower()
    filtered_df = df[df["Event"].str.contains(query, case=False, na=False)]
    event_cards.objects = create_event_cards(filtered_df).objects  

# Bind search function
search_box.param.watch(search_events, 'value')

# Initial event list
event_cards = create_event_cards(df)

# Layout
homepage = pn.Column(
    pn.pane.Markdown("# 🎲 Current Betting Events 🎲", sizing_mode="stretch_width"),
    search_box,
    event_cards,
    sizing_mode="stretch_width"
)

# Set homepage inside tabs
tabs[0] = ("Home", homepage)
