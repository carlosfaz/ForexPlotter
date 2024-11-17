import yfinance as yf
import plotly.graph_objects as go

def obtener_datos(ticker_symbol, period, interval):
    """Obtiene los datos históricos de un ticker con el periodo e intervalo especificados."""
    ticker = yf.Ticker(ticker_symbol)
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

    return data, weekend_jumps

def mostrar_estadisticas(data):
    """Muestra estadísticas si el intervalo es de 1 minuto."""
    print(f"Estadísticas del precio:")
    print(f"- Último precio: {data['Close'].iloc[-1]:.2f} USD")
    print(f"- Última fecha y hora del dato: {data.index[-1]}")
    print(f"- Precio medio: {data['Close'].mean():.2f} USD")
    print(f"- Desviación estándar: {data['Close'].std():.2f} USD")
    print(f"- Precio mínimo: {data['Close'].min():.2f} USD")
    print(f"- Precio máximo: {data['Close'].max():.2f} USD")

def crear_grafica(data, weekend_jumps):
    """Crea una gráfica de velas con los datos y añade las líneas de saltos."""
    fig = go.Figure()

    # Crear gráfico de velas
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

    # Añadir líneas rojas para los saltos de fin de semana
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
    fig.update_layout(
        title="Precio Histórico",
        xaxis_title='Fecha',
        yaxis_title='Precio',
        height=900,
        width=1600,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        xaxis=dict(tickformat='%d-%m-%Y %H:%M:%S', tickmode='auto', nticks=20)
    )

    return fig

def guardar_graficas_html(html_filename, *figs):
    """Guarda varias gráficas en un archivo HTML de forma eficiente."""
    with open(html_filename, 'w') as f:
        # Guardar las gráficas
        f.write(figs[0].to_html(full_html=True, include_plotlyjs="cdn"))
        for fig in figs[1:]:
            f.write(fig.to_html(full_html=False, include_plotlyjs="cdn"))
    print(f"Las gráficas han sido guardadas en {html_filename}")

# Parámetros de entrada
html_filename = "grafico_precios_historicos.html"

tickers = ["MXN=X"]

# Más combinaciones de periodos e intervalos para agregar más gráficas
periodos = [
    ("1d", "1m"),      # Un día, intervalos de 1 minuto
    ("1mo", "15m"),    # Un mes, intervalos de 15 minutos
    ("3mo", "1h"),     # Tres meses, intervalos de 1 hora
    ("6mo", "1h"),     # Seis meses, intervalos de 1 hora
    ("1y", "1d")     # Un año, intervalos de 1 día
]
# Obtener datos y gráficas para cada par de periodo/intervalo
figs = []
for periodo, intervalo in periodos:
    data, weekend_jumps = obtener_datos(tickers[0], periodo, intervalo)
    if data is not None:
        # Mostrar estadísticas solo si el intervalo es de 1 minuto
        if intervalo == "1m":
            mostrar_estadisticas(data)
        
        fig = crear_grafica(data, weekend_jumps)
        figs.append(fig)

# Guardar todas las gráficas juntas en un solo archivo HTML
guardar_graficas_html(html_filename, *figs)
