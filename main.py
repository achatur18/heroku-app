import yfinance as yf
import datetime as dt
import uvicorn
from supertrend import Supertrend
from signals import signal_given_st_indicator
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

tickers=['BTC-USD', 'ETH-USD', "TTM", "CDSL.NS", "SBICARD.NS", "RELAXO.NS", "JUBLFOOD.NS", "TATACONSUM.NS", "ASIANPAINT.NS", \
    "BAJAJHCARE.NS", "RELIANCE.NS", "IRCTC.NS", "TITAN.NS", "TRIDENT.NS", "TCS.BO", "ASTRAL.NS", "WIPRO.NS", "TATAMOTORS.NS", \
        "BALKRISIND.NS", "ROUTE.NS", "POLYCAB.NS", "LTI.NS", "BAJAJ-AUTO.NS", "DMART.NS", "ZOMATO.NS", "LALPATHLAB.NS", "URJA.NS", \
            "TATAELXSI.NS", "ALKYLAMINE.NS", "TATASTEEL.NS", "HDFC.NS", "BAJFINANCE.NS", "MUTHOOTFIN.NS", "ZENTEC.NS", "PRINCEPIPE.NS",\
                 "AFFLE.NS", "NAZARA.NS", "IRCON.NS", "HDFCBANK.NS", "DEEPAKNTR.NS", "KEI.NS", "HINDUNILVR.NS", "NAZARA.NS", "MINDTREE.NS",\
                    "FCL.NS", "RENUKA.NS", "PVR.NS", "INOXLEISUR.NS", "ICICIBANK.NS", "KOTAKBANK.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS",\
                         "ICICIPRULI.NS", "INFY.NS", "MARICO.NS", "HAPPSTMNDS.NS", "BATAINDIA.NS", "COLPAL.NS", "PIDILITIND.NS",\
                            "RELAXO.NS", "CEATLTD.NS", "HCLTECH.NS", "AAPL", "NVDA", "AMZN", "GOOG", "TSLA", "META"]
cache3={}
cache5={}
cache7={}

def get_signal(ticker):
    start='2021-01-01'
    end=dt.datetime.now()
    ohlc_data=None
    try:
        ohlc_data = yf.download(ticker,start,end,interval='1d')
    except:
        return None
    st=Supertrend(ohlc_data)
    return signal_given_st_indicator(st)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    global cache3
    global cache5
    global cache7
    start='2021-01-01'
    t=end=dt.datetime.now()
    key = str(t.year)+str(t.month)+str(t.day)
    if key not in cache3.keys():
        signal3 = {}
        signal5 = {}
        signal7 = {}
        for ticker in tickers:
            ohlc_data=None
            try:
                ohlc_data = yf.download(ticker,start,end,interval='1d')
            except:
                continue
            st3=Supertrend(ohlc_data, atr_period=10, multiplier=3.0)
            st5=Supertrend(ohlc_data, atr_period=10, multiplier=5.0)
            st7=Supertrend(ohlc_data, atr_period=10, multiplier=7.0)
            signal3[ticker] = signal_given_st_indicator(st3)
            signal5[ticker] = signal_given_st_indicator(st5)
            signal7[ticker] = signal_given_st_indicator(st7)
        cache3={}
        cache5={}
        cache7={}
        cache3[key]=signal3
        cache5[key]=signal5
        cache7[key]=signal7
    return templates.TemplateResponse("item.html", {"request": request, \
        "signals3": dict(sorted(cache3[key].items(), key=lambda item: (item[1]['signal'], item[1]['count']))),\
        "signals5": dict(sorted(cache5[key].items(), key=lambda item: (item[1]['signal'], item[1]['count']))),\
        "signals7": dict(sorted(cache7[key].items(), key=lambda item: (item[1]['signal'], item[1]['count']))),\
            })

@app.post("/show_tickers")
async def root(new_tickers):
    global tickers
    
    tickers.append(new_tickers)

    tickers=list(set(tickers))
    
    return get_signal(new_tickers)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)