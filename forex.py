import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# Modelos de predicción

# 1. Levy Process (Levy Flight) - Proceso de Levy
def levy_process(S0, T, r, sigma, alpha, num_steps):
    dt = T / num_steps
    prices = np.zeros(num_steps + 1)
    prices[0] = S0
    for i in range(num_steps):
        dz = np.random.standard_t(df=alpha)  # Distribución de Lévy
        prices[i + 1] = prices[i] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * dz)
    return prices

# 2. Brownian Motion with Drift - Movimiento Browniano con deriva
def brownian_motion_with_drift(S0, T, r, sigma, num_steps):
    dt = T / num_steps
    prices = np.zeros(num_steps + 1)
    prices[0] = S0
    for i in range(num_steps):
        dz = np.random.normal(0, 1)
        prices[i + 1] = prices[i] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * dz)
    return prices

# 3. Stable Paretian Process (α-stable) - Proceso Pareto Estable
def stable_paretian_process(S0, T, r, sigma, alpha, num_steps):
    dt = T / num_steps
    prices = np.zeros(num_steps + 1)
    prices[0] = S0
    for i in range(num_steps):
        dz = np.random.standard_t(df=alpha)  # Distribución estable
        prices[i + 1] = prices[i] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * dz)
    return prices

# 4. Wald Process - Proceso de Wald
def wald_process(S0, T, r, sigma, num_steps):
    dt = T / num_steps
    prices = np.zeros(num_steps + 1)
    prices[0] = S0
    for i in range(num_steps):
        dz = np.random.normal(0, 1)  # Distribución normal
        prices[i + 1] = prices[i] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * dz)
    return prices

# 5. Cox Process - Proceso de Cox
def cox_process(S0, T, r, sigma, kappa, theta, num_steps):
    dt = T / num_steps
    prices = np.zeros(num_steps + 1)
    prices[0] = S0
    for i in range(num_steps):
        dz = np.random.normal(0, 1)
        dz_jump = np.random.normal(0, kappa)  # Estabilidad de la media
        prices[i + 1] = prices[i] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * dz + theta * dz_jump)
    return prices

# 6. Random Walk Process - Proceso de Caminata Aleatoria
def random_walk_process(S0, T, r, sigma, num_steps):
    dt = T / num_steps
    prices = np.zeros(num_steps + 1)
    prices[0] = S0
    for i in range(num_steps):
        dz = np.random.choice([-1, 1])  # Movimiento aleatorio
        prices[i + 1] = prices[i] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * dz)
    return prices

# Función para pronosticar precios
def pronosticar_precio(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    asset_name = ticker.info.get("shortName", "Activo")
    
    # Descargar datos del activo en intervalos de 1 minuto para los últimos 5 días
    data = ticker.history(period="5d", interval="15m")
    
    if data.empty:
        print(f"No se han encontrado datos para la última semana de {ticker_symbol}.")
        return None, None, None, None, None
    
    log_returns = np.log(data['Close'] / data['Close'].shift(1)).dropna()
    mu = log_returns.mean() * len(data)
    sigma = log_returns.std() * np.sqrt(len(data))

    # Parámetros comunes
    num_steps = 100  # Número de pasos en la simulación
    S0 = data['Close'].iloc[-1]  # Precio inicial
    T = 1 / 24  # 1 día
    r = 0.01  # Tasa de interés libre de riesgo
    kappa = 0.2  # Parámetro para el proceso de Cox
    theta = 0.1  # Parámetro para el proceso de Cox
    
    # Pronósticos con los modelos seleccionados
    prices_levy = levy_process(S0, T, r, sigma, 1.5, num_steps)
    prices_brownian = brownian_motion_with_drift(S0, T, r, sigma, num_steps)
    prices_stable = stable_paretian_process(S0, T, r, sigma, 1.5, num_steps)
    prices_wald = wald_process(S0, T, r, sigma, num_steps)
    prices_cox = cox_process(S0, T, r, sigma, kappa, theta, num_steps)
    prices_random_walk = random_walk_process(S0, T, r, sigma, num_steps)

    return data, prices_levy, prices_brownian, prices_stable, prices_wald, prices_cox, prices_random_walk, asset_name

# Función para agregar los pronósticos a la gráfica
def agregar_pronosticos_a_grafica(fig, future_times, prices_dict):
    model_colors = {
        'Levy': '#FF0000',  # Rojo
        'Brownian': '#00FF00',  # Verde
        'Stable': '#0000FF',  # Azul
        'Wald': '#FF00FF',  # Magenta
        'Cox': '#FF6600',  # Naranja
        'Random Walk': '#000000'  # Negro
    }

    for model, prices in prices_dict.items():
        fig.add_trace(go.Scatter(x=future_times, y=prices, mode='lines', name=model, line=dict(color=model_colors.get(model, '#000000'))))

# Función para mostrar la gráfica combinada
def mostrar_grafica(ticker_symbol, data, prices_dict, html_filename):
    if data is None or not prices_dict:
        return
    
    # Crear figura para la simulación de precios
    future_times = pd.date_range(data.index[-1], periods=len(next(iter(prices_dict.values()))), freq='40T')
    
    fig = go.Figure()
    
    # Añadir candlesticks para el precio histórico
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Precio Histórico',
        increasing_line_color='green',  # Color para el precio creciente
        decreasing_line_color='red'  # Color para el precio decreciente
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
html_filename = "prediccion_precios_MXN_X.html"

# Pronosticar precios
data, prices_levy, prices_brownian, prices_stable, prices_wald, prices_cox, prices_random_walk, asset_name = pronosticar_precio("MXN=X")

# Crear un diccionario con los precios pronosticados
prices_dict = {
    'Levy': prices_levy,
    'Brownian': prices_brownian,
    'Stable': prices_stable,
    'Wald': prices_wald,
    'Cox': prices_cox,
    'Random Walk': prices_random_walk
}

# Mostrar gráfica
mostrar_grafica("MXN=X", data, prices_dict, html_filename)
