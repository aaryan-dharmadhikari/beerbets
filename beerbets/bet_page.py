# bet.py

import pandas as pd
import panel as pn
import plotly.express as px

# Initialize Panel extension
pn.extension('plotly', 'tabulator')

# Define accent colors to match main.py
ACCENT = "#BB2649"
RED = "#D94467"
GREEN = "#5AD534"

# Sample Data for Markets with Fixed Dates
market_data = {
    'Market A': {
        'description': 'Market A Description: Predict the outcome of Event A.',
        'price_history': pd.DataFrame({
            'Time': pd.date_range(start='2024-01-01', periods=10, freq='D'),
            'Price': [2.5, 2.4, 2.6, 2.5, 2.7, 2.8, 2.75, 2.7, 2.65, 2.6],
        }),
        'closing_time': '2024-02-15 18:00:00'
    },
    'Market B': {
        'description': 'Market B Description: Predict the outcome of Event B.',
        'price_history': pd.DataFrame({
            'Time': pd.date_range(start='2024-01-05', periods=8, freq='D'),
            'Price': [1.6, 1.7, 1.65, 1.7, 1.68, 1.65, 1.7, 1.72],
        }),
        'closing_time': '2024-01-20 12:00:00'
    },
    # Add more markets as needed with fixed dates
}

# Global Variables
USER_BALANCE = 10  # Starting balance for the user
placed_bets = []  # Store placed bets as a list of dictionaries

# Widgets
market_selector = pn.widgets.Select(
    name="Select Market",
    options=list(market_data.keys()),
    value='Market A',
    width=300
)

market_description = pn.pane.Markdown("### Market Description", width=400)

price_history_plot = pn.pane.Plotly(height=300, sizing_mode='stretch_width')

closing_time_display = pn.pane.Markdown("**Closing Time:** N/A", width=400)

bet_option = pn.widgets.RadioButtonGroup(
    name="Bet Option",
    options=["Yes", "No"],
    button_type='success'
)

bet_amount = pn.widgets.IntSlider(
    name="Bet Amount",
    start=1,
    end=USER_BALANCE,
    step=1,
    value=1,
    width=300
)

submit_bet_button = pn.widgets.Button(
    name="Place Bet",
    button_type="primary",
    width=150
)

bet_feedback = pn.pane.Markdown("### Feedback will appear here.", width=400)

user_balance_display = pn.pane.Markdown(f"**Your Balance:** {USER_BALANCE} beers", width=200)

placed_bets_pane = pn.widgets.Tabulator(
    pd.DataFrame(placed_bets),
    name="Your Bets",
    disabled=True,
    height=200
)

reset_button = pn.widgets.Button(
    name="🔙 Reset",
    button_type="warning",
    width=200
)


# Functions

def update_market_details(market):
    """Update the market description, price history plot, and closing time based on selected market."""
    details = market_data.get(market, {})
    description_md = f"### {market}\n\n{details.get('description', 'No description available.')}"
    market_description.object = description_md

    # Update Closing Time
    closing_time = details.get('closing_time', 'N/A')
    closing_time_display.object = f"**Closing Time:** {closing_time}"

    # Plot Price History
    price_df = details.get('price_history')
    if price_df is not None:
        fig = px.line(price_df, x='Time', y='Price', title='Price History')
        price_history_plot.object = fig
    else:
        price_history_plot.object = "No price history available."

    # Update bet_amount slider
    bet_amount.end = USER_BALANCE if USER_BALANCE > 0 else 1
    bet_amount.value = min(bet_amount.value, USER_BALANCE) if USER_BALANCE > 0 else 1


def place_bet(event):
    """Handle placing a bet."""
    global USER_BALANCE
    selected_market = market_selector.value
    chosen_option = bet_option.value
    amount = bet_amount.value

    if not selected_market or not chosen_option:
        bet_feedback.object = "⚠️ Please select both a market and an option to place a bet."
        return

    if amount > USER_BALANCE:
        bet_feedback.object = "⚠️ Insufficient balance to place this bet."
        return

    # Deduct amount from balance
    USER_BALANCE -= amount
    user_balance_display.object = f"**Your Balance:** {USER_BALANCE} beers"

    # Record the bet with fixed date
    placed_bets.append({
        "Market": selected_market,
        "Bet On": chosen_option,
        "Amount": amount,
        "Date": '2024-01-10 14:30:00'  # Fixed date for demonstration
    })

    # Update placed bets table
    placed_bets_pane.value = pd.DataFrame(placed_bets)

    # Provide feedback
    bet_feedback.object = f"""✅ **Bet Placed Successfully!**
- **Market:** {selected_market}
- **Bet On:** {chosen_option}
- **Amount:** {amount} beers"""


def reset_page(event):
    """Reset the betting page to its initial state."""
    global USER_BALANCE, placed_bets
    USER_BALANCE = 10
    placed_bets = []
    user_balance_display.object = f"**Your Balance:** {USER_BALANCE} beers"
    bet_feedback.object = "### Feedback will appear here."
    bet_amount.end = USER_BALANCE
    bet_amount.value = 1
    placed_bets_pane.value = pd.DataFrame(placed_bets)
    market_selector.value = list(market_data.keys())[0]
    bet_option.active = None


# Event Listeners
market_selector.param.watch(lambda event: update_market_details(event.new), 'value')
submit_bet_button.on_click(place_bet)
reset_button.on_click(reset_page)

# Initialize with the default market
update_market_details(market_selector.value)

# Layout
bet_page = pn.Column(
    pn.pane.Markdown("# 🍺 BeerBets Prediction Market 🍺"),
    pn.Row(market_selector, user_balance_display),
    pn.Row(
        pn.Column(market_description, closing_time_display),
        pn.Column(price_history_plot),
        sizing_mode='stretch_width'
    ),
    pn.Row(bet_option, bet_amount, submit_bet_button, sizing_mode='stretch_width'),
    bet_feedback,
    pn.pane.Markdown("## Your Placed Bets"),
    placed_bets_pane,
    pn.layout.Divider(),
    reset_button,
    sizing_mode='stretch_width',
    css_classes=["bet-page"]
)

# Define template to match main.py
template = pn.template.FastListTemplate(
    title="🍺 BeerBets Prediction Market 🍺",
    accent_base_color=ACCENT,
    header_background=ACCENT,
    theme_toggle=False,
    theme='dark',
)

template.main.append(bet_page)

# Serve the template
if pn.state.served:
    template.servable()