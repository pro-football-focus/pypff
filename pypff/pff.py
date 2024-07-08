#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:09:12 2022

@author: apschram
"""
import requests
import pandas as pd
import tqdm

def get_competitions(url, key):
    ''' 
    Retrieves information of all competitions available for the given API key.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key

    Returns
    ---------
    
    df: a dataframe containing the competition information
    
    '''
    payload = "{\"query\":\"query competitions {\\n    competitions {\\n        id\\n        name\\n        games {\\n            id\\n            season\\n        }\\n    }\\n}\",\"variables\":{}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)
    
    try:
        df = pd.DataFrame.from_dict(response.json()['data']['competitions'])
        return df.infer_objects()
    except:
        print(response.text)

def get_competition(url, key, competition_id):
    ''' 
    Retrieves information of a competition for a given competition_id.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API 
    competition_id: an integer to select the competition

    Returns
    ---------
    
    df: a dataframe containing the competition information
    
    '''
    payload = "{\"query\":\"query competition ($id: ID!) {\\n    competition (id: $id) {\\n        id\\n        name\\n        games {\\n            id\\n            season\\n        }\\n    }\\n}\",\"variables\":{\"id\":" + str(competition_id) + "}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)

    try:
        df = pd.DataFrame(response.json()['data']['competition'])
        return df.infer_objects()
    except:
        print(response.text)

def get_teams(url, key):
    ''' 
    Retrieves information of all teams available for the given API key.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key

    Returns
    ---------
    
    df: a dataframe containing the team information
    
    '''
    payload = "{\"query\":\"query teams {\\n    teams {\\n        id\\n        name\\n        shortName\\n        country\\n        homeGames {\\n            id\\n        }\\n        awayGames {\\n            id\\n        }\\n        kits {\\n            id\\n            name\\n            primaryColor\\n            secondaryColor\\n            primaryTextColor\\n            secondaryTextColor\\n        }\\n        homeStadium {\\n            id\\n            name\\n            pitchLength\\n            pitchWidth\\n        }\\n    }\\n}\",\"variables\":{}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)
    
    try:
        df = pd.DataFrame.from_dict(response.json()['data']['teams'])
        return df.infer_objects()
    except:
        print(response.text)        

def get_team(url, key, team_id):
    ''' 
    Retrieves information of a team for a given team_id.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key
    team_id: an integer to select the team


    Returns
    ---------
    
    df: a dataframe containing the team information
    
    '''
    payload = "{\"query\":\"query team ($id: ID!) {\\n    team (id: $id) {\\n        id\\n        name\\n        shortName\\n        country\\n        homeGames {\\n            id\\n        }\\n        awayGames {\\n            id\\n        }\\n        kits {\\n            id\\n            name\\n            primaryColor\\n            secondaryColor\\n            primaryTextColor\\n            secondaryTextColor\\n        }\\n        homeStadium {\\n            id\\n            name\\n            pitchLength\\n            pitchWidth\\n        }\\n    }\\n}\",\"variables\":{\"id\":" + str(team_id) + "}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)

    try:
        df = pd.DataFrame(response.json()['data']['team'].items()).T
        df.columns = df.loc[0]
        df = df[df['awayGames'] != 'awayGames'].reset_index(drop = True)
        return df.infer_objects()
    except:
        print(response.text)

def get_games(url, key, competition_id):
    ''' 
    Retrieves information of all games available in a given competition.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key
    competition_id: an integer to select the competition

    Returns
    ---------
    
    df: a dataframe containing the game information
    
    '''
    payload = "{\"query\":\"query competition ($id: ID!) {\\n    competition (id: $id) {\\n        id\\n        name\\n        games {\\n            id\\n            date\\n            season\\n            week\\n            homeTeam {\\n                id\\n                name\\n                shortName\\n            }\\n            awayTeam {\\n                id\\n                name\\n                shortName\\n            }\\n            startPeriod1\\n            endPeriod1\\n            startPeriod2\\n            endPeriod2\\n            period1\\n            period2\\n            halfPeriod\\n            homeTeamStartLeft\\n            homeTeamKit {\\n                name\\n                primaryColor\\n                primaryTextColor\\n                secondaryColor\\n                secondaryTextColor\\n            }\\n            awayTeamKit {\\n                name\\n                primaryColor\\n                primaryTextColor\\n                secondaryColor\\n                secondaryTextColor\\n            }\\n            stadium {\\n                id\\n                name\\n                pitchLength\\n                pitchWidth\\n            }\\n            videos {\\n                id\\n                fps\\n                videoUrl\\n            }\\n        }\\n    }\\n}\",\"variables\":{\"id\":" + str(competition_id) + "}}"
    
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)
    
    try:
        df = pd.DataFrame.from_dict(response.json()['data']['competition']['games'])
        
        competition = pd.DataFrame(index = df.index)
        competition.loc[:,'id'] = response.json()['data']['competition']['id']
        competition.loc[:,'name'] = response.json()['data']['competition']['name']
        competition['competition'] = competition[['id','name']].to_dict(orient = 'records')
        
        df = df.merge(competition[['competition']], how = 'left', left_index = True, right_index = True)
        df = df.reindex(sorted(df.columns), axis = 1).infer_objects()
        return df.infer_objects()
    except:
        print(response.text)

def get_game(url, key, game_id):
    ''' 
    Retrieves information of a game for a given game_id.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key
    game_id: an integer to select the game


    Returns
    ---------
    
    df: a dataframe containing the game information
    
    '''
    payload = "{\"query\":\"query game ($id: ID!) {\\n    game (id: $id) {\\n        id\\n        competition {\\n            id\\n            name\\n        }\\n        date\\n        stadium{\\n            id\\n            name\\n        pitchLength\\n        pitchWidth\\n        }\\n        videos{\\n            id\\n            fps\\n        \\n            videoUrl}\\n        season\\n        week\\n        homeTeam {\\n            id\\n            name\\n            shortName\\n        }\\n        awayTeam {\\n            id\\n            name\\n            shortName\\n        }\\n        startPeriod1\\n        endPeriod1\\n        startPeriod2\\n        endPeriod2\\n        period1\\n        period2\\n        halfPeriod\\n        homeTeamStartLeft\\n        homeTeamKit {\\n            name\\n            primaryColor\\n            primaryTextColor\\n            secondaryColor\\n            secondaryTextColor\\n        }\\n        awayTeamKit {\\n            name\\n            primaryColor\\n            primaryTextColor\\n            secondaryColor\\n            secondaryTextColor\\n        }\\n    }\\n}\",\"variables\":{\"id\":" + str(game_id) + "}}"

    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)
    
    try:
        df = pd.DataFrame(response.json()['data']['game'].items()).T
        df.columns = df.loc[0]
        df = df[df['awayTeam'] != 'awayTeam'].reset_index(drop = True)
        return df.infer_objects()
    except:
        print(response.text)

def get_players_competition(url, key, competition_id):
    ''' 
    Retrieves information of all players available in a given competition.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key
    competition_id: an integer to select the competition

    Returns
    ---------
    
    df: a dataframe containing the player information
    
    '''
    payload = "{\"query\":\"query competition ($id: ID!) {\\n    competition (id: $id) {\\n        games {\\n            rosters {\\n                player {\\n                    id\\n                    firstName\\n                    lastName\\n                    nickname\\n                    positionGroupType\\n                    nationality {\\n                        id\\n                        country\\n                    }\\n                    secondNationality {\\n                        id\\n                        country\\n                    }\\n                    weight\\n                    height\\n                    dob\\n                    gender\\n                    countryOfBirth {\\n                        id\\n                        country\\n                    }\\n                    euMember\\n                transfermarktPlayerId\\n}\\n            }\\n        }\\n    }\\n}\",\"variables\":{\"id\":" + str(competition_id) + "}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)

    try:
        df = pd.DataFrame(response.json()['data']['competition']['games'])
        df = df['rosters'].apply(pd.Series)
        df = df.dropna(how = 'all', axis = 0)
        
        oneCol = []
        colLength = len(list(df.columns))
        for k in range(colLength):
            oneCol.append(df[k])
        
        df = pd.concat(oneCol, ignore_index = True)
        df = df.apply(pd.Series)['player'].apply(pd.Series)
        
        df = df.reset_index(drop = False)
        df['rank'] = df.groupby('id')['index'].rank('dense', ascending = False)
        df = df[df['rank'] == 1]
        # df = df.drop_duplicates()
        df = df.drop(columns = [0,'index','rank'])
        df = df.dropna(how = 'all', axis = 0)
        
        df['id'] = df['id'].astype(int)
        
        return df.infer_objects()
    except:
        print(response.text)

def get_player(url, key, player_id):
    ''' 
    Retrieves information of a player for a given player_id.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key
    player_id: an integer to select the player

    Returns
    ---------
    
    df: a dataframe containing the player information
    
    '''
    payload = "{\"query\":\"query player ($id: ID!) {\\n    player (id: $id) {\\n        id\\n        firstName\\n        lastName\\n        nickname\\n        positionGroupType\\n        nationality {\\n            id\\n            country\\n        }\\n        secondNationality {\\n            id\\n            country\\n        }\\n        weight\\n        height\\n        dob\\n        gender\\n        countryOfBirth {\\n            id\\n            country\\n        }\\n        euMember\\n        rosters {\\n            game {\\n                id\\n            }\\n            started\\n        }\\n        transfermarktPlayerId\\n    }\\n}\",\"variables\":{\"id\":" + str(player_id) + "}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)
    
    try:
        df = pd.DataFrame(response.json()['data']['player'])
        return df.infer_objects()
    except:
        print(response.text)
        
def get_roster(url, key, game_id):
    ''' 
    Retrieves roster information of a game for a given game_id.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key
    game_id: an integer to select the game


    Returns
    ---------
    
    df: a dataframe containing the roster information
    
    '''
    payload = "{\"query\":\"query game ($id: ID!) {\\n    game (id: $id) {\\n        id\\n    rosters {\\n        player {\\n            id\\n            nickname\\n        }\\n        positionGroupType\\n        shirtNumber\\n        team {\\n            id\\n            name\\n        }\\n        started\\n    }\\n}\\n}\",\"variables\":{\"id\":" + str(game_id) + "}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)

    try:
        df = pd.DataFrame.from_dict(response.json()['data']['game']['rosters'])
        df['game_id'] = response.json()['data']['game']['id']
        df = df.reindex(sorted(df.columns), axis = 1)    
        return df.infer_objects()
    except:
        print(response.text)

def get_game_events(url, key, game_id):
    ''' 
    Retrieves all events of a game for a given game_id.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key
    game_id: an integer to select the game


    Returns
    ---------
    
    df: a dataframe containing the events
    
    '''
    payload = "{\"query\":\"query game ($id: ID!) {\\n    game (id: $id) {\\n        id\\n        gameEvents {\\n            id\\n            advantageType\\n            bodyType\\n            duration\\n            earlyDistribution\\n            endTime\\n            endType\\n            formattedGameClock\\n            gameClock\\n            gameEventType\\n            heightType\\n            initialTouchType\\n            insertedAt\\n            otherPlayer {\\n                id\\n                nickname\\n            }\\n            outType\\n            player {\\n                id\\n                nickname\\n            }\\n            playerOff {\\n                id\\n                nickname\\n            }\\n            playerOffType\\n            playerOn {\\n                id\\n                nickname\\n            }\\n            pressurePlayer {\\n                id\\n                nickname\\n            }\\n            pressureType\\n            scoreValue\\n            setpieceType\\n            startTime\\n            subType\\n            team {\\n                id\\n                name\\n            }\\n            touches\\n            touchesInBox\\n            updatedAt\\n            videoAngleType\\n            video {\\n                id\\n            }\\n            videoMissing\\n            videoUrl\\n            defenderLocations {\\n                eventModule\\n                name\\n                x\\n                y\\n            }\\n            offenderLocations {\\n                eventModule\\n                name\\n                x\\n                y\\n            }\\n            possessionEvents {\\n                duration\\n                endTime\\n                formattedGameClock\\n                gameClock\\n                id\\n                insertedAt\\n                possessionEventType\\n                startTime\\n                updatedAt\\n                videoUrl\\n                ballCarryEvent {\\n                    additionalChallenger1 {\\n                        id\\n                        nickname\\n                    }\\n                    additionalChallenger2 {\\n                        id\\n                        nickname\\n                    }\\n                    additionalChallenger3 {\\n                        id\\n                        nickname\\n                    }\\n                    advantageType\\n                    ballCarrierPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    ballCarryType\\n                    betterOptionPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    betterOptionTime\\n                    betterOptionType\\n                    carryType\\n                    createsSpace\\n                    defenderPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    id\\n                    insertedAt\\n                    ballCarryOutcome\\n                    linesBrokenType\\n                    opportunityType\\n                    pressurePlayer {\\n                        id\\n                        nickname\\n                    }\\n                    touchOutcomeType\\n                    touchType\\n                    updatedAt\\n                }\\n                challengeEvent {\\n                    additionalChallenger1 {\\n                        id\\n                        nickname\\n                    }\\n                    additionalChallenger2 {\\n                        id\\n                        nickname\\n                    }\\n                    additionalChallenger3 {\\n                        id\\n                        nickname\\n                    }\\n                    advantageType\\n                    ballCarrierPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    betterOptionPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    betterOptionTime\\n                    betterOptionType\\n                    challengeOutcomeType\\n                    challengeType\\n                    challengeWinnerPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    challengerHomePlayer {\\n                        id\\n                        nickname\\n                    }\\n                    challengerAwayPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    challengerPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    createsSpace\\n                    dribbleType\\n                    insertedAt\\n                    keeperPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    linesBrokenType\\n                    missedTouchPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    missedTouchType\\n                    opportunityType\\n                    pressurePlayer {\\n                        id\\n                        nickname\\n                    }\\n                    tackleAttemptType\\n                    trickType\\n                    updatedAt\\n                }\\n                clearanceEvent {\\n                    advantageType\\n                    ballHeightType\\n                    betterOptionPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    betterOptionTime\\n                    betterOptionType\\n                    blockerPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    clearanceBodyType\\n                    clearanceOutcomeType\\n                    clearancePlayer {\\n                        id\\n                        nickname\\n                    }\\n                    createsSpace\\n                    failedInterventionPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer1 {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer2 {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer3 {\\n                        id\\n                        nickname\\n                    }\\n                    insertedAt\\n                    missedTouchPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    missedTouchType\\n                    opportunityType\\n                    pressurePlayer {\\n                        id\\n                        nickname\\n                    }\\n                    pressureType\\n                    shotInitialHeightType\\n                    shotOutcomeType\\n                    updatedAt\\n                }\\n                crossEvent {\\n                    advantageType\\n                    ballHeightType\\n                    betterOptionPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    betterOptionTime\\n                    betterOptionType\\n                    blockerPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    clearerPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    completeToPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    createsSpace\\n                    crossHighPointType\\n                    crossOutcomeType\\n                    crossType\\n                    crossZoneType\\n                    crosserBodyType\\n                    crosserPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    defenderBallHeightType\\n                    defenderBodyType\\n                    defenderPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    deflectorBodyType\\n                    deflectorPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer1 {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer2 {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer3 {\\n                        id\\n                        nickname\\n                    }\\n                    incompletionReasonType\\n                    insertedAt\\n                    intendedTargetPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    keeperPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    missedTouchPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    missedTouchType\\n                    noLook\\n                    opportunityType\\n                    pressurePlayer {\\n                        id\\n                        nickname\\n                    }\\n                    pressureType\\n                    receiverBallHeightType\\n                    receiverBodyType\\n                    secondIncompletionReasonType\\n                    shotInitialHeightType\\n                    shotOutcomeType\\n                    updatedAt\\n                }\\n                passingEvent {\\n                    advantageType\\n                    ballHeightType\\n                    betterOptionPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    betterOptionTime\\n                    betterOptionType\\n                    blockerPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    createsSpace\\n                    defenderBodyType\\n                    defenderHeightType\\n                    defenderPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    deflectorBodyType\\n                    deflectorPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer1 {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer2 {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer3 {\\n                        id\\n                        nickname\\n                    }\\n                    incompletionReasonType\\n                    insertedAt\\n                    linesBrokenType\\n                    missedTouchPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    missedTouchType\\n                    noLook\\n                    opportunityType\\n                    passAccuracyType\\n                    passBodyType\\n                    passHighPointType\\n                    passOutcomeType\\n                    passType\\n                    passerPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    pressurePlayer {\\n                        id\\n                        nickname\\n                    }\\n                    pressureType\\n                    receiverBodyType\\n                    receiverFacingType\\n                    receiverHeightType\\n                    receiverPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    secondIncompletionReasonType\\n                    shotInitialHeightType\\n                    shotOutcomeType\\n                    targetFacingType\\n                    targetPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    updatedAt\\n                }\\n                reboundEvent {\\n                    advantageType\\n                    blockerPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    insertedAt\\n                    missedTouchPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    missedTouchType\\n                    originateType\\n                    reboundBodyType\\n                    reboundHeightType\\n                    reboundHighPointType\\n                    reboundOutcomeType\\n                    rebounderPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    shotInitialHeightType\\n                    shotOutcomeType\\n                    updatedAt\\n                }\\n                shootingEvent {\\n                    advantageType\\n                    badParry\\n                    ballHeightType\\n                    ballMoving\\n                    betterOptionPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    betterOptionTime\\n                    betterOptionType\\n                    blockerPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    bodyMovementType\\n                    clearerPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    createsSpace\\n                    deflectorBodyType\\n                    deflectorPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer1 {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer2 {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer3 {\\n                        id\\n                        nickname\\n                    }\\n                    insertedAt\\n                    keeperTouchType\\n                    missedTouchPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    missedTouchType\\n                    noLook\\n                    pressurePlayer {\\n                        id\\n                        nickname\\n                    }\\n                    pressureType\\n                    saveHeightType\\n                    saveReboundType\\n                    saveable\\n                    saverPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    shooterPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    shotBodyType\\n                    shotInitialHeightType\\n                    shotNatureType\\n                    shotOutcomeType\\n                    shotType\\n                    updatedAt\\n                }\\n                fouls {\\n                    badCall\\n                    correctDecision\\n                    culpritPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    foulOutcomeType\\n                    foulType\\n                    insertedAt\\n                    potentialOffenseType\\n                    sequence\\n                    updatedAt\\n                    var\\n                    varCulpritPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    varOutcomeType\\n                    varPotentialOffenseType\\n                    varReasonType\\n                    victimPlayer {\\n                        id\\n                        nickname\\n                    }\\n                }\\n                grades {\\n                    gradeLabel\\n                    gradeStyle\\n                    gradeType\\n                    insertedAt\\n                    playerGrade\\n                    player {\\n                        id\\n                        nickname\\n                    }\\n                    updatedAt\\n                }\\n            }\\n        }\\n    }\\n}\",\"variables\":{\"id\":" + str(game_id) + "}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)
    
    try:
        df = pd.DataFrame(response.json()['data']['game']['gameEvents'])
        df.insert(0, 'gameId', [game_id] * len(df))
        df = df.sort_values('startTime', ascending = True).reset_index(drop = True)
        return df.infer_objects()
    except:
        print(response.text)        

def get_game_event(url, key, game_event_id):    
    ''' 
    Retrieves event for a given game_event_id.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key
    game_event_id: an integer to select the event


    Returns
    ---------
    
    df: a dataframe containing the event
    
    '''    
    payload = "{\"query\":\"query gameEvent ($id: ID!) {\\n    gameEvent (id: $id) {\\n            id\\n        advantageType\\n        bodyType\\n        duration\\n        earlyDistribution\\n        endTime\\n        endType\\n        formattedGameClock\\n        gameClock\\n        gameEventType\\n        heightType\\n        initialTouchType\\n        insertedAt\\n        otherPlayer {\\n            id\\n            nickname\\n        }\\n        outType\\n        player {\\n            id\\n            nickname\\n        }\\n        playerOff {\\n            id\\n            nickname\\n        }\\n        playerOffType\\n        playerOn {\\n            id\\n            nickname\\n        }\\n        pressurePlayer {\\n            id\\n            nickname\\n        }\\n        pressureType\\n        scoreValue\\n        setpieceType\\n        startTime\\n        subType\\n        team {\\n            id\\n            name\\n        }\\n        touches\\n        touchesInBox\\n        updatedAt\\n        videoAngleType\\n        video {\\n            id\\n        }\\n        videoMissing\\n        videoUrl\\n        defenderLocations {\\n            eventModule\\n            name\\n            x\\n            y\\n        }\\n        offenderLocations {\\n            eventModule\\n            name\\n            x\\n            y\\n        }\\n        possessionEvents {\\n            duration\\n            endTime\\n            formattedGameClock\\n            gameClock\\n            id\\n            insertedAt\\n            possessionEventType\\n            startTime\\n            updatedAt\\n            videoUrl\\n            ballCarryEvent {\\n                additionalChallenger1 {\\n                    id\\n                    nickname\\n                }\\n                additionalChallenger2 {\\n                    id\\n                    nickname\\n                }\\n                additionalChallenger3 {\\n                    id\\n                    nickname\\n                }\\n                advantageType\\n                ballCarrierPlayer {\\n                    id\\n                    nickname\\n                }\\n                ballCarryType\\n                betterOptionPlayer {\\n                    id\\n                    nickname\\n                }\\n                betterOptionTime\\n                betterOptionType\\n                carryType\\n                createsSpace\\n                defenderPlayer {\\n                    id\\n                    nickname\\n                }\\n                id\\n                insertedAt\\n                ballCarryOutcome\\n                linesBrokenType\\n                opportunityType\\n                pressurePlayer {\\n                    id\\n                    nickname\\n                }\\n                touchOutcomeType\\n                touchType\\n                updatedAt\\n            }\\n            challengeEvent {\\n                additionalChallenger1 {\\n                    id\\n                    nickname\\n                }\\n                additionalChallenger2 {\\n                    id\\n                    nickname\\n                }\\n                additionalChallenger3 {\\n                    id\\n                    nickname\\n                }\\n                advantageType\\n                ballCarrierPlayer {\\n                    id\\n                    nickname\\n                }\\n                betterOptionPlayer {\\n                    id\\n                    nickname\\n                }\\n                betterOptionTime\\n                betterOptionType\\n                challengeOutcomeType\\n                challengeType\\n                challengeWinnerPlayer {\\n                    id\\n                    nickname\\n                }\\n                challengerHomePlayer {\\n                    id\\n                    nickname\\n                }\\n                challengerAwayPlayer {\\n                    id\\n                    nickname\\n                }\\n                challengerPlayer {\\n                    id\\n                    nickname\\n                }\\n                createsSpace\\n                dribbleType\\n                insertedAt\\n                keeperPlayer {\\n                    id\\n                    nickname\\n                }\\n                linesBrokenType\\n                missedTouchPlayer {\\n                    id\\n                    nickname\\n                }\\n                missedTouchType\\n                opportunityType\\n                pressurePlayer {\\n                    id\\n                    nickname\\n                }\\n                tackleAttemptType\\n                trickType\\n                updatedAt\\n            }\\n            clearanceEvent {\\n                advantageType\\n                ballHeightType\\n                betterOptionPlayer {\\n                    id\\n                    nickname\\n                }\\n                betterOptionTime\\n                betterOptionType\\n                blockerPlayer {\\n                    id\\n                    nickname\\n                }\\n                clearanceBodyType\\n                clearanceOutcomeType\\n                clearancePlayer {\\n                    id\\n                    nickname\\n                }\\n                createsSpace\\n                failedInterventionPlayer {\\n                    id\\n                    nickname\\n                }\\n                failedInterventionPlayer1 {\\n                    id\\n                    nickname\\n                }\\n                failedInterventionPlayer2 {\\n                    id\\n                    nickname\\n                }\\n                failedInterventionPlayer3 {\\n                    id\\n                    nickname\\n                }\\n                insertedAt\\n                missedTouchPlayer {\\n                    id\\n                    nickname\\n                }\\n                missedTouchType\\n                opportunityType\\n                pressurePlayer {\\n                    id\\n                    nickname\\n                }\\n                pressureType\\n                shotInitialHeightType\\n                shotOutcomeType\\n                updatedAt\\n            }\\n            crossEvent {\\n                advantageType\\n                ballHeightType\\n                betterOptionPlayer {\\n                    id\\n                    nickname\\n                }\\n                betterOptionTime\\n                betterOptionType\\n                blockerPlayer {\\n                    id\\n                    nickname\\n                }\\n                clearerPlayer {\\n                    id\\n                    nickname\\n                }\\n                completeToPlayer {\\n                    id\\n                    nickname\\n                }\\n                createsSpace\\n                crossHighPointType\\n                crossOutcomeType\\n                crossType\\n                crossZoneType\\n                crosserBodyType\\n                crosserPlayer {\\n                    id\\n                    nickname\\n                }\\n                defenderBallHeightType\\n                defenderBodyType\\n                defenderPlayer {\\n                    id\\n                    nickname\\n                }\\n                deflectorBodyType\\n                deflectorPlayer {\\n                    id\\n                    nickname\\n                }\\n                failedInterventionPlayer {\\n                    id\\n                    nickname\\n                }\\n                failedInterventionPlayer1 {\\n                    id\\n                    nickname\\n                }\\n                failedInterventionPlayer2 {\\n                    id\\n                    nickname\\n                }\\n                failedInterventionPlayer3 {\\n                    id\\n                    nickname\\n                }\\n                incompletionReasonType\\n                insertedAt\\n                intendedTargetPlayer {\\n                    id\\n                    nickname\\n                }\\n                keeperPlayer {\\n                    id\\n                    nickname\\n                }\\n                missedTouchPlayer {\\n                    id\\n                    nickname\\n                }\\n                missedTouchType\\n                noLook\\n                opportunityType\\n                pressurePlayer {\\n                    id\\n                    nickname\\n                }\\n                pressureType\\n                receiverBallHeightType\\n                receiverBodyType\\n                secondIncompletionReasonType\\n                shotInitialHeightType\\n                shotOutcomeType\\n                updatedAt\\n            }\\n            passingEvent {\\n                advantageType\\n                ballHeightType\\n                betterOptionPlayer {\\n                    id\\n                    nickname\\n                }\\n                betterOptionTime\\n                betterOptionType\\n                blockerPlayer {\\n                    id\\n                    nickname\\n                }\\n                createsSpace\\n                defenderBodyType\\n                defenderHeightType\\n                defenderPlayer {\\n                    id\\n                    nickname\\n                }\\n                deflectorBodyType\\n                deflectorPlayer {\\n                    id\\n                    nickname\\n                }\\n                failedInterventionPlayer {\\n                    id\\n                    nickname\\n                }\\n                failedInterventionPlayer1 {\\n                    id\\n                    nickname\\n                }\\n                failedInterventionPlayer2 {\\n                    id\\n                    nickname\\n                }\\n                failedInterventionPlayer3 {\\n                    id\\n                    nickname\\n                }\\n                incompletionReasonType\\n                insertedAt\\n                linesBrokenType\\n                missedTouchPlayer {\\n                    id\\n                    nickname\\n                }\\n                missedTouchType\\n                noLook\\n                opportunityType\\n                passAccuracyType\\n                passBodyType\\n                passHighPointType\\n                passOutcomeType\\n                passType\\n                passerPlayer {\\n                    id\\n                    nickname\\n                }\\n                pressurePlayer {\\n                    id\\n                    nickname\\n                }\\n                pressureType\\n                receiverBodyType\\n                receiverFacingType\\n                receiverHeightType\\n                receiverPlayer {\\n                    id\\n                    nickname\\n                }\\n                secondIncompletionReasonType\\n                shotInitialHeightType\\n                shotOutcomeType\\n                targetFacingType\\n                targetPlayer {\\n                    id\\n                    nickname\\n                }\\n                updatedAt\\n            }\\n            reboundEvent {\\n                advantageType\\n                blockerPlayer {\\n                    id\\n                    nickname\\n                }\\n                insertedAt\\n                missedTouchPlayer {\\n                    id\\n                    nickname\\n                }\\n                missedTouchType\\n                originateType\\n                reboundBodyType\\n                reboundHeightType\\n                reboundHighPointType\\n                reboundOutcomeType\\n                rebounderPlayer {\\n                    id\\n                    nickname\\n                }\\n                shotInitialHeightType\\n                shotOutcomeType\\n                updatedAt\\n            }\\n            shootingEvent {\\n                advantageType\\n                badParry\\n                ballHeightType\\n                ballMoving\\n                betterOptionPlayer {\\n                    id\\n                    nickname\\n                }\\n                betterOptionTime\\n                betterOptionType\\n                blockerPlayer {\\n                    id\\n                    nickname\\n                }\\n                bodyMovementType\\n                clearerPlayer {\\n                    id\\n                    nickname\\n                }\\n                createsSpace\\n                deflectorBodyType\\n                deflectorPlayer {\\n                    id\\n                    nickname\\n                }\\n                failedInterventionPlayer {\\n                    id\\n                    nickname\\n                }\\n                failedInterventionPlayer1 {\\n                    id\\n                    nickname\\n                }\\n                failedInterventionPlayer2 {\\n                    id\\n                    nickname\\n                }\\n                failedInterventionPlayer3 {\\n                    id\\n                    nickname\\n                }\\n                insertedAt\\n                keeperTouchType\\n                missedTouchPlayer {\\n                    id\\n                    nickname\\n                }\\n                missedTouchType\\n                noLook\\n                pressurePlayer {\\n                    id\\n                    nickname\\n                }\\n                pressureType\\n                saveHeightType\\n                saveReboundType\\n                saveable\\n                saverPlayer {\\n                    id\\n                    nickname\\n                }\\n                shooterPlayer {\\n                    id\\n                    nickname\\n                }\\n                shotBodyType\\n                shotInitialHeightType\\n                shotNatureType\\n                shotOutcomeType\\n                shotType\\n                updatedAt\\n            } \\n            fouls {\\n                badCall\\n                correctDecision\\n                culpritPlayer {\\n                    id\\n                    nickname\\n                }\\n                foulOutcomeType\\n                foulType\\n                insertedAt\\n                potentialOffenseType\\n                sequence\\n                updatedAt\\n                var\\n                varCulpritPlayer {\\n                    id\\n                    nickname\\n                }\\n                varOutcomeType\\n                varPotentialOffenseType\\n                varReasonType\\n                victimPlayer {\\n                    id\\n                    nickname\\n                }\\n            }\\n            grades {\\n                gradeLabel\\n                gradeStyle\\n                gradeType\\n                insertedAt\\n                playerGrade\\n                player {\\n                    id\\n                    nickname\\n                }\\n                updatedAt\\n            }\\n        }\\n    }\\n}\",\"variables\":{\"id\":" + str(game_event_id) + "}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)
    
    try:
        df = pd.DataFrame(response.json()['data']).T
        return df.infer_objects()
    except:
        print(response.text)
        
def get_game_events_games(url, key, games):
    ''' 
    Retrieves all events of games for a given list of games.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key
    games: a list of integers to select the games


    Returns
    ---------
    
    df: a dataframe containing the events
    
    '''
    df_list = []
    for game_id in tqdm.tqdm(games):
        payload = "{\"query\":\"query game ($id: ID!) {\\n    game (id: $id) {\\n        id\\n        gameEvents {\\n            id\\n            advantageType\\n            bodyType\\n            duration\\n            earlyDistribution\\n            endTime\\n            endType\\n            formattedGameClock\\n            gameClock\\n            gameEventType\\n            heightType\\n            initialTouchType\\n            insertedAt\\n            otherPlayer {\\n                id\\n                nickname\\n            }\\n            outType\\n            player {\\n                id\\n                nickname\\n            }\\n            playerOff {\\n                id\\n                nickname\\n            }\\n            playerOffType\\n            playerOn {\\n                id\\n                nickname\\n            }\\n            pressurePlayer {\\n                id\\n                nickname\\n            }\\n            pressureType\\n            scoreValue\\n            setpieceType\\n            startTime\\n            subType\\n            team {\\n                id\\n                name\\n            }\\n            touches\\n            touchesInBox\\n            updatedAt\\n            videoAngleType\\n            video {\\n                id\\n            }\\n            videoMissing\\n            videoUrl\\n            defenderLocations {\\n                eventModule\\n                name\\n                x\\n                y\\n            }\\n            offenderLocations {\\n                eventModule\\n                name\\n                x\\n                y\\n            }\\n            possessionEvents {\\n                duration\\n                endTime\\n                formattedGameClock\\n                gameClock\\n                id\\n                insertedAt\\n                possessionEventType\\n                startTime\\n                updatedAt\\n                videoUrl\\n                ballCarryEvent {\\n                    additionalChallenger1 {\\n                        id\\n                        nickname\\n                    }\\n                    additionalChallenger2 {\\n                        id\\n                        nickname\\n                    }\\n                    additionalChallenger3 {\\n                        id\\n                        nickname\\n                    }\\n                    advantageType\\n                    ballCarrierPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    ballCarryType\\n                    betterOptionPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    betterOptionTime\\n                    betterOptionType\\n                    carryType\\n                    createsSpace\\n                    defenderPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    id\\n                    insertedAt\\n                    ballCarryOutcome\\n                    linesBrokenType\\n                    opportunityType\\n                    pressurePlayer {\\n                        id\\n                        nickname\\n                    }\\n                    touchOutcomeType\\n                    touchType\\n                    updatedAt\\n                }\\n                challengeEvent {\\n                    additionalChallenger1 {\\n                        id\\n                        nickname\\n                    }\\n                    additionalChallenger2 {\\n                        id\\n                        nickname\\n                    }\\n                    additionalChallenger3 {\\n                        id\\n                        nickname\\n                    }\\n                    advantageType\\n                    ballCarrierPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    betterOptionPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    betterOptionTime\\n                    betterOptionType\\n                    challengeOutcomeType\\n                    challengeType\\n                    challengeWinnerPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    challengerHomePlayer {\\n                        id\\n                        nickname\\n                    }\\n                    challengerAwayPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    challengerPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    createsSpace\\n                    dribbleType\\n                    insertedAt\\n                    keeperPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    linesBrokenType\\n                    missedTouchPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    missedTouchType\\n                    opportunityType\\n                    pressurePlayer {\\n                        id\\n                        nickname\\n                    }\\n                    tackleAttemptType\\n                    trickType\\n                    updatedAt\\n                }\\n                clearanceEvent {\\n                    advantageType\\n                    ballHeightType\\n                    betterOptionPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    betterOptionTime\\n                    betterOptionType\\n                    blockerPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    clearanceBodyType\\n                    clearanceOutcomeType\\n                    clearancePlayer {\\n                        id\\n                        nickname\\n                    }\\n                    createsSpace\\n                    failedInterventionPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer1 {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer2 {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer3 {\\n                        id\\n                        nickname\\n                    }\\n                    insertedAt\\n                    missedTouchPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    missedTouchType\\n                    opportunityType\\n                    pressurePlayer {\\n                        id\\n                        nickname\\n                    }\\n                    pressureType\\n                    shotInitialHeightType\\n                    shotOutcomeType\\n                    updatedAt\\n                }\\n                crossEvent {\\n                    advantageType\\n                    ballHeightType\\n                    betterOptionPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    betterOptionTime\\n                    betterOptionType\\n                    blockerPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    clearerPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    completeToPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    createsSpace\\n                    crossHighPointType\\n                    crossOutcomeType\\n                    crossType\\n                    crossZoneType\\n                    crosserBodyType\\n                    crosserPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    defenderBallHeightType\\n                    defenderBodyType\\n                    defenderPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    deflectorBodyType\\n                    deflectorPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer1 {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer2 {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer3 {\\n                        id\\n                        nickname\\n                    }\\n                    incompletionReasonType\\n                    insertedAt\\n                    intendedTargetPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    keeperPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    missedTouchPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    missedTouchType\\n                    noLook\\n                    opportunityType\\n                    pressurePlayer {\\n                        id\\n                        nickname\\n                    }\\n                    pressureType\\n                    receiverBallHeightType\\n                    receiverBodyType\\n                    secondIncompletionReasonType\\n                    shotInitialHeightType\\n                    shotOutcomeType\\n                    updatedAt\\n                }\\n                passingEvent {\\n                    advantageType\\n                    ballHeightType\\n                    betterOptionPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    betterOptionTime\\n                    betterOptionType\\n                    blockerPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    createsSpace\\n                    defenderBodyType\\n                    defenderHeightType\\n                    defenderPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    deflectorBodyType\\n                    deflectorPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer1 {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer2 {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer3 {\\n                        id\\n                        nickname\\n                    }\\n                    incompletionReasonType\\n                    insertedAt\\n                    linesBrokenType\\n                    missedTouchPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    missedTouchType\\n                    noLook\\n                    opportunityType\\n                    passAccuracyType\\n                    passBodyType\\n                    passHighPointType\\n                    passOutcomeType\\n                    passType\\n                    passerPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    pressurePlayer {\\n                        id\\n                        nickname\\n                    }\\n                    pressureType\\n                    receiverBodyType\\n                    receiverFacingType\\n                    receiverHeightType\\n                    receiverPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    secondIncompletionReasonType\\n                    shotInitialHeightType\\n                    shotOutcomeType\\n                    targetFacingType\\n                    targetPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    updatedAt\\n                }\\n                reboundEvent {\\n                    advantageType\\n                    blockerPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    insertedAt\\n                    missedTouchPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    missedTouchType\\n                    originateType\\n                    reboundBodyType\\n                    reboundHeightType\\n                    reboundHighPointType\\n                    reboundOutcomeType\\n                    rebounderPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    shotInitialHeightType\\n                    shotOutcomeType\\n                    updatedAt\\n                }\\n                shootingEvent {\\n                    advantageType\\n                    badParry\\n                    ballHeightType\\n                    ballMoving\\n                    betterOptionPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    betterOptionTime\\n                    betterOptionType\\n                    blockerPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    bodyMovementType\\n                    clearerPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    createsSpace\\n                    deflectorBodyType\\n                    deflectorPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer1 {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer2 {\\n                        id\\n                        nickname\\n                    }\\n                    failedInterventionPlayer3 {\\n                        id\\n                        nickname\\n                    }\\n                    insertedAt\\n                    keeperTouchType\\n                    missedTouchPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    missedTouchType\\n                    noLook\\n                    pressurePlayer {\\n                        id\\n                        nickname\\n                    }\\n                    pressureType\\n                    saveHeightType\\n                    saveReboundType\\n                    saveable\\n                    saverPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    shooterPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    shotBodyType\\n                    shotInitialHeightType\\n                    shotNatureType\\n                    shotOutcomeType\\n                    shotType\\n                    updatedAt\\n                }\\n                fouls {\\n                    badCall\\n                    correctDecision\\n                    culpritPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    foulOutcomeType\\n                    foulType\\n                    insertedAt\\n                    potentialOffenseType\\n                    sequence\\n                    updatedAt\\n                    var\\n                    varCulpritPlayer {\\n                        id\\n                        nickname\\n                    }\\n                    varOutcomeType\\n                    varPotentialOffenseType\\n                    varReasonType\\n                    victimPlayer {\\n                        id\\n                        nickname\\n                    }\\n                }\\n                grades {\\n                    gradeLabel\\n                    gradeStyle\\n                    gradeType\\n                    insertedAt\\n                    playerGrade\\n                    player {\\n                        id\\n                        nickname\\n                    }\\n                    updatedAt\\n                }\\n            }\\n        }\\n    }\\n}\",\"variables\":{\"id\":" + str(game_id) + "}}"
        response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)
        
        try:
            df = pd.DataFrame(response.json()['data']['game']['gameEvents'])
            df.insert(0, 'gameId', [game_id] * len(df))
            df = df.sort_values('startTime', ascending = True).reset_index(drop = True)
            df_list.append(df)
        except:
            print('\nError in game: ' + str(game_id))
            print(response.text) 
    final_df = pd.concat(df_list, ignore_index = True)
    return final_df.infer_objects()

def get_scoring_events(url, key, competition_id, season):
    ''' 
    Retrieves all scoring events for a given competition and season.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key
    competition_id: an integer to select the competition
    season: a string to select the season


    Returns
    ---------
    
    df: a dataframe containing the scoring events
    
    '''    
    payload = "{\"query\":\"  query($competitionId: ID!, $season: String!) {\\n       scoringEvents(competitionId: $competitionId, season: $season) {\\n            id\\n           gameEventType\\n           gameId\\n            period\\n            startTime\\n            formattedGameClock\\n            outType\\n        }\\n    }\\n\",\"variables\":{\"competitionId\":" + str(competition_id) + ",\"season\":\"" + str(season) + "\"}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)
    
    try:
        df = pd.DataFrame.from_dict(response.json()['data']['scoringEvents'])
        df = df[df['gameEventType'] == 'OUT']
        df['gameId'] = df['gameId'].astype(int)
        
        df_pivot = df.groupby(['gameId','outType'])[['id']].count().reset_index(drop = False)
        df_pivot = df_pivot.pivot(index = 'gameId', columns = 'outType', values = 'id').fillna(0)
        df_pivot = df_pivot.rename(columns = {'A':'awayGoals','H':'homeGoals'}).reset_index(drop = False)
        
        return df.infer_objects(), df_pivot.infer_objects()
    except:
        print(response.text)
        
    