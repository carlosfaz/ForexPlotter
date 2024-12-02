import pandas as pd
import yfinance as yf

# URL de la página de Wikipedia que contiene la lista de los componentes del S&P 500
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

# Leer la tabla de la página web
tables = pd.read_html(url)

# La tabla que contiene los tickers se encuentra generalmente en la primera
df = tables[0]

# Extraer solo los tickers de la columna 'Symbol'
tickers = df['Symbol'].tolist()

# Check if a ticker is active
def is_ticker_active(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            print(f"Warning: {ticker} has no data within the given date range.")
            return False
        return True
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return False

# Fecha de ejemplo (puedes ajustarlo según necesites)
start_date = '2020-01-01'
end_date = '2024-12-31'

# Verificar cada ticker si está activo
for ticker in tickers:
    if is_ticker_active(ticker, start_date, end_date):
        print(f"{ticker} is active.")
    else:
        print(f"{ticker} is not active.")
