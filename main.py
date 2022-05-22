"""
Created on 25/03/2022
@author: GuzH
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from leaguepedia_requests import queryPlayersDataTableForAllTournaments, queryPlayersDataTableForLastTournament, queryPlayersNames

def main():
    # Setea los títulos y subtítulos de la página
    st.set_page_config(page_title="Historial Ecuador",layout="wide",initial_sidebar_state="expanded")
    st.title("Historial de jugadores Ecuador")

    # Consigue toda la data
    dataLastTournament = queryPlayersDataTableForLastTournament()
    data = queryPlayersDataTableForAllTournaments()
    players = queryPlayersNames()
    
    # DataFrame all data
    datalastdf = pd.DataFrame(dataLastTournament)
    datadf = pd.DataFrame(data)
    playersdf = pd.DataFrame(players)

    # Ordena a los nombres de los jugadores por equipo
    playersdf = playersdf.sort_values('Team')

    # Arma la lista de jugadores para crear el select
    players_list = playersdf['Team'] + ' | ' + playersdf['ID']

    # Crea un Select Box para elegir el jugador
    player_name = st.selectbox("Jugador", players_list)

    player_data_last_tournament = []
    player_data_all_tournaments = []

    if 'Name' in datalastdf:
        player_data_last_tournament = datalastdf[datalastdf.Name == player_name.split(' | ')[1]]
    
    if 'Name' in datadf:
        player_data_all_tournaments = datadf[datadf.Name == player_name.split(' | ')[1]]

    # Divide el espacio en dos columnas (por ahora no es la idea dividir)
    # col1, col2 = st.columns(2)

    # Tabla de arriba: muestra el historial del torneo vigente
    st.write("Historial del torneo vigente:")
    st.dataframe(player_data_last_tournament,950)

    # Tabla de abajo: muestra el historial del jugador
    # with col1: (por ahora no es la idea dividir)
    st.write("Historial de todos los torneos:")
    st.dataframe(player_data_all_tournaments,950)
        
    # Gráfico pie: muestra todos sus campeones jugados en un grafico circular
    # with col2: (por ahora no es la idea dividir)
    # https://plotly.com/python/pie-charts/
    fig = []

    if 'Champion' in player_data_all_tournaments:
        fig = px.pie(player_data_all_tournaments, names='Champion', title="Campeones jugados:")
        fig.update_traces(textinfo='value')
        st.plotly_chart(fig)
        # Hace un histograma al final de la página con las wins sumadas de cada campeón para el jugador elegido
        fig = px.histogram(player_data_all_tournaments, x="Champion", color="Champion", y="Win", title="Victorias por campeón")
        fig.update_layout(barmode='stack', xaxis={'categoryorder': 'category ascending'})
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()