#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 12:56:36 2022

@author: apschram
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
import humps
import sys
import os

current_path = os.path.dirname(os.path.realpath(__file__))  
sys.path.append(os.path.dirname(current_path))

from pypff import pff

def shooter_grade(url,key,game_event_id):
    ## RETRIEVE GAME EVENT
    df = pff.get_game_event(url, key, game_event_id)
    
    ## UNPACK & MERGE POSSESSION EVENT
    df = df.merge(df['possessionEvents'].apply(pd.Series)[0].apply(pd.Series), how = 'inner', left_index = True, right_index = True, suffixes = ('_gameEvent','_possessionEvent'))
    
    ## UNPACK & MERGE SHOOTING EVENT
    df = df.merge(df['shootingEvent'].apply(pd.Series), how = 'inner', left_index = True, right_index = True, suffixes = ('','_shootingEvent'))
    
    ## UNPACK & MERGE SHOOTER GRADES
    grades = df['possessionEvents'].apply(pd.Series)[0].apply(pd.Series).dropna(how = 'all', axis = 1)
    grades = grades['grades'].apply(pd.Series)
    
    ## RETRIEVE SHOOTER GRADES
    shooter_grades = pd.DataFrame(columns = ['gradeLabel','playerGrade'])
    for col in list(grades.columns):
        temp = grades[col].apply(pd.Series)
        temp = temp[temp['gradeLabel'].isin(['Shooter'])]
        
        ## APPEND SHOOTER GRADES
        shooter_grades = shooter_grades.append(temp[['gradeLabel','playerGrade']], ignore_index = False)
    
    df = df.merge(shooter_grades, how = 'inner', left_index = True, right_index = True)
    
    ## CONSTRUCT ADVANTAGE COLUMN FROM GAME EVENT & SHOOTING EVENT
    df['advantage'] = np.where(df['advantageType'] == 'N', 1, 0)
    df['advantage'] = np.where(df['advantageType_shootingEvent'] == 'N', 1, df['advantage'])
    df = df.drop(columns = ['advantageType','advantageType_shootingEvent'])
    
    ## MAKE SURE TOUCHES ARE NOT EMPTY AND INTEGER
    df['touches'] = df['touches'].astype(int)
    df['touches_in_box'] = df['touchesInBox'].fillna(0)
    df['touches_in_box'] = df['touches_in_box'].astype(int)
    
    ## CREATE DUMMIES FOR ONE TOUCH SHOTS, IN BOX AND ONE TOUCH IN BOX
    df['one_touch'] = np.where(df['touches'] == 1, 1, 0)
    df['in_box'] = np.where(df['touches_in_box'] > 0, 1, 0)
    
    ## CONVERT BOOLEAN COLUMN TO DUMMY
    df['creates_space'] = np.where(df['createsSpace'] == True, 1, 0)
    
    ## CONSTRUCT DUMMY IF BETTER OPTION IS AVAILABLE
    df['better_option'] = np.where(df['betterOptionType'].isnull(), 0, 1)
    
    ## CONSTRUCT DUMMY IF THERE IS A MISSED TOUCH
    df['missed_touch'] = np.where(df['missedTouchType'].isnull(), 0, 1)
    
    ## CONSTRUCT DUMMY IF THERE IS A FAILED INTERVENTION
    df['failed_intervention'] = np.where(df['failedInterventionPlayer'].isnull(), 0, 1)
    
    ## GROUP OTHER BODY PARTS THAN HE, RF, LF INTO O (OTHER)
    df['shotBodyType'] = np.where(df['shotBodyType'].isin(['R','L']), df['shotBodyType'] + 'F', df['shotBodyType'])
    df['shotBodyType'] = np.where(df['shotBodyType'].isin(['HE','RF','LF']), df['shotBodyType'], 'O')
    
    ## SHOT NATURE TYPE L (LACES) SHOULD BE P (POWER)
    df['shotNatureType'] = np.where(df['shotNatureType'] == 'L', 'P', df['shotNatureType'])
    
    ## CONSTRUCT DUMMY VARIABLES FOR CATEGORICAL COLUMNS
    categorical = ['ballHeightType','bodyMovementType','setpieceType','shotBodyType','shotNatureType','shotType']
    categorical = pd.get_dummies(data = df[categorical])
    categorical.columns = [humps.decamelize(x) for x in categorical.columns]
    categorical.columns = [x[:x.find('__')] + x[x.find('__'):].upper() for x in categorical.columns]
    categorical.columns = categorical.columns.str.replace('__','_')
    df = df.merge(categorical, how = 'inner', left_index = True, right_index = True)
    
    ## USE RESULTS OF THE LINEAR REGRESSION TO PREDICT EXPECTED GRADE
    ls = sm.load(current_path + '/shooting' + '_grade_model.pickle')
    variables = pd.read_pickle(current_path + '/shooting' + '_grade_variables.pickle')
    
    ## SET VARIABLES THAT ARE MISSING TO 0
    for variable in variables:
        if variable not in list(df.columns):
            df[variable] = 0     
    
    ## SET INDEPENDENT VARIABLES
    X = df[variables]
    X = X.assign(Intercept = 1)
    X = X.dropna(how = 'any')
    
    ## PREDICT EXPECTED GRADE FOR EACH SHOT
    df['expectedGrade'] = ls.predict(X)
    
    ## CALCULATE ADJUSTED GRADE FOR EACH SHOT
    df['adjustedGrade'] = df['playerGrade'] - df['expectedGrade']
    
    return df