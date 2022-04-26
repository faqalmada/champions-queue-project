from mwrogue.esports_client import EsportsClient
import json
import streamlit as st

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