import pandas as pd

def parse_csv():
    # Read in the csv file
    df = pd.read_csv('btcusd-15m.csv')

    # Convert the Time column to datetime format
    df['Time'] = pd.to_datetime(df['Time'])

    # Check if there are any missing time points in the sequence
    time_diff = df['Time'].diff()
    fifteen_min_diff = pd.Timedelta(minutes=15)
    missing_times = df.iloc[1:].loc[time_diff != fifteen_min_diff, 'Time']

    if not missing_times.empty:
        print("You have missing data points")
        print(missing_times)

    return
