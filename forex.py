import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from scipy.stats import norm
import math
import time

import warnings
warnings.filterwarnings("ignore")

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

def pronosticar_precio(ticker_symbol, html_filename):
    while True:
        # Crear objeto de Ticker y obtener el nombre del activo
        ticker = yf.Ticker(ticker_symbol)
        asset_name = ticker.info.get("shortName", "Activo")
        
        # Descargar datos del activo en intervalos de 1 minuto para los últimos 5 días
        data = ticker.history(period="5d", interval="15m")
        
        # Verificar si se obtuvieron datos
        if data.empty:
            print(f"No se han encontrado datos para la última semana de {ticker_symbol}.")
            return
        
        # Calcular media (mu) y volatilidad (sigma)
        log_returns = np.log(data['Close'] / data['Close'].shift(1)).dropna()
        mu = log_returns.mean() * len(data)
        sigma = log_returns.std() * np.sqrt(len(data))

        # Simular precios para las próximas 24 horas con el modelo de Heston
        num_steps = 24 * 60  # 24 horas en intervalos de 1 minuto
        S0 = data['Close'].iloc[-1]
        T = 1 / 24  # 1 día
        r = 0.01  # Tasa de interés libre de riesgo
        v0 = sigma**2  # Volatilidad inicial
        kappa = 1.0  # Velocidad de reversión
        theta = sigma**2  # Nivel de equilibrio
        rho = 0.1  # Correlación
        prices_heston = heston_model(S0, T, r, sigma, v0, kappa, theta, rho, num_steps)

        
        # Crear figura para la simulación de precios
        future_times = pd.date_range(data.index[-1], periods=num_steps, freq='T')
        
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
        
        # Añadir línea para la predicción de precios Heston
        fig.add_trace(go.Scatter(
            x=future_times, 
            y=prices_heston, 
            mode='lines', 
            name='Predicción de Precios Heston', 
            line=dict(color='green', width=2, dash='dash')
        ))
        
        # Añadir línea horizontal con el último precio
        last_price = data['Close'].iloc[-1]
        fig.add_trace(go.Scatter(
            x=[data.index[0], future_times[-1]], 
            y=[last_price, last_price], 
            mode='lines', 
            name='Último Precio', 
            line=dict(color='red', width=1, dash='dot')
        ))
        
        fig.update_layout(
            title=f"Precio Histórico y Simulación",
            height=900,
            width=1600,
            showlegend=True,
            xaxis_title='Fecha',
            yaxis_title='Precio',
            xaxis_rangeslider_visible=False
        )
        
        # Mostrar la figura
        fig.show()

       
        # Guardar la figura en un archivo HTML
        fig.write_html(html_filename)
        print(f"La gráfica de predicción ha sido guardada en {html_filename}")
        print("\n" * 10)

        # Calcular y mostrar estadísticas
        mean_price = data['Close'].mean()
        std_dev_price = data['Close'].std()
        min_price = data['Close'].min()
        max_price = data['Close'].max()
        price_range = max_price - min_price
        median_price = data['Close'].median()
        coef_var = (std_dev_price / mean_price) * 100
        q1_price = data['Close'].quantile(0.25)
        q3_price = data['Close'].quantile(0.75)
        iqr_price = q3_price - q1_price
        skewness = data['Close'].skew()
        kurtosis = data['Close'].kurtosis()
        last_datetime = data.index[-1]

        print(f"Estadísticas del precio de {asset_name} estas 24 hrs :")
        print(f"- Último precio: {last_price:.2f} USD")
        print(f"- Última fecha y hora del dato: {last_datetime}")
        print(f"- Precio medio: {mean_price:.2f} USD")
        print(f"- Desviación estándar: {std_dev_price:.2f} USD")
        print(f"- Precio mínimo: {min_price:.2f} USD")
        print(f"- Precio máximo: {max_price:.2f} USD")
        print(f"- Rango de precios: {price_range:.2f} USD")
        print(f"- Mediana: {median_price:.2f} USD")
        print(f"- Coeficiente de variación: {coef_var:.2f}%")
        print(f"- Primer cuartil (Q1): {q1_price:.2f} USD")
        print(f"- Tercer cuartil (Q3): {q3_price:.2f} USD")
        print(f"- Rango intercuartílico (IQR): {iqr_price:.2f} USD")
        print(f"- Asimetría: {skewness:.2f}")
        print(f"- Curtosis: {kurtosis:.2f}")
        
        # Calcular probabilidades de subida/bajada
        probabilidad_subida_heston = np.mean(prices_heston > last_price)
        probabilidad_bajada_heston = 1 - probabilidad_subida_heston

        # Bootstrap
        bootstrap_samples = 1000
        bootstrap_returns = np.random.choice(log_returns, size=(num_steps, bootstrap_samples), replace=True)
        bootstrap_prices = S0 * np.exp(np.cumsum(bootstrap_returns, axis=0))
        probabilidad_subida_bootstrap = np.mean(bootstrap_prices[-1, :] > last_price)
        probabilidad_bajada_bootstrap = 1 - probabilidad_subida_bootstrap

        # Modelo de Black-Scholes
        d1 = (np.log(last_price / S0) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        probabilidad_subida_black_scholes = norm.cdf(d1)
        probabilidad_bajada_black_scholes = 1 - probabilidad_subida_black_scholes
        print("\n")
        print(f"Probabilidad de que el precio suba en las próximas 24 horas:")
        print(f"- Modelo de Heston: {probabilidad_subida_heston:.2%}")
        print(f"- Bootstrap: {probabilidad_subida_bootstrap:.2%}")
        print(f"- Modelo de Black-Scholes: {probabilidad_subida_black_scholes:.2%}")

        # Esperar 5 segundos antes de la siguiente actualización
        time.sleep(5)

# Crear un archivo HTML para guardar la predicción de precios
html_filename = "prediccion_precios_heston.html"
pronosticar_precio("MXN=X", html_filename)
