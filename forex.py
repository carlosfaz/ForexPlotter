import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from scipy.stats import norm
import math
import time
import warnings

warnings.filterwarnings("ignore")

# Definición de los modelos estocásticos
def heston_model(S0, T, r, sigma, v0, kappa, theta, rho, num_steps):
    dt = T / num_steps
    prices = np.zeros(num_steps + 1)
    prices[0] = S0
    v = np.zeros(num_steps + 1)
    v[0] = v0
    for i in range(num_steps):
        z1 = np.random.normal(0, 1)
        z2 = rho * z1 + math.sqrt(1 - rho**2) * np.random.normal(0, 1)
        v[i + 1] = v[i] + kappa * (theta - v[i]) * dt + sigma * np.sqrt(v[i] * dt) * z1
        prices[i + 1] = prices[i] * np.exp((r - 0.5 * v[i]) * dt + np.sqrt(v[i] * dt) * z2)
    return prices

def black_scholes_model(S0, T, r, sigma, num_steps):
    dt = T / num_steps
    prices = np.zeros(num_steps + 1)
    prices[0] = S0
    for i in range(num_steps):
        z = np.random.normal(0, 1)
        prices[i + 1] = prices[i] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)
    return prices

def geometric_brownian_motion(S0, T, r, sigma, num_steps):
    dt = T / num_steps
    prices = np.zeros(num_steps + 1)
    prices[0] = S0
    for i in range(num_steps):
        z = np.random.normal(0, 1)
        prices[i + 1] = prices[i] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)
    return prices

# Función para pronosticar precios
def pronosticar_precio(ticker_symbol):
    # Crear objeto de Ticker y obtener el nombre del activo
    ticker = yf.Ticker(ticker_symbol)
    asset_name = ticker.info.get("shortName", "Activo")
    
    # Descargar datos del activo en intervalos de 1 minuto para los últimos 5 días
    data = ticker.history(period="5d", interval="15m")
    
    # Verificar si se obtuvieron datos
    if data.empty:
        print(f"No se han encontrado datos para la última semana de {ticker_symbol}.")
        return None, None, None
    
    # Calcular media (mu) y volatilidad (sigma)
    log_returns = np.log(data['Close'] / data['Close'].shift(1)).dropna()
    mu = log_returns.mean() * len(data)
    sigma = log_returns.std() * np.sqrt(len(data))

    # Parámetros comunes
    num_steps = 24 * 60  # 24 horas en intervalos de 1 minuto
    S0 = data['Close'].iloc[-1]
    T = 1 / 24  # 1 día
    r = 0.01  # Tasa de interés libre de riesgo
    v0 = sigma**2  # Volatilidad inicial
    kappa = 1.0  # Velocidad de reversión
    theta = sigma**2  # Nivel de equilibrio
    rho = 0.1  # Correlación

    # Pronósticos
    prices_heston = heston_model(S0, T, r, sigma, v0, kappa, theta, rho, num_steps)
    prices_bs = black_scholes_model(S0, T, r, sigma, num_steps)
    prices_gbm = geometric_brownian_motion(S0, T, r, sigma, num_steps)

    return data, prices_heston, prices_bs, prices_gbm, asset_name

# Función especial para agregar los pronósticos a la gráfica
def agregar_pronosticos_a_grafica(fig, future_times, prices_dict):
    colors = {
        'Heston': 'green',
        'Black-Scholes': 'blue',
        'GBM': 'purple',
        'Vasicek': 'orange',
        'CIR': 'red'
    }
    for model, prices in prices_dict.items():
        fig.add_trace(go.Scatter(
            x=future_times, 
            y=prices, 
            mode='lines', 
            name=f'Predicción de Precios {model}', 
            line=dict(color=colors[model], width=2, dash='dash')
        ))

# Función para mostrar la gráfica combinada
def mostrar_grafica(ticker_symbol, data, prices_dict, html_filename):
    if data is None or not prices_dict:
        return
    
    # Crear figura para la simulación de precios
    future_times = pd.date_range(data.index[-1], periods=len(next(iter(prices_dict.values()))), freq='T')
    
    fig = go.Figure()
    
    # Añadir candlesticks para el precio histórico
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Precio Histórico'
    ))

    # Agregar los pronósticos a la gráfica
    agregar_pronosticos_a_grafica(fig, future_times, prices_dict)

    # Añadir línea horizontal con el último precio
    last_price = data['Close'].iloc[-1]
    fig.add_trace(go.Scatter(
        x=[data.index[0], future_times[-1]], 
        y=[last_price, last_price], 
        mode='lines', 
        name='Último Precio', 
        line=dict(color='black', width=1, dash='dot')
    ))
    
    fig.update_layout(
        title=f"Precio Histórico y Simulación de {ticker_symbol}",
        height=900,
        width=1600,
        showlegend=True,
        xaxis_title='Fecha',
        yaxis_title='Precio',
        xaxis_rangeslider_visible=False
    )
    
    # Guardar la figura en un archivo HTML
    fig.write_html(html_filename)
    print(f"La gráfica de predicción ha sido guardada en {html_filename}")

# Crear un archivo HTML para guardar la predicción de precios
html_filename = "prediccion_precios.html"

# Pronosticar precios
data, prices_heston, prices_bs, prices_gbm, asset_name = pronosticar_precio("MXN=X")

# Crear un diccionario con los precios pronosticados
prices_dict = {
    'Heston': prices_heston,
    'Black-Scholes': prices_bs,
    'GBM': prices_gbm
}

# Mostrar gráfica
mostrar_grafica("MXN=X", data, prices_dict, html_filename)
