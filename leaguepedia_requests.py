from mwrogue.esports_client import EsportsClient
import json
import streamlit as st

@st.cache(persist=True)
def queryPlayersDataTable():
    # Esta función devuelve una lista de diccionarios con 

    # Crea un cliente de leaguepedia
    site= EsportsClient('lol')

    # Query de Leaguepedia: Busca 
    response = site.cargo_client.query(
        # Todos los Players
        limit = "max",
        # Que aparecen en la tabla Players: https://lol.fandom.com/wiki/Special:CargoTables/Players
        tables = "Players=P",
        # Visualizando solo los siguientes datos
        fields = "P.OverviewPage, P.ID, P.Name, P.Country, P.Age, P.Role, P.Team",
        # Solamente aquellos que sean de EBRO.
        where = "(P.Team='EBRO') AND (P.IsRetired=FALSE) AND (P.ToWildrift=FALSE) AND " +
                "(P.Role='Top' OR P.Role='Jungle' OR P.Role ='Mid' OR P.Role='Bot' OR P.Role='Support')",
        order_by= "P.ID ASC"
    )

    datatable=[]
    players = json.loads(json.dumps(response))
    
    for player in players:
        # Para cada uno de los players
        responseGetAccurateName = site.cargo_client.query(
            limit = "max",
            # Buscamos todos sus nombres
            tables = "PlayerRedirects=PR",
            fields = "PR.OverviewPage, PR.AllName",
            where = "PR.OverviewPage='" + player['OverviewPage'] + "'"
        )
        
        names = []
        names = json.loads(json.dumps(responseGetAccurateName))
        
        for name in names:
            # Para cada uno de los nombres que tuvo el jugador, buscamos sus partidas
            # Esto es para evitar perder partidas debido a cambios de nombres
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
            
            # Cambios los Winners="Yes" por "1"s para que sea más fácil de calcular
            for match in matches:
                if match['Win'] == 'Yes':
                    match['Win'] = 1
                else:
                    match['Win'] = 0
                match.popitem()
                match.pop("Link")
            
            datatable.extend(matches)
    
    # Devolvemos la lista completa con todos los partidos de todos los jugadores
    return datatable

@st.cache
def queryPlayersNames():
    #Esta función es para conseguir todos los nombres de los jugadores y usarlos en la Select Box.
    
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
        # Solamente aquellos que sean de EBRO.
        where = "(P.Team='EBRO') AND P.IsRetired=FALSE AND P.ToWildrift=FALSE AND " +
                "(P.Role='Top' OR P.Role='Jungle' OR P.Role ='Mid' OR P.Role='Bot' OR P.Role='Support')",
        order_by= "P.ID ASC"
    )

    players = json.loads(json.dumps(response))
    return players