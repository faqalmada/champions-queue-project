"""
Created on 13/03/2022
@author: GuzH
"""

import streamlit as st
import pandas as pd
from mwrogue.esports_client import EsportsClient
import json
import plotly.express as px

st.set_page_config(page_title="Test APP",layout="wide",initial_sidebar_state="expanded")
st.title("Test APP: Historial De Jugadores")
st.subheader("Liga Master Flow 2022 / Opening Season:")
st.subheader("Players de EBRO Gaming")

# Get all data
@st.cache(persist=True)
def queryPlayersDataTable():
    # Esta función recibe un EsportsClient(site) y una query de Leaguepedia con los siguientes campos: 
    # "P.OverviewPage, P.ID, P.Name, P.Country, P.Age, P.Role, P.Team"

    # Llamada a la API de Leaguepedia
    site= EsportsClient('lol')

    # Query de Leaguepedia para Players: EBRO
    response = site.cargo_client.query(
        # Todos los Players
        limit = "max",
        # Que aparecen en la tabla Players: https://lol.fandom.com/wiki/Special:CargoTables/Players
        tables = "Players=P",
        # Visualizando solo los siguientes datos
        fields = "P.OverviewPage, P.ID, P.Name, P.Country, P.Age, P.Role, P.Team",
        # Solamente aquellos que sean de la Liga Master Flow 2022 Apertura, y que hayan concluido
        where = "(P.Team='EBRO') AND (P.IsRetired=FALSE) AND (P.ToWildrift=FALSE) AND " +
                "(P.Role='Top' OR P.Role='Jungle' OR P.Role ='Mid' OR P.Role='Bot' OR P.Role='Support')",
        order_by= "P.ID ASC"
    )

    datatable=[]
    players = json.loads(json.dumps(response))
    
    for player in players:
            
        responseGetAccurateName = site.cargo_client.query(
            # Todos los nombres
            limit = "max",
            # Que tiene un jugador
            tables = "PlayerRedirects=PR",
            # Visualizando los siguientes datos
            fields = "PR.OverviewPage, PR.AllName",
            # Solamente aquellos que tengan el mismo OverviewPage
            where = "PR.OverviewPage='" + player['OverviewPage'] + "'"
        )
        
        names = []
        names = json.loads(json.dumps(responseGetAccurateName))
        
        for name in names:
            responseMatchesPlayer = site.cargo_client.query(
                    # Todos los champions jugados
                    limit = "max",
                    # Que aparecen en la tabla ScoreboardPlayers: https://lol.fandom.com/wiki/Special:CargoTables/ScoreboardPlayers
                    tables = "ScoreboardPlayers=SP",
                    # Visualizando solo los siguientes datos
                    fields = "SP.Name, SP.Link, SP.Champion, SP.Kills, SP.Deaths, SP.Assists, SP.PlayerWin=Win, SP.DateTime_UTC, ",
                    where = "SP.Link='" + name['AllName'] + "' AND (SP.OverviewPage='Liga Master Flow/2022 Season/Opening Season' OR SP.OverviewPage='Liga Master Flow/2022 Season/Opening Playoffs')",
                    order_by= "SP.DateTime_UTC DESC"
                )
            
            matches = json.loads(json.dumps(responseMatchesPlayer))
            
            for match in matches:
                if match['Win'] == 'Yes':
                    match['Win'] = 1
                else:
                    match['Win'] = 0
                match.popitem()
                match.pop("Link")
            
            datatable.extend(matches)
    
    return datatable

@st.cache
def queryPlayersNames():
    # Esta función usa un EsportsClient(site) y una query de LeaguePedia con los siguientes campos:
    # "P.OverviewPage, P.ID, P.Name, P.Country, P.Age, P.Role, P.Team"
    
    # Llamada a la API de Leaguepedia
    site= EsportsClient('lol')
    
    # Query de Leaguepedia para Players: EBRO
    response = site.cargo_client.query(
        # Todos los Players
        limit = "max",
        # Que aparecen en la tabla Players: https://lol.fandom.com/wiki/Special:CargoTables/Players
        tables = "Players=P",
        # Visualizando solo los siguientes datos
        fields = "P.OverviewPage, P.ID, P.Name, P.Country, P.Age, P.Role, P.Team",
        # Solamente aquellos que sean de la Liga Master Flow 2022 Apertura, y que hayan concluido
        where = "(P.Team='EBRO') AND P.IsRetired=FALSE AND P.ToWildrift=FALSE AND " +
                "(P.Role='Top' OR P.Role='Jungle' OR P.Role ='Mid' OR P.Role='Bot' OR P.Role='Support')",
        order_by= "P.ID ASC"
    )

    players = json.loads(json.dumps(response))
    return players

data = queryPlayersDataTable()
datadf = pd.DataFrame(data)

players = queryPlayersNames()
playersdf = pd.DataFrame(players)

players_list = playersdf.sort_values('ID')['ID']

player_name = st.selectbox("Elige un jugador", players_list)
player_data = datadf[datadf.Name == player_name]

col1, col2 = st.columns(2)

with col1:
    st.write("Historial:")
    st.dataframe(player_data,800,337)
    
with col2:
    # Group the match history by champion to see which ones were played the most
    # Check plotly doc here: https://plotly.com/python/pie-charts/
    fig = px.pie(player_data, names='Champion', title="Campeones Jugados:")
    fig.update_traces(textinfo='value')
    # Once again streamlit has a way to display what we want
    st.plotly_chart(fig)

fig = px.histogram(player_data, x="Champion", color="Champion", y="Win", title="Wins")
fig.update_layout(barmode='stack', xaxis={'categoryorder': 'category ascending'})
st.plotly_chart(fig)
