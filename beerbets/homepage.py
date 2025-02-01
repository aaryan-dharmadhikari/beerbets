# beerbets/beerbets/homepage.py
import pandas as pd
import panel as pn

# Initialize Panel extension
pn.extension('plotly', 'tabulator')

def create_homepage():
    # Sample data for current bets
    data = {
        'Bet': ['Bet 1', 'Bet 2', 'Bet 3'],
        'Odds': [2.5, 1.8, 3.0],
        'Amount': [100, 150, 200]
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Create a Tabulator widget to display the bets
    bets_table = pn.widgets.Tabulator(df, show_index=False, height=200)

    # Create a Markdown pane for the title
    title = pn.pane.Markdown("# Current Bets")

    # Create a layout
    layout = pn.Column(
        title,
        bets_table
    )

    return layout