import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

def crear_figura_medias_moviles(data, asset_name):
    # Crear la figura de medias móviles
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name=asset_name, line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_5'], mode='lines', name='Media Móvil 5 minutos', line=dict(color='red', width=2)))
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], mode='lines', name='Media Móvil 20 minutos', line=dict(color='green', width=2)))
    fig.add_hline(y=data['Close'].iloc[-1], line=dict(color='orange', dash='dash'), annotation_text='Último Precio')
    
    fig.update_layout(title=f"Medias Móviles del Precio de {asset_name} esta semana", height=900, width=1600, showlegend=True)
    return fig

def crear_figura_histograma(data, asset_name, mean_price, median_price):
    # Crear la figura del histograma de precios
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=data['Close'], nbinsx=20, name='Precios', marker_color='lightblue'))
    fig.add_vline(x=mean_price, line=dict(color='red', dash='dash'), annotation_text='Media')
    fig.add_vline(x=median_price, line=dict(color='green', dash='dash'), annotation_text='Mediana')
    
    fig.update_layout(title=f"Histograma del Precio de {asset_name} esta semana", height=900, width=1600, showlegend=True)
    return fig

def analizar_activo(ticker_symbol, html_filename):
    # Crear objeto de Ticker y obtener el nombre del activo
    ticker = yf.Ticker(ticker_symbol)
    asset_name = ticker.info.get("shortName", "Activo")
    
    # Descargar datos del activo en intervalos de 1 minuto para los últimos 5 días
    data = ticker.history(period="5d", interval="1m")
    
    # Verificar si se obtuvieron datos
    if data.empty:
        print(f"No se han encontrado datos para la última semana de {ticker_symbol}.")
        return
    
    # Calcular estadísticas
    mean_price = data['Close'].mean()
    median_price = data['Close'].median()
    
    # Calcular medias móviles
    data['SMA_5'] = data['Close'].rolling(window=5).mean()
    data['SMA_20'] = data['Close'].rolling(window=20).mean()

    # Crear figuras
    fig_medias_moviles = crear_figura_medias_moviles(data, asset_name)
    fig_histograma = crear_figura_histograma(data, asset_name, mean_price, median_price)
    
    # Guardar las figuras en un archivo HTML
    with open(html_filename, 'w') as f:
        f.write(fig_medias_moviles.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write('<br><br>')
        f.write(fig_histograma.to_html(full_html=False, include_plotlyjs='cdn'))
    
    print(f"Las gráficas han sido guardadas en {html_filename}")

# Crear un archivo HTML para guardar todas las gráficas
html_filename = "analisis_activos.html"
analizar_activo("MXN=X", html_filename)
