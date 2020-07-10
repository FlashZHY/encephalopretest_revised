# Encephalo Investments Coding Pre-Test - Revised April 2020

import pandas as pd
import numpy as np
import math
import warnings

warnings.filterwarnings('ignore')


def cleanse_data(df):
    # Your task here is to remove data from any ticker that isn't XXY, sort chronologically and return a dataframe
    # whose only column is 'Adj Close'

    # select the stock
    df = df.loc[df.Ticker == "XXY"]
    # change the type of date for sorting
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(by="Date")
    df = df[["Adj Close"]]
    dfclean = df
    return dfclean


def mc_sim(sims, days, df):
    # The code for a crude monte carlo simulation is given below. Your job is to extract the mean expected price
    # on the last day, as well as the 95% confidence interval.
    # Note that the z-score for a 95% confidence interval is 1.960
    returns = df.pct_change()
    last_price = df.iloc[-1]

    simulation_df = pd.DataFrame()

    for x in range(sims):
        count = 0
        daily_vol = returns.std()

        price_series = []

        price = last_price * (1 + np.random.normal(0, daily_vol))
        price_series.append(price)

        for y in range(days):
            price = price_series[count] * (1 + np.random.normal(0, daily_vol))
            price_series.append(price)
            count += 1

        simulation_df[x] = price_series

    # FILL OUT THE REST OF THE CODE. The above code has given you 'sims' of simulations run 'days' days into the future.
    # Your task is to return the expected price on the last day +/- the 95% confidence interval.

    # Select the last row of the simulations, namely the 1000 different outcome of the last day
    lastday_outcome = simulation_df.iloc[-1]
    # Compute the mean and std of the outcome
    mean = lastday_outcome.mean()
    std = lastday_outcome.std()
    # Use confidence interval formula to compute the upper and lower limit
    upper_limit = mean + 1.96 * std / math.sqrt(sims)
    lower_limit = mean - 1.96 * std / math.sqrt(sims)
    Half_interval = 1.96 * std / math.sqrt(sims)
    CI = [lower_limit, upper_limit]

    return mean, Half_interval, CI


def main():
    filename = '20192020histdata.csv'
    rawdata = pd.read_csv(filename)
    cleansed = cleanse_data(rawdata)
    simnum = 3000  # change this number to one that you deem appropriate
    days = 25
    mc_sim(simnum, days, cleansed)
    print("Expected price, half of the interval and 95% confidence interval are:", '\n', mc_sim(simnum, days, cleansed))
    # return


if __name__ == '__main__':
    main()
