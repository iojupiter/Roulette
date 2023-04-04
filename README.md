# Roulette
A trading bot which uses a logistic regression to predict whether the next 15 minute BTC/USD candlestick will close red or green. As long as the candle is predicted to close green, open and hold a position.
This bot works accurately, however you need to be aware that Kraken takes a ~0.26% fee on the trade size for both the buy order and the sell order. This implies that 15 minute candlesticks closing green at least above 0.52% are profitable.

# How to run this script
1. Add your Kraken API key and Secret in sign.py, order.py and balance.py
2. The /Prod folder is a python virtual environment which you need to initialize with "source Prod/bin/activate"
3. In sync.py set the size of the USD position. It is the second parameter to for "trade_bot(900, 50)"
4. Run python3 sync.py
5. Outputs will be printed to predictions.txt, yield.csv and btcusd-15m.csv
6. Note, you need a consistent dataset of 15 minute btc/usd candlesticks. Obtain the latest ones using the Google Sheets CryptoFinance extension.


# How this script works
1. sync.py begins a True loop and syncs with the current minute.
2. Approx. 3 before the next 15 minute marks (i.e. 00, 15, 30, 45) sync.py will invoke decide().
3. decide() fetches the latest 15 minute btc/usd OHLC candlestick from the Kraken API, decodes and appends the data to the btcusd-15m.csv file.
4. A logistic regression is applied on the dataset by creating a target column. 5 Rolling averages columns of 4h, 8h, 16h, 20h respectively are created as parameters for the prediction.
The dataset is split into train/test with last 200 rows as test rows. Random Forest Classifier with 200 estimators is fit. Prediction accuracy is constrained with a 60% probability.
5. If the prediction returns 1, open a position of size in USD and block execution for 15 minutes.
6. sync.py holds position further as long as the prediction is 1. Closes the position otherwise.
7. The balance and profit is written to yield.csv
