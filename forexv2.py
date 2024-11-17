import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Función para obtener datos de precios
def obtener_datos(ticker_symbol, period, interval):
    ticker = yf.Ticker(ticker_symbol)
    asset_name = ticker.info.get("shortName", "Activo")
    
    # Descargar datos del activo con el periodo y intervalo especificado
    data = ticker.history(period=period, interval=interval)
    
    if data.empty:
        print(f"No se han encontrado datos para {ticker_symbol}.")
        return None, None
    
    # Filtrar saltos mayores a 1 día
    data = data[~data.index.to_series().diff().dt.days.gt(1)]
    data['Date'] = data.index.strftime('%d-%m-%Y %H:%M:%S')  # Convertir índices a string
    
    # Identificar los saltos entre días
    data['Delta'] = data.index.to_series().diff().dt.days.fillna(0)
    weekend_jumps = data[data['Delta'] > 1].index  # Fechas con saltos
    
    # Mostrar estadísticas solo si el intervalo es de 1 minuto
    if interval == "1m":
        print(f"Estadísticas del precio de {asset_name}:")
        print(f"- Último precio: {data['Close'].iloc[-1]:.2f} USD")
        print(f"- Última fecha y hora del dato: {data.index[-1]}")
        print(f"- Precio medio: {data['Close'].mean():.2f} USD")
        print(f"- Desviación estándar: {data['Close'].std():.2f} USD")
        print(f"- Precio mínimo: {data['Close'].min():.2f} USD")
        print(f"- Precio máximo: {data['Close'].max():.2f} USD")
    
    return data, asset_name, weekend_jumps

# Función para mostrar la gráfica
def mostrar_grafica(ticker_symbol, data, weekend_jumps):
    if data is None:
        return go.Figure()

    # Crear figura para la gráfica de precios históricos
    fig = go.Figure()
    
    # Crear gráfico de velas con los precios históricos
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
            x0=jump.strftime('%d-%m-%Y %H:%M:%S'),
            x1=jump.strftime('%d-%m-%Y %H:%M:%S'),
            y0=data['Low'].min(),
            y1=data['High'].max(),
            line=dict(color="red", width=2, dash="dot"),
            xref='x',
            yref='y'
        )
    
    # Ajustar el diseño para omitir los huecos de tiempo
    fig.update_xaxes(type='category')
    
    # Configuración del diseño
    fig.update_layout(
        title=f"Precio Histórico de {ticker_symbol}",
        xaxis_title='Fecha',
        yaxis_title='Precio',
        height=900,
        width=1600,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        xaxis=dict(
            tickformat='%d-%m-%Y %H:%M:%S',
            tickmode='auto',
            nticks=20  # Ajustar la cantidad de etiquetas según sea necesario
        )
    )
    
    return fig

# Función para guardar ambas gráficas en un solo archivo HTML
def guardar_graficas_html(html_filename, fig1, fig2):
    # Guardamos la primera gráfica en el archivo HTML
    with open(html_filename, 'w') as f:
        f.write(fig1.to_html(full_html=True, include_plotlyjs="cdn"))
    
    # Añadimos la segunda gráfica
    with open(html_filename, 'a') as f:
        f.write(fig2.to_html(full_html=False, include_plotlyjs="cdn"))
    
    print(f"Las gráficas han sido guardadas en {html_filename}")

# Crear un archivo HTML para guardar el gráfico
html_filename = "grafico_precios_historicos.html"

# Obtener los datos históricos (intervalo de 1 minuto para el último día)
data_1min, asset_name, weekend_jumps_1min = obtener_datos("MXN=X", "1d", "1m")

# Crear la primera gráfica (precio histórico 1 minuto)
fig1 = mostrar_grafica("MXN=X", data_1min, weekend_jumps_1min)

# Obtener los datos históricos (intervalo de 15 minutos para el último mes)
data_15min, asset_name, weekend_jumps_15min = obtener_datos("MXN=X", "1mo", "15m")

# Crear la segunda gráfica (precio histórico 15 minutos)
fig2 = mostrar_grafica("MXN=X", data_15min, weekend_jumps_15min)

# Guardar ambas gráficas en el mismo archivo HTML
guardar_graficas_html(html_filename, fig1, fig2)
