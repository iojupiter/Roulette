import time
import strategy
import ohlc
import predict
import csv
import balance

def decide():
    x = ohlc.get_OHLC()
    y = predict.predict()
    with open("predictions.txt", "a") as file:
        file.write(time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time())) + " : " + str(y) + "\n")
    decision = False
    if y == 1:
        decision = True

    return decision

def trade_bot(candle_interval, trade_size):
    while True:
        current_minute = int(time.time() / 60)
        wait_time = 60 - (time.time() - current_minute * 60)
        wait_time = max(0, wait_time)
        time.sleep(wait_time)
        if abs(time.time() % candle_interval) <= 3:
            if decide():
                strategy.open(trade_size)
                print("Holding for 15 minutes...")
                time.sleep(candle_interval)
                while decide():
                    print("Holding for another 15 minutes...")
                    time.sleep(candle_interval)
                strategy.close()
                try:
                    total = balance.get_balance("ZUSD")
                    yield_time = time.strftime('%Y-%m-%d %H:%M', time.gmtime(time.time()))
                    with open('yield.csv', mode='a', newline='') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow([yield_time, total])
                except:
                    print("Error while fetching balance")
                    continue


trade_bot(900, 50)
