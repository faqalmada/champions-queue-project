"""
Created on 25/03/2022
@author: GuzH
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from leaguepedia_requests import queryPlayersDataTable, queryPlayersNames

def main():
    # Setea los títulos y subtítulos de la página
    st.set_page_config(page_title="Test APP",layout="wide",initial_sidebar_state="expanded")
    st.title("Test APP: Historial De Jugadores")
    st.subheader("Volcano League 2022 / Opening Season | Playoffs:")
    st.subheader("Players de Ecuador")

    # Consigue toda la data
    data = queryPlayersDataTable()
    players = queryPlayersNames()
    
    # DataFrame all data
    datadf = pd.DataFrame(data)
    playersdf = pd.DataFrame(players)

    # Ordena a los nombres de los jugadores alfabeticamente
    players_list = playersdf['Team'] + ' | ' + playersdf.sort_values('Team')['ID']

    # Crea un Select Box para elegir el jugador
    player_name = st.selectbox("Elige un jugador", players_list)
    player_data = datadf[datadf.Name == player_name.split(' | ')[1]]

    # Divide el espacio en dos columnas
    col1, col2 = st.columns(2)

    # Columna una: Muestra el historial del jugador
    with col1:
        st.write("Historial:")
        st.dataframe(player_data,800,337)
        
    # Columna dos: Muestra todos sus campeones jugados en un grafico circular
    with col2:
        # https://plotly.com/python/pie-charts/
        fig = px.pie(player_data, names='Champion', title="Campeones Jugados:")
        fig.update_traces(textinfo='value')
        st.plotly_chart(fig)

    # Hace un histograma al final de la página con las wins sumadas de cada campeón para el jugador elegido
    fig = px.histogram(player_data, x="Champion", color="Champion", y="Win", title="Wins")
    fig.update_layout(barmode='stack', xaxis={'categoryorder': 'category ascending'})
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()