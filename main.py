"""
Created on 13/03/2022
@author: GuzH
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from leaguepedia_requests import queryPlayersDataTable, queryPlayersNames

def main():
    st.set_page_config(page_title="Test APP",layout="wide",initial_sidebar_state="expanded")
    st.title("Test APP: Historial De Jugadores")
    st.subheader("Liga Master Flow 2022 / Opening Season:")
    st.subheader("Players de EBRO Gaming")

    # Get all data
    data = queryPlayersDataTable()
    players = queryPlayersNames()
    
    # DataFrame all data
    datadf = pd.DataFrame(data)
    playersdf = pd.DataFrame(players)

    # Sort all players by ID
    players_list = playersdf.sort_values('ID')['ID']

    # Add a Select Box
    player_name = st.selectbox("Elige un jugador", players_list)
    player_data = datadf[datadf.Name == player_name]

    # Divide on two columns
    col1, col2 = st.columns(2)

    # Column 1
    with col1:
        st.write("Historial:")
        st.dataframe(player_data,800,337)
        
    # Column 2
    with col2:
        # Group the match history by champion to see which ones were played the most
        # Check plotly doc here: https://plotly.com/python/pie-charts/
        fig = px.pie(player_data, names='Champion', title="Campeones Jugados:")
        fig.update_traces(textinfo='value')
        st.plotly_chart(fig)

    # Histogram on bottom
    fig = px.histogram(player_data, x="Champion", color="Champion", y="Win", title="Wins")
    fig.update_layout(barmode='stack', xaxis={'categoryorder': 'category ascending'})
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
    
    st.write("Made by [GuzH](https://twitter.com/guzhotero) - See the [whole code here]("")")