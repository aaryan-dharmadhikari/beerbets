import panel as pn

# Start Panel extension
pn.extension()

# Create input and button widgets
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

# Layout
app = pn.Column(
    pn.pane.Markdown("# 🍺 BeerBets Prediction Market 🍺"),
    bet_input,
    submit_button,
    output_text
)

# Run the app
app.show()

