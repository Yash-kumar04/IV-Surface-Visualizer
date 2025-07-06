import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

def get_option_chain(ticker):
    stock = yf.Ticker(ticker)
    expiries = stock.options[:4]  # Limit to 4 expirations for speed
    data = []
    for exp in expiries:
        opt = stock.option_chain(exp)
        for df, opt_type in zip([opt.calls, opt.puts], ["call", "put"]):
            temp = df[['strike', 'impliedVolatility']].copy()
            temp['expiry'] = exp
            temp['type'] = opt_type
            data.append(temp)
    return pd.concat(data)

def prepare_surface(df, opt_type="call"):
    df = df[df['type'] == opt_type]
    df['expiry_days'] = df['expiry'].apply(lambda x: (datetime.strptime(x, "%Y-%m-%d") - datetime.now()).days)
    pivot = df.pivot_table(index='strike', columns='expiry_days', values='impliedVolatility')
    return pivot

def plot_surface(pivot, ticker):
    X, Y = np.meshgrid(pivot.columns, pivot.index)
    Z = pivot.values
    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
    fig.update_layout(title=f"{ticker} Implied Volatility Surface",
                      scene=dict(xaxis_title='Days to Expiry',
                                 yaxis_title='Strike Price',
                                 zaxis_title='Implied Volatility'),
                      autosize=True)
    fig.write_html("plots/iv_surface.html")
    fig.show()

def main():
    ticker = "AAPL"
    print(f"Fetching option chain for {ticker}...")
    df = get_option_chain(ticker)
    df.dropna(inplace=True)
    pivot = prepare_surface(df, opt_type="call")
    print("Plotting IV surface...")
    plot_surface(pivot, ticker)

if __name__ == "__main__":
    main()
