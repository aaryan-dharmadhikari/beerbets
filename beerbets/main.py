# beerbets/beerbets/main.py
import panel as pn
from beerbets.homepage import tabs

# Initialize Panel extension
pn.extension('plotly', 'tabulator')

# Create widgets
bet_input = pn.widgets.TextInput(name="Your Bet", placeholder="Enter your bet here...")
submit_button = pn.widgets.Button(name="Place Bet", button_type="primary")
output_text = pn.pane.Markdown("### Your bet will appear here.", width=400)

# Define button click action
def place_bet(event):
    if bet_input.value:
        output_text.object = f"**You bet on:** {bet_input.value}"
    else:
        output_text.object = "⚠️ Please enter a bet!"

# Link button click to function
submit_button.on_click(place_bet)

# Layout for placing bets
betting_layout = pn.Column(
    pn.pane.Markdown("# 🍺 BeerBets Prediction Market 🍺"),
    bet_input,
    submit_button,
    output_text
)

# Define template
ACCENT = "#BB2649"
template = pn.template.FastListTemplate(
    title="🍺 BeerBets Prediction Market 🍺",
    accent_base_color=ACCENT,
    header_background=ACCENT,
    theme_toggle=False,
    theme='dark',
)

# Add the betting layout and homepage layout to the template
# template.main.append(betting_layout)
template.main.append(tabs)

# Serve the app
if pn.state.served:
    template.servable()