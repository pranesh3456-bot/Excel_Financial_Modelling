import pandas as pd
import xlwings as xl
import yfinance as yf
from datetime import date, timedelta

# current share price 

wb = xl.Book("DMart_Financial_Model.xlsx")
valuations = wb.sheets['DCF Valuation']

Dmart_market_data = yf.download("DMART.NS", 
                                start = '2020-09-05', 
                                end = date.today() + timedelta(days=1))

Nifty_50_market_data = yf.download('^NSEI', 
                                    start = '2020-09-05', 
                                    end = date.today() + timedelta(days=1))

DMart = Dmart_market_data.sort_index(ascending=False)
Nifty_index = Nifty_50_market_data.sort_index(ascending=False)

raw_market_data = pd.DataFrame({
                            'DMart': DMart['Close']['DMART.NS'],
                            'Nifty_50': Nifty_index['Close']['^NSEI']
                            })

market_data = raw_market_data.sort_index(ascending=False)

valuations['C40'].value = market_data.iloc[0,0]

# CAGR value calcuation

years = (market_data.index[0] - market_data.index[-1]).days / 365.25

cagr = ((market_data['Nifty_50'].iloc[0] / market_data['Nifty_50'].iloc[-1]) ** (1/years) - 1)

valuations['C36'].value = cagr 

# Beta calculation

market_data['DMart_return'] = market_data['DMart'].pct_change()
market_data['Nifty_50_return'] = market_data['Nifty_50'].pct_change()

beta =  market_data['DMart_return'].cov(market_data['Nifty_50_return']) / market_data['Nifty_50_return'].var()

valuations['C35'].value = beta
