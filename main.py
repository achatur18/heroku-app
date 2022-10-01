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
                            "RELAXO.NS", "CEATLTD.NS", "HCLTECH.NS"]
cache={}

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
    global cache
    start='2021-01-01'
    t=end=dt.datetime.now()
    key = str(t.year)+str(t.month)+str(t.day)+str(t.hour)
    if key not in cache.keys():
        signal = {}
        for ticker in tickers:
            ohlc_data=None
            try:
                ohlc_data = yf.download(ticker,start,end,interval='1d')
            except:
                continue
            st=Supertrend(ohlc_data)
            signal[ticker] = signal_given_st_indicator(st)
        cache={}
        cache[key]=signal
    return templates.TemplateResponse("item.html", {"request": request, "signals": dict(sorted(cache[key].items(), key=lambda item: (item[1]['signal'], item[1]['count'])))})

@app.post("/show_tickers")
async def root(new_tickers):
    global tickers
    
    tickers.append(new_tickers)

    tickers=list(set(tickers))
    
    return get_signal(new_tickers)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)