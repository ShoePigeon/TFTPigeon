from src.models.db import get_db
from pulsefire.clients import RiotAPIClient
import requests

apiKey = "RGAPI-1d388562-de0c-47e8-8e9b-35fdd87c24cf"
def get_match_info(username, tagLine):
    puuid = get_puuid(username, tagLine)
    if not puuid:
        return None, "Failed to retrieve PUUID for the user."
    match_ids = get_matchHistory(puuid)
    if not match_ids:   
        return None, "No match history found for the user."
    match_data = []
    #This gets every matches data for the user
    for match_id in match_ids:
        match_info = get_matchData(match_id)
        match_info = filter_matchData(match_info)
        if not match_info:
            return None, f"Failed to retrieve data for match ID: {match_id}"
        match_data.append(match_info)
    #TODO: Add logic to specify match_data as needed
    return match_data[0], None
    # return match_data, None


def get_puuid(gameName, tagLine):
    
    gameName = "CR17FT"
    tagLine = "NA1"
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"

    headers = {
        "X-Riot-Token": apiKey
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(data)
        return data["puuid"]
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
def get_matchHistory(puuid):
    url = f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?start=0&count=20"

    headers = {
        "X-Riot-Token": apiKey
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        matchList = response.json()
        print(matchList)
        return matchList
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
def get_matchData(matchID):
    url = f"https://americas.api.riotgames.com/tft/match/v1/matches/{matchID}"
    headers = {
        "X-Riot-Token": apiKey
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        matchList = response.json()
        print(matchList)
        return matchList
        # return matchList["info"]["participants"]
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
# # Now call get_match_info_sync normally
# match_info = get_match_info_sync("some_username", "some_match_id")
# print(match_info)


def filter_matchData(match_info):
    if not match_info or "info" not in match_info:
        return None

    # Extract relevant data from each participant
    filtered_data = match_info["info"]
    return filtered_data