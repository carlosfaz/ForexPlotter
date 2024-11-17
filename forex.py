import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from scipy.stats import norm
import math
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

# Modelo CIR (Cox-Ingersoll-Ross)
def cir_model(S0, T, r, sigma, kappa, theta, num_steps):
    dt = T / num_steps
    prices = np.zeros(num_steps + 1)
    prices[0] = S0
    v = np.zeros(num_steps + 1)
    v[0] = sigma**2
    for i in range(num_steps):
        dz = np.random.normal(0, 1)
        v[i + 1] = v[i] + kappa * (theta - v[i]) * dt + np.sqrt(v[i] * dt) * dz
        v[i + 1] = max(v[i + 1], 0)  # Evitar que la volatilidad se vuelva negativa
        prices[i + 1] = prices[i] * np.exp((r - 0.5 * v[i]) * dt + np.sqrt(v[i] * dt) * dz)
    return prices

# Modelo Vasicek (para tasas de interés)
def vasicek_model(S0, T, r, sigma, kappa, theta, num_steps):
    dt = T / num_steps
    prices = np.zeros(num_steps + 1)
    prices[0] = S0
    v = np.zeros(num_steps + 1)
    v[0] = r
    for i in range(num_steps):
        dz = np.random.normal(0, 1)
        v[i + 1] = v[i] + kappa * (theta - v[i]) * dt + sigma * np.sqrt(dt) * dz
        prices[i + 1] = prices[i] * np.exp((v[i] - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * dz)
    return prices

def calcular_probabilidades(models, S0, T, r, sigma, v0, kappa, theta, rho, num_steps, num_iterations=1000):
    resultados = {modelo: [] for modelo in models.keys()}
    probabilidades = {}

    for modelo, func in models.items():
        for _ in range(num_iterations):
            if modelo == "Heston":
                prices = func(S0, T, r, sigma, v0, kappa, theta, rho, num_steps)
            elif modelo == "CIR" or modelo == "Vasicek":
                prices = func(S0, T, r, sigma, kappa, theta, num_steps)
            else:
                prices = func(S0, T, r, sigma, num_steps)
            resultados[modelo].append(prices[-1])
        
        # Calcular probabilidades
        precios_finales = np.array(resultados[modelo])
        probabilidad_subida = np.mean(precios_finales > S0)
        probabilidad_bajada = np.mean(precios_finales < S0)
        probabilidades[modelo] = (probabilidad_subida, probabilidad_bajada)
    
    return probabilidades


# Función para pronosticar precios
def pronosticar_precio(ticker_symbol):
    # Crear objeto de Ticker y obtener el nombre del activo
    ticker = yf.Ticker(ticker_symbol)
    asset_name = ticker.info.get("shortName", "Activo")
    
    # Descargar datos del activo en intervalos de 1 minuto para los últimos 5 días
    data = ticker.history(period="1mo", interval="15m")
    
    # Verificar si se obtuvieron datos
    if data.empty:
        print(f"No se han encontrado datos para la última semana de {ticker_symbol}.")
        return None, None, None
    
    # Obtener la fecha y hora del último dato
    last_datetime = data.index[-1]
    # Calcular estadísticas
    mean_price = data['Close'].mean()
    std_dev_price = data['Close'].std()
    min_price = data['Close'].min()
    max_price = data['Close'].max()
    price_range = max_price - min_price
    median_price = data['Close'].median()
    coef_var = (std_dev_price / mean_price) * 100  # Porcentaje
    last_price = data['Close'].iloc[-1]
    q1_price = data['Close'].quantile(0.25)
    q3_price = data['Close'].quantile(0.75)
    iqr_price = q3_price - q1_price
    skewness = data['Close'].skew()
    kurtosis = data['Close'].kurtosis()
    
    # Mostrar estadísticas
    print(f"Estadísticas del precio de {asset_name} esta semana:")
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

    # Calcular media (mu) y volatilidad (sigma)
    log_returns = np.log(data['Close'] / data['Close'].shift(1)).dropna()
    mu = log_returns.mean() * len(data)
    sigma = log_returns.std() * np.sqrt(len(data))

    # Parámetros comunes
    num_steps = 120  # Número de pasos en la simulación
    S0 = data['Close'].iloc[-1]  # Precio inicial
    T = 1 / 24  # 1 día
    r = 0.01  # Tasa de interés libre de riesgo
    v0 = sigma**2  # Volatilidad inicial
    kappa = 1.0  # Velocidad de reversión
    theta = sigma**2  # Nivel de equilibrio
    rho = 0.1  # Correlación

    # Pronósticos con los modelos seleccionados
    prices_heston = heston_model(S0, T, r, sigma, v0, kappa, theta, rho, num_steps)
    prices_bs = black_scholes_model(S0, T, r, sigma, num_steps)
    prices_gbm = geometric_brownian_motion(S0, T, r, sigma, num_steps)
    prices_cir = cir_model(S0, T, r, sigma, kappa, theta, num_steps)
    prices_vasicek = vasicek_model(S0, T, r, sigma, kappa, theta, num_steps)

    # Calcular probabilidades
    probabilidades = calcular_probabilidades({
        'Heston': heston_model,
        'Black-Scholes': black_scholes_model,
        'GBM': geometric_brownian_motion,
        'CIR': cir_model,
        'Vasicek': vasicek_model
    }, S0, T, r, sigma, v0, kappa, theta, rho, num_steps, num_iterations=1000)
    
    # Preparar datos de probabilidades para impresión
    header = ["Modelo", "Prob de Subida", "Prob de Bajada"]
    rows = []
    
    for modelo, (prob_subida, prob_bajada) in probabilidades.items():
        rows.append([modelo, f"{prob_subida:.2%}", f"{prob_bajada:.2%}"])
    
    # Calcular el ancho máximo para cada columna
    col_widths = [
        max(len(header[0]), max(len(row[0]) for row in rows)),
        max(len(header[1]), max(len(row[1]) for row in rows)),
        max(len(header[2]), max(len(row[2]) for row in rows))
    ]
    
    # Función para crear líneas divisorias
    def print_divider(widths):
        print("+" + "+".join("-" * (w + 2) for w in widths) + "+")
    
    # Imprimir encabezado
    print_divider(col_widths)
    print(f"| {header[0]:<{col_widths[0]}} | {header[1]:<{col_widths[1]}} | {header[2]:<{col_widths[2]}} |")
    print_divider(col_widths)
    
    # Imprimir cada fila de probabilidades
    for row in rows:
        print(f"| {row[0]:<{col_widths[0]}} | {row[1]:<{col_widths[1]}} | {row[2]:<{col_widths[2]}} |")
    
    # Línea final
    print_divider(col_widths)
    return data, prices_heston, prices_bs, prices_gbm, prices_cir, prices_vasicek, asset_name

# Función especial para agregar los pronósticos a la gráfica con candlesticks
def agregar_pronosticos_a_grafica(fig, future_times, prices_dict):
    # Colores personalizados para cada modelo
    model_colors = {
        'Heston': '#00FF00',  # Verde
        'Black-Scholes': '#0000FF',  # Azul
        'GBM': '#800080',  # Morado
        'CIR': '#FF4500',  # Naranja
        'Vasicek': '#FFD700',  # Dorado
    }

    for model, prices in prices_dict.items():
        # Crear candlesticks para los pronósticos con colores específicos
        up_color = model_colors[model]  # Color para los precios crecientes
        down_color = model_colors[model]  # Color para los precios decrecientes
        fig.add_trace(go.Candlestick(
            x=future_times, 
            open=prices[:-1], 
            high=np.maximum(prices[:-1], prices[1:]), 
            low=np.minimum(prices[:-1], prices[1:]), 
            close=prices[1:], 
            name=f'Predicción de Precios {model}',
            increasing_line_color=up_color, 
            decreasing_line_color=down_color
        ))

# Función para mostrar la gráfica combinada
# Función para mostrar la gráfica combinada
def mostrar_grafica(ticker_symbol, data, prices_dict, html_filename):
    if data is None or not prices_dict:
        return
    
    # Crear figura para la simulación de precios
    future_times = pd.date_range(data.index[-1], periods=len(next(iter(prices_dict.values()))), freq='40T')
    
    fig = go.Figure()
    
    data = data[~data.index.to_series().diff().dt.days.gt(1)]  # Filtrar saltos mayores a 1 día
    data['Date'] = data.index.strftime('%Y-%m-%d %H:%M:%S')  # Convertir índices a string
    
    # Identificar los saltos entre días
    data['Delta'] = data.index.to_series().diff().dt.days.fillna(0)
    weekend_jumps = data[data['Delta'] > 1].index  # Fechas con saltos

    
    fig.add_trace(go.Candlestick(
        x=data['Date'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Precio Histórico',
        increasing_line_color='green',
        decreasing_line_color='red'
    ))
    
    # Añadir líneas rojas para saltos de fin de semana
    for jump in weekend_jumps:
        fig.add_shape(
            type="line",
            x0=jump.strftime('%Y-%m-%d %H:%M:%S'),
            x1=jump.strftime('%Y-%m-%d %H:%M:%S'),
            y0=data['Low'].min(),
            y1=data['High'].max(),
            line=dict(color="red", width=2, dash="dot"),
            xref='x',
            yref='y'
        )
    
    # Ajustar ejes con menos etiquetas y rotación
    fig.update_layout(
        title="Gráfico de Velas con Líneas de Fin de Semana",
        xaxis=dict(
            type="category", 
            title="Fecha y Hora",
            tickangle=-45,  # Rotar las etiquetas
            tickmode='auto',
            nticks=20  # Ajustar la cantidad de etiquetas
        ),
        yaxis=dict(title="Precio")  
    )
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
#esta es la version esatalbe 
# Crear un archivo HTML para guardar la predicción de precios
html_filename = "prediccion_precios2.html"

# Pronosticar precios
data, prices_heston, prices_bs, prices_gbm, prices_cir, prices_vasicek, asset_name = pronosticar_precio("MXN=X")

# Crear un diccionario con los precios pronosticados
prices_dict = {
    'Heston': prices_heston,
    'Black-Scholes': prices_bs,
    'GBM': prices_gbm,
    'CIR': prices_cir,
    'Vasicek': prices_vasicek
}

# Mostrar gráfica
mostrar_grafica("MXN=X", data, prices_dict, html_filename)
    