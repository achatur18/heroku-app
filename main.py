import yfinance as yf
import datetime as dt
from supertrend import Supertrend
from signals import signal_given_st_indicator
from fastapi import FastAPI

app = FastAPI()


tickers=['BTC-USD']

@app.get("/")
async def root():
    start='2021-01-01'
    end=dt.datetime.now()
    signal = {}
    for ticker in tickers:
        ohlc_data=None
        try:
            ohlc_data = yf.download(ticker,start,end,interval='1d')
        except:
            continue
        st=Supertrend(ohlc_data)
        signal[ticker] = signal_given_st_indicator(st)

    return signal

@app.post("/add_tickers")
async def root(new_tickers):
    global tickers
    
    tickers.append(new_tickers)

    tickers=list(set(tickers))
    
    return tickers

@app.post("/remove_tickers")
async def root(new_tickers):
    global tickers

    tickers=[x for x in tickers if x!=new_tickers]

    tickers=list(set(tickers))
    
    return tickers