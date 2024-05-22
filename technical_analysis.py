import pandas as pd
import apimoex
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import ta

def plt_rsi(df, company_name):
    plt.plot(df.index, df['RSI'], color='black', linewidth=1.5)
    plt.grid(True)    
    plt.axhspan(30, 70, color='blue', alpha=0.2)
    plt.axhline(70, color='red', linestyle='--', linewidth=3)
    plt.axhline(30, color='green', linestyle='--', linewidth=3)
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B')) 
    plt.title(f"RSI, {company_name}")
    plt.show()

def plt_sma_ema(df, company_name):
    plt.plot(df.index, df['CLOSE'], color='black', linewidth=1.2, alpha=0.4)
    plt.plot(df.index, df['SMA'], color='red', linewidth=1.5)
    plt.plot(df.index, df['EMA'], color='blue', linewidth=1.5)
    plt.grid(True)    
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B')) 
    plt.title(f"SMA(red), EMA(blue), {company_name}")
    plt.show()

def plt_volume(df, company_name):    
    plt.plot(df.index, df['VPT'], color='blue', linewidth=1.5)
    plt.grid(True)    
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B')) 
    plt.title(f'Объемно-ценовой тренд (VPT) для {company_name}')
    plt.show()

with requests.Session() as session:
    data = apimoex.get_board_history(session, start='2024-01-01', board='TQBR', security='GAZP')
    df = pd.DataFrame(data)
    df['TRADEDATE'] = pd.to_datetime(df['TRADEDATE'])
    df.set_index('TRADEDATE', inplace=True)
    df['RSI'] = ta.momentum.rsi(df['CLOSE'])
    df['SMA'] = ta.trend.sma_indicator(df['CLOSE'])
    df['EMA'] = ta.trend.ema_indicator(df['CLOSE'])
    df['VPT'] = ta.volume.volume_price_trend(df['CLOSE'], df['VOLUME'])
    