import yfinance as yf
import pandas as pd

# Función para mostrar la barra de progreso
def barra_progreso(actual, total, longitud=30):
    porcentaje = actual / total
    bloques_llenos = int(longitud * porcentaje)
    barra = "[" + "#" * bloques_llenos + "-" * (longitud - bloques_llenos) + "]"
    print(f"\r{barra} {porcentaje:.0%} completado", end="")

# Leer los tickers desde el archivo
df = pd.read_csv("alfa1/A2.txt")
tickers = df["0"].to_list()

# Función para verificar si un ticker es activo
def is_ticker_active(ticker):
    try:
        data = yf.download(ticker, period="1d", progress=False)  # Descargar datos del último día
        if data.empty:
            return False
        return True
    except Exception:
        return False
    
# Lista para almacenar los tickers inactivos
inactive_tickers = []

# Verificar cada ticker con barra de progreso
total_tickers = len(tickers)
for index, ticker in enumerate(tickers, start=1):
    if not is_ticker_active(ticker):
        inactive_tickers.append(ticker)
    barra_progreso(index, total_tickers)  # Actualizar barra de progreso

# Exportar los tickers inactivos a un archivo .txt
output_file = "inactive_tickers_V1.txt"
with open(output_file, "w") as file:
    for ticker in inactive_tickers:
        file.write(ticker + "\n")

print(f"\nLos siguientes tickers están inactivos y se exportaron a '{output_file}':")
print(inactive_tickers)
