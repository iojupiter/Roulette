# Roulette
A trading bot which uses a Random Forest Classifier to predict whether the next 15 minute BTC/USD candlestick will close red or green. As long as the candle is predicted to close green, open and hold a position, exit at the end of the 15 minute candle.
Despite trading fees, the probability of the next candlstick being red or green is 50%, a coin toss. These are already pretty good odds. Market information increases the odds in a favour which picking by prediction the next correct green candle and holding it as a position until completion making a good strategy.
This bot works accurately, however you need to be aware that Kraken takes a ~0.26% fee on the trade size for both the buy order and the sell order. This implies that 15 minute candlesticks closing green at least above 0.52% are profitable.


![Dashboard](https://github.com/iojupiter/Roulette/blob/main/Screenshot%202023-04-04%20at%2021.04.13.png?raw=true)

# How to run this script
1. Add your Kraken API key and Secret in sign.py, order.py and balance.py respectively.
2. The /Prod folder is a python virtual environment which you need to initialize with "source Prod/bin/activate". You can also create your own venv to import the necessary python dependencies.
3. Sync.py is the main script. In sync.py set the size of the USD position. It is the second parameter to for the function `trade_bot(900, 50)` at the end of the file. In this case, $50 will put placed.
4. Run `python3 sync.py`
5. Outputs will be appended to predictions.txt, yield.csv and btcusd-15m.csv. You can open different bash shells and use `tail -f predictions.txt`to watch the output.
6. Note, you need a consistent dataset of 15 minute btc/usd candlesticks for accurate predictions. Obtain the latest ones using the Google Sheets [CryptoFinance](https://cryptowat.ch/cryptofinance) extension.


# How this script works
1. sync.py begins a true loop and syncs with the current minute.
2. Approx. 3 seconds after the next 15 minute marks (i.e. 00, 15, 30, 45) sync.py will invoke `decide()`.
3. `decide()` fetches the latest 15 minute btc/usd OHLC candlestick from the Kraken API, decodes and appends the data to the btcusd-15m.csv file.
4. A random forest classifier is fit on the dataset by creating a target column. Five rolling averages columns of 4h, 8h, 16h, 20h respectively are created as new features for the prediction.
The dataset is split into train/test with last 200 rows as test rows. The classifier has 200 estimators. Prediction accuracy is constrained with a 60% probability.
5. If the prediction returns 1, a new spot buy order is sent to the Kraken API and the script blocks for 15 minutes.
6. sync.py holds position for a further 15 minutes as long as the prediction is 1. Closes the position otherwise.
7. The balance and profit is written to yield.csv
