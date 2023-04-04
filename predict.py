import pandas as pd
import numpy as np
import requests
import time
import datetime
import json
import csv
from sklearn.ensemble import RandomForestClassifier
import verify_data


def predict():
    # Load the data
    verify_data.parse_csv()
    data = pd.read_csv('/Users/jupiter/Desktop/Roulette/Models/LogisticRegression/Prod/btcusd-15m.csv')

    del data['Exchange']
    del data['Base']
    del data['Quote']

    data['Next Candlestick'] = data['Close'].shift(-1)
    #data['Target'] = (data['Next Candlestick'] > data['Close']).astype(int)
    data['Target'] = ((data['Next Candlestick'] - data['Close']) / data['Close'] > 0.0052).astype(int)

    horizons = [4,8,12,16,20] #2h, 4h, 3h, 4h, 5h
    predictors = []
    for horizon in horizons:
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        rolling_averages = data[numeric_columns].rolling(horizon).mean()
        ratio_column = f"Close_Ratio_{horizon}"
        data[ratio_column] = data["Close"] / rolling_averages["Close"]
        trend_column = f"Trend_{horizon}"
        data[trend_column] = data["Target"].shift(1).rolling(horizon).sum()
        predictors += [ratio_column, trend_column]
    # Create a new DataFrame with the predictor columns
    predictor_df = data[predictors]
    # Concatenate the original data and the predictors DataFrames
    data = pd.concat([data, predictor_df], axis=1)
    # Drop any rows that contain NaN values in any column except "Next Candlestick"
    data = data.dropna(subset=data.columns[data.columns != "Next Candlestick"])

    train = data.iloc[:-200]
    test = data.iloc[-200:]
    model = RandomForestClassifier(n_estimators=200, min_samples_split=50, random_state=1)
    model.fit(train[predictors], train["Target"])
    last_candlestick = data.tail(1)[predictors]
    next_candlestick_direction = model.predict_proba(last_candlestick)[:,1]
    next_candlestick_direction[next_candlestick_direction >= .6] = 1
    next_candlestick_direction[next_candlestick_direction < .6] = 0
    return int(next_candlestick_direction[0])
