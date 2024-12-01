import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import time
start_time = time.time()

# Technology
ticker_tech = {
    "AAPL": ("Apple Inc.", "Technology"),
    "ADBE": ("Adobe Inc.", "Technology"),
    "AMD": ("Advanced Micro Devices Inc.", "Technology"),
    "AMZN": ("Amazon.com, Inc.", "Technology"),
    "GOOG": ("Alphabet Inc. (Google)", "Technology"),
    "GOOGL": ("Alphabet Inc. (Google)", "Technology"),
    "HPQ": ("HP Inc.", "Technology"),
    "IBM": ("International Business Machines Corporation", "Technology"),
    "INTC": ("Intel Corporation", "Technology"),
    "MSFT": ("Microsoft Corporation", "Technology"),
    "NVDA": ("NVIDIA Corporation", "Technology"),
    "ORCL": ("Oracle Corporation", "Technology"),
    "PANW": ("Palo Alto Networks Inc.", "Technology"),
    "QCOM": ("Qualcomm Inc.", "Technology"),
    "SNOW": ("Snowflake Inc.", "Technology"),
    "TXN": ("Texas Instruments Inc.", "Technology"),
    "WDAY": ("Workday Inc.", "Technology"),
    "ZM": ("Zoom Video Communications Inc.", "Technology"),
    "CRM": ("Salesforce Inc.", "Technology"),
    "TTD": ("The Trade Desk Inc.", "Technology"),
    "SHOP": ("Shopify Inc.", "Technology"),
    "ASML": ("ASML Holding NV", "Technology"),
    "PYPL": ("PayPal Holdings Inc.", "Technology"),
    "SPOT": ("Spotify Technology S.A.", "Technology"),
    "INTU": ("Intuit Inc.", "Technology"),
    "SNPS": ("Synopsys Inc.", "Technology"),
    "MDB": ("MongoDB Inc.", "Technology"),
    "ZS": ("Zscaler Inc.", "Technology"),
    "NOW": ("ServiceNow Inc.", "Technology"),
    "RBLX": ("Roblox Corporation", "Technology"),
    "VRSN": ("Verisign Inc.", "Technology"),
    "FTNT": ("Fortinet Inc.", "Technology"),
    "OKTA": ("Okta Inc.", "Technology"),
    "WDAY": ("Workday Inc.", "Technology"),
    "ADSK": ("Autodesk Inc.", "Technology"),
    "NET": ("Cloudflare Inc.", "Technology"),
    "TEAM": ("Atlassian Corporation", "Technology"),

}

# Finance
ticker_bank = {
    "AXP": ("American Express Company", "Finance"),
    "BLK": ("BlackRock Inc.", "Finance"),
    "BAC": ("Bank of America Corporation", "Finance"),
    "C": ("Citigroup Inc.", "Finance"),
    "CME": ("CME Group Inc.", "Finance"),
    "COF": ("Capital One Financial Corp.", "Finance"),
    "GS": ("Goldman Sachs Group Inc.", "Finance"),
    "ICE": ("Intercontinental Exchange Inc.", "Finance"),
    "JPM": ("JPMorgan Chase & Co.", "Finance"),
    "MS": ("Morgan Stanley", "Finance"),
    "MSC": ("MSCI Inc.", "Finance"),
    "PGR": ("Progressive Corporation", "Finance"),
    "PNC": ("PNC Financial Services", "Finance"),
    "SCHW": ("Charles Schwab Corporation", "Finance"),
    "TROW": ("T. Rowe Price Group Inc.", "Finance"),
    "V": ("Visa Inc.", "Finance"),
    "WFC": ("Wells Fargo & Co.", "Finance"),
    "MSCI": ("MSCI Inc.", "Finance"),
    "AIG": ("American International Group Inc.", "Finance"),
    "ALL": ("Allstate Corporation", "Finance"),
    "AON": ("Aon PLC", "Finance"),
    "BRK-B": ("Berkshire Hathaway Inc.", "Finance"),
    "SPGI": ("S&P Global Inc.", "Finance"),
    "PGR": ("Progressive Corporation", "Finance"),
    "TRV": ("The Travelers Companies Inc.", "Finance"),
    "RJF": ("Raymond James Financial Inc.", "Finance"),
    "CINF": ("Cincinnati Financial Corporation", "Finance"),
    "IAG": ("Iamgold Corporation", "Finance"),
    "SYF": ("Synchrony Financial", "Finance"),
    "BLKB": ("Blackboard Inc.", "Finance"),
    "CME": ("CME Group Inc.", "Finance"),
    "STT": ("State Street Corporation", "Finance"),
    "TROW": ("T. Rowe Price Group Inc.", "Finance"),
}

# Consumer
ticker_consumer = {
    "BKNG": ("Booking Holdings Inc.", "Consumer"),
    "CMG": ("Chipotle Mexican Grill Inc.", "Consumer"),
    "CL": ("Colgate-Palmolive Company", "Consumer"),
    "CPB": ("Campbell Soup Company", "Consumer"),
    "DIS": ("The Walt Disney Company", "Consumer"),
    "GIS": ("General Mills Inc.", "Consumer"),
    "HLT": ("Hilton Worldwide Holdings Inc.", "Consumer"),
    "K": ("Kellogg Company", "Consumer"),
    "KO": ("Coca-Cola Company", "Consumer"),
    "KDP": ("Keurig Dr Pepper Inc.", "Consumer"),
    "MCD": ("McDonald's Corporation", "Consumer"),
    "NKE": ("Nike Inc.", "Consumer"),
    "PEP": ("PepsiCo Inc.", "Consumer"),
    "PG": ("Procter & Gamble Co.", "Consumer"),
    "RL": ("Ralph Lauren Corporation", "Consumer"),
    "TAP": ("Molson Coors Beverage Company", "Consumer"),
    "WHR": ("Whirlpool Corporation", "Consumer"),
    "YUM": ("Yum! Brands Inc.", "Consumer"),
    "SBUX": ("Starbucks Corporation", "Consumer"),
    "SYY": ("Sysco Corporation", "Consumer"),
    "TSN": ("Tyson Foods Inc.", "Consumer"),
    "BUD": ("Anheuser-Busch InBev", "Consumer"),
    "KHC": ("Kraft Heinz Company", "Consumer"),
    "GIS": ("General Mills Inc.", "Consumer"),
    "NKE": ("Nike Inc.", "Consumer"),
    "CVS": ("CVS Health Corporation", "Consumer"),
    "CLX": ("Clorox Company", "Consumer"),
    "PRGO": ("Perrigo Company", "Consumer"),
    "MCK": ("McKesson Corporation", "Consumer"),
    "COTY": ("Coty Inc.", "Consumer"),
    "TGT": ("Target Corporation", "Consumer"),
    "WMT": ("Walmart Inc.", "Consumer"),
    "EXPE": ("Expedia Group Inc.", "Consumer"),
    "MELI": ("Mercado Libre Inc.", "Consumer"),
    "QSR": ("Restaurant Brands International", "Consumer"),
    "MDLZ": ("Mondelez International", "Consumer"),
    "HOG": ("Harley-Davidson Inc.", "Consumer"),
}

# Healthcare
ticker_healthcare = {
    "ABBV": ("AbbVie Inc.", "Healthcare"),
    "ABT": ("Abbott Laboratories", "Healthcare"),
    "BAX": ("Baxter International Inc.", "Healthcare"),
    "BMY": ("Bristol-Myers Squibb", "Healthcare"),
    "CI": ("Cigna Group", "Healthcare"),
    "CVS": ("CVS Health Corporation", "Healthcare"),
    "DHR": ("Danaher Corporation", "Healthcare"),
    "GILD": ("Gilead Sciences Inc.", "Healthcare"),
    "HUM": ("Humana Inc.", "Healthcare"),
    "ISRG": ("Intuitive Surgical Inc.", "Healthcare"),
    "JNJ": ("Johnson & Johnson", "Healthcare"),
    "LLY": ("Eli Lilly and Co.", "Healthcare"),
    "MDT": ("Medtronic PLC", "Healthcare"),
    "MRK": ("Merck & Co. Inc.", "Healthcare"),
    "PFE": ("Pfizer Inc.", "Healthcare"),
    "VRTX": ("Vertex Pharmaceuticals", "Healthcare"),
    "ZBH": ("Zimmer Biomet Holdings Inc.", "Healthcare"),
    "AMGN": ("Amgen Inc.", "Healthcare"),
    "REGN": ("Regeneron Pharmaceuticals", "Healthcare"),
    "VRTX": ("Vertex Pharmaceuticals", "Healthcare"),
    "IDXX": ("IDEXX Laboratories Inc.", "Healthcare"),
    "IQV": ("IQVIA Holdings Inc.", "Healthcare"),
    "SYK": ("Stryker Corporation", "Healthcare"),
    "BSX": ("Boston Scientific Corporation", "Healthcare"),
    "ZBH": ("Zimmer Biomet Holdings Inc.", "Healthcare"),
    "MDT": ("Medtronic PLC", "Healthcare"),
    "BDX": ("Becton, Dickinson and Company", "Healthcare"),
    "EW": ("Edwards Lifesciences Corporation", "Healthcare"),
    "CVS": ("CVS Health Corporation", "Healthcare"),
    "UNH": ("UnitedHealth Group Incorporated", "Healthcare"),
    "PFE": ("Pfizer Inc.", "Healthcare"),
    "ABBV": ("AbbVie Inc.", "Healthcare"),
    "JNJ": ("Johnson & Johnson", "Healthcare"),
    "LLY": ("Eli Lilly and Co.", "Healthcare"),
    "CI": ("Cigna Corporation", "Healthcare"),
}

# Energy
ticker_energy = {
    "APA": ("APA Corporation", "Energy"),
    "BP": ("BP PLC", "Energy"),
    "BKR": ("Baker Hughes Company", "Energy"),
    "COP": ("ConocoPhillips", "Energy"),
    "EOG": ("EOG Resources Inc.", "Energy"),
    "FTI": ("TechnipFMC", "Energy"),
    "HAL": ("Halliburton Company", "Energy"),
    "HES": ("Hess Corporation", "Energy"),
    "KMI": ("Kinder Morgan Inc.", "Energy"),
    "OXY": ("Occidental Petroleum Corporation", "Energy"),
    "SLB": ("Schlumberger Limited", "Energy"),
    "WMB": ("Williams Companies Inc.", "Energy"),
    "XLE": ("Energy Select Sector SPDR Fund", "Energy"),
    "XOM": ("Exxon Mobil Corporation", "Energy"),
    "CVX": ("Chevron Corporation", "Energy"),
    "ENB": ("Enbridge Inc.", "Energy"),
    "COP": ("ConocoPhillips", "Energy"),
    "EOG": ("EOG Resources Inc.", "Energy"),
    "SLB": ("Schlumberger Limited", "Energy"),
    "OXY": ("Occidental Petroleum Corporation", "Energy"),
    "KMI": ("Kinder Morgan Inc.", "Energy"),
    "XOM": ("Exxon Mobil Corporation", "Energy"),
    "CVX": ("Chevron Corporation", "Energy"),
    "WMB": ("Williams Companies Inc.", "Energy"),
    "FTI": ("TechnipFMC", "Energy"),
    "HAL": ("Halliburton Company", "Energy"),
    "HES": ("Hess Corporation", "Energy"),
    "TRP": ("TransCanada Corporation", "Energy"),
    "KOS": ("Kosmos Energy Ltd.", "Energy"),
    }

# Industrials
ticker_industrials = {
    "CAT": ("Caterpillar Inc.", "Industrials"),
    "CSX": ("CSX Corporation", "Industrials"),
    "DE": ("Deere & Co.", "Industrials"),
    "DOV": ("Dover Corporation", "Industrials"),
    "EMR": ("Emerson Electric Co.", "Industrials"),
    "FDX": ("FedEx Corporation", "Industrials"),
    "GE": ("General Electric Company", "Industrials"),
    "GD": ("General Dynamics Corporation", "Industrials"),
    "HON": ("Honeywell International Inc.", "Industrials"),
    "ITW": ("Illinois Tool Works Inc.", "Industrials"),
    "LMT": ("Lockheed Martin Corporation", "Industrials"),
    "LUV": ("Southwest Airlines Co.", "Industrials"),
    "MMM": ("3M Company", "Industrials"),
    "NSC": ("Norfolk Southern Corporation", "Industrials"),
    "ROK": ("Rockwell Automation", "Industrials"),
    "TRV": ("The Travelers Companies Inc.", "Industrials"),
    "UPS": ("United Parcel Service", "Industrials"),
    "XPO": ("XPO Logistics Inc.", "Industrials"),
    "MMM": ("3M Company", "Industrials"),
    "CAT": ("Caterpillar Inc.", "Industrials"),
    "LMT": ("Lockheed Martin Corporation", "Industrials"),
    "HON": ("Honeywell International Inc.", "Industrials"),
    "EMR": ("Emerson Electric Co.", "Industrials"),
    "ITW": ("Illinois Tool Works Inc.", "Industrials"),
    "DE": ("Deere & Co.", "Industrials"),
    "UPS": ("United Parcel Service", "Industrials"),
    "FDX": ("FedEx Corporation", "Industrials"),
    "GE": ("General Electric Company", "Industrials"),
    "CSX": ("CSX Corporation", "Industrials"),
    "NSC": ("Norfolk Southern Corporation", "Industrials"),
    "TRV": ("The Travelers Companies Inc.", "Industrials"),
    "ROK": ("Rockwell Automation", "Industrials"),
    "XPO": ("XPO Logistics Inc.", "Industrials"),
    "MMM": ("3M Company", "Industrials"),
    "GD": ("General Dynamics Corporation", "Industrials"),
    "RSG": ("Republic Services Inc.", "Industrials"),
    "GWW": ("W.W. Grainger Inc.", "Industrials"),
}

# Utilities
ticker_utilities = {
    "AEP": ("American Electric Power Company Inc.", "Utilities"),
    "DUK": ("Duke Energy Corporation", "Utilities"),
    "ED": ("Consolidated Edison Inc.", "Utilities"),
    "EXC": ("Exelon Corporation", "Utilities"),
    "NEE": ("NextEra Energy Inc.", "Utilities"),
    "PCG": ("PG&E Corporation", "Utilities"),
    "SRE": ("Sempra Energy", "Utilities"),
    "SO": ("Southern Company", "Utilities"),
    "WEC": ("WEC Energy Group Inc.", "Utilities"),
    "XEL": ("Xcel Energy Inc.", "Utilities"),
}

# Retail
ticker_retail = {
    "AMZN": ("Amazon.com Inc.", "Retail"),
    "BBY": ("Best Buy Co. Inc.", "Retail"),
    "COST": ("Costco Wholesale Corporation", "Retail"),
    "DG": ("Dollar General Corporation", "Retail"),
    "FL": ("Foot Locker Inc.", "Retail"),
    "KSS": ("Kohl's Corporation", "Retail"),
    "TGT": ("Target Corporation", "Retail"),
    "TJX": ("TJX Companies Inc.", "Retail"),
    "WMT": ("Walmart Inc.", "Retail"),
    "JWN": ("Nordstrom Inc.", "Retail"),
    "HD": ("Home Depot Inc.", "Retail"),
    "LOW": ("Lowe's Companies Inc.", "Retail"),
    "TGT": ("Target Corporation", "Retail"),
    "WMT": ("Walmart Inc.", "Retail"),
    "AMZN": ("Amazon.com Inc.", "Retail"),
    "COST": ("Costco Wholesale Corporation", "Retail"),
    "BBY": ("Best Buy Co. Inc.", "Retail"),
    "M": ("Macy's Inc.", "Retail"),
    "ULTA": ("Ulta Beauty Inc.", "Retail"),
    "BBY": ("Best Buy Co. Inc.", "Retail"),
    "KSS": ("Kohl's Corporation", "Retail"),
    "JWN": ("Nordstrom Inc.", "Retail"),
    "TGT": ("Target Corporation", "Retail"),
}

# Logistics
ticker_logistics = {
    "ARCB": ("ArcBest Corporation", "Logistics"),
    "CSX": ("CSX Corporation", "Logistics"),
    "JBHT": ("J.B. Hunt Transport Services Inc.", "Logistics"),
    "KNX": ("Knight-Swift Transportation Holdings", "Logistics"),
    "MATX": ("Matson Inc.", "Logistics"),
    "NSC": ("Norfolk Southern Corporation", "Logistics"),
    "ODFL": ("Old Dominion Freight Line Inc.", "Logistics"),
    "R": ("Ryder System Inc.", "Logistics"),
    "UNP": ("Union Pacific Corporation", "Logistics"),
    "WERN": ("Werner Enterprises Inc.", "Logistics"),
}

# Ahora unimos todos los diccionarios en uno solo

# Unir todos los diccionarios en un solo diccionario
tickers_info = {**ticker_tech, **ticker_bank, **ticker_consumer, **ticker_healthcare, 
                **ticker_energy, **ticker_industrials, **ticker_utilities, 
                **ticker_retail, **ticker_logistics}


def obtener_datos(ticker_symbol, period, interval):
    """Obtiene los datos históricos de un ticker con el periodo e intervalo especificados."""
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period=period, interval=interval)
    
    if data.empty:
        print(f"No se han encontrado datos para {tickers_info[ticker_symbol]} ({ticker_symbol}).")
        return None, None

    # Filtrar saltos mayores a 1 día
    data = data[~data.index.to_series().diff().dt.days.gt(1)]
    
    # Convertir índices a fecha con formato "día mes abreviado y año"
    data['Date'] = data.index.strftime('%d-%b-%Y %H:%M:%S')  # Día, mes abreviado y año (4 dígitos)
    
    # Identificar los saltos entre días
    data['Delta'] = data.index.to_series().diff().dt.days.fillna(0)
    weekend_jumps = data[data['Delta'] > 1].index  # Fechas con saltos

    return data, weekend_jumps


def crear_grafica(data, weekend_jumps, periodo, intervalo, ticker_symbol, index_id):
    """Crea una gráfica de velas con los datos y añade las líneas de saltos."""
    fig = go.Figure()

    # Crear gráfico de velas
    fig.add_trace(go.Candlestick(
        x=data['Date'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name=f'{tickers_info[ticker_symbol][0]}',
        increasing_line_color='green',
        decreasing_line_color='red'
    ))

    # Añadir líneas rojas para los saltos de fin de semana
    for jump in weekend_jumps:
        fig.add_shape(
            type="line",
            x0=jump.strftime('%d-%b-%Y %H:%M:%S'),
            x1=jump.strftime('%d-%b-%Y %H:%M:%S'),
            y0=data['Low'].min(),
            y1=data['High'].max(),
            line=dict(color="red", width=2, dash="dot"),
            xref='x',
            yref='y'
        )

    # Ajustar el diseño para omitir los huecos de tiempo
    fig.update_xaxes(type='category')
    
    # Titulo dinámico basado en periodo, intervalo, y sector
    title = f"{tickers_info[ticker_symbol][0]} ({ticker_symbol}) - Sector: {tickers_info[ticker_symbol][1]}, Periodo: {periodo}, Intervalo: {intervalo}"

    fig.update_layout(
        title=title,
        xaxis_title='Fecha',
        yaxis_title='Precio',
        height=900,
        width=1600,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        xaxis=dict(tickformat='%d-%b-%Y %H:%M:%S', tickmode='auto', nticks=20)
    )

    return fig



# Función para formatear los valores numéricos a "1,234.56"
def formatear_numeros(val):
    try:
        return f"{val:,.2f}"  # Formato de número con comas y 2 decimales
    except:
        return val  # Si no es un número, lo dejamos tal cual

# Función para mostrar una barra de progreso
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    # Imprimir una nueva línea al completar
    if iteration == total: 
        print()

# Función optimizada para obtener la información financiera abreviada
def get_financial_info(tickers_info):
    financial_data = []
    total_tickers = len(tickers_info)
    for i, ticker in enumerate(tickers_info):
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Recopilando la información financiera abreviada
        financial_info = {
            "Ticker": ticker,
            "P/E": info.get("trailingPE", 0),  # P/E Ratio
            "EPS": info.get("trailingEps", 0),  # Earnings per Share
            "BV": info.get("bookValue", 0),  # Book Value
            "Div Yld": info.get("dividendYield", 0),  # Dividend Yield
            "Div/Sh": info.get("dividendRate", 0),  # Dividend per Share
            "D/E": info.get("debtToEquity", 0),  # Debt-to-Equity Ratio
            "Beta": info.get("beta", 0),  # Beta
            "ROI": info.get("returnOnInvestment", 0),  # Return on Investment
            "ROE": info.get("returnOnEquity", 0),  # Return on Equity
            "Vol": info.get("fiftyDayAverage", 0),  # Volatility (50-day)
            "52W H": info.get("fiftyTwoWeekHigh", 0),  # 52 Week High
            "52W L": info.get("fiftyTwoWeekLow", 0),  # 52 Week Low
            "P/B": info.get("priceToBook", 0),  # Price to Book Ratio
            "GM": info.get("grossMargins", 0),  # Gross Margin
            "ROA": info.get("returnOnAssets", 0),  # Return on Assets
            "OM": info.get("operatingMargins", 0),  # Operating Margin
            "Rev Gr": info.get("revenueGrowth", 0),  # Revenue Growth
            "PM": info.get("profitMargins", 0),  # Profit Margin
            "EPS Gr": info.get("earningsGrowth", 0),  # EPS Growth
            "IC": info.get("interestCoverage", 0),  # Interest Coverage
            "CR": info.get("currentRatio", 0),  # Current Ratio
            "NI Stab": info.get("netIncomeStability", 0),  # Net Income Stability
            "Sec Persp": info.get("sectorPerspective", 0)  # Sector Perspective
        }
        financial_data.append(financial_info)
        
        # Actualizar la barra de progreso
        print_progress_bar(i + 1, total_tickers, prefix='Progreso:', suffix='Completado', length=50)
    
    return pd.DataFrame(financial_data)


# Función para analizar las acciones
def analizar_acciones(df, output_filename="resultados.txt"):
    # Definir las condiciones de filtrado y las columnas para ordenación
    filtros_y_orden = {
        'P/E alto (posiblemente sobrevaloradas)': {'condicion': df['P/E'] > 30, 'columna': 'P/E'},
        'Alta rentabilidad por dividendo': {'condicion': df['Div Yld'] > 0.03, 'columna': 'Div Yld'},
        'Beta alto (riesgo elevado)': {'condicion': df['Beta'] > 1, 'columna': 'Beta'},
        'Volumen alto': {'condicion': df['Vol'] > 100, 'columna': 'Vol'},
        'Alta volatilidad (Rango 52W alto)': {'condicion': df['52W H'] - df['52W L'] > 100, 'columna': '52W Range'},
        'Alto riesgo (Beta > 1 y P/E > 30)': {'condicion': (df['Beta'] > 1) & (df['P/E'] > 30), 'columna': ['Beta', 'P/E']},
        'Acciones sin ganancias': {'condicion': df['P/E'] == 0, 'columna': 'P/E'},
        'Alta relación D/E (alto endeudamiento)': {'condicion': df['D/E'] > 1, 'columna': 'D/E'},
        'Alto margen bruto': {'condicion': df['GM'] > 0.5, 'columna': 'GM'},
        'Bajo P/B (menos de 1)': {'condicion': df['P/B'] < 1, 'columna': 'P/B'},
        'Alto ROE (Rentabilidad sobre el capital)': {'condicion': df['ROE'] > 0.15, 'columna': 'ROE'},
        'Alto Crecimiento de Ingresos': {'condicion': df['Rev Gr'] > 0.1, 'columna': 'Rev Gr'},
        'Alto Margen Operativo': {'condicion': df['OM'] > 0.2, 'columna': 'OM'},
        'Alta Rentabilidad sobre Activos (ROA)': {'condicion': df['ROA'] > 0.1, 'columna': 'ROA'}
    }

    # Crear el dataframe para la columna '52W Range' (volatilidad)
    df['52W Range'] = df['52W H'] - df['52W L']

    # Función auxiliar para filtrar, limpiar y ordenar el DataFrame
    def filtrar_y_ordenar(df, condicion, columna_orden):
        df_filtrado = df[condicion]  # Filtrar las filas
        df_filtrado = df_filtrado[(df_filtrado[columna_orden] != 0).all(axis=1)]  # Eliminar filas con valor 0 en columnas relevantes
        if not df_filtrado.empty:
            return df_filtrado.sort_values(by=columna_orden, ascending=False)
        return None

    # Función auxiliar para generar el resultado del análisis
    def generar_resultado(categoria, df_filtrado, columnas):
        resultado = f"\nAcciones con {categoria}:\n"
        resultado += df_filtrado[['Nombre Ticker', *columnas]].to_string(index=False)
        resultado += "\n"
        return resultado

    # Abrir el archivo para escribir los resultados
    with open(output_filename, "w", encoding="utf-8") as file:
        # Iterar sobre el diccionario de filtros y ordenarlos
        for categoria, info in filtros_y_orden.items():
            columna_orden = [info['columna']] if isinstance(info['columna'], str) else info['columna']
            df_filtrado = filtrar_y_ordenar(df, info['condicion'], columna_orden)

            if df_filtrado is None:
                resultado = f"\nNo se encontraron acciones para {categoria}\n"
                print(resultado, end="")
                file.write(resultado)
            else:
                resultado = generar_resultado(categoria, df_filtrado, columna_orden)
                print(resultado, end="")
                file.write(resultado)

def guardar_graficas_html(html_filename, *figs, df, tickers_info):
    # Añadir las columnas de nombres de los tickers e industria
    df['Nombre Ticker'] = df['Ticker'].map(lambda ticker: tickers_info[ticker][0])  # Solo el nombre
    df['Industria'] = df['Ticker'].map(lambda ticker: tickers_info[ticker][1])  # Solo la industria

    # Reordenar las columnas para que 'Nombre Ticker' y 'Industria' sean las primeras
    df = df[['Nombre Ticker', 'Industria'] + [col for col in df.columns if col not in ['Nombre Ticker', 'Industria']]]

    # Aplicar el formato a las columnas numéricas utilizando `apply` + `map`
    df = df.apply(lambda col: col.map(formatear_numeros) if col.dtype != 'O' else col)

    # Guardar la información en HTML
    with open(html_filename, 'w', encoding='utf-8') as f:  # Codificación UTF-8
        # Crear el índice al inicio del archivo HTML
        f.write("<h1 id='top'>Índice de Gráficas y Datos Financieros</h1>\n")
        f.write("<ul style='columns: 5;'>\n")  # Índice en dos columnas
        
        # Crear enlaces al índice de los tickers (gráficas)
        for i, fig in enumerate(figs):
            ticker_symbol = fig.layout.title.text.split('(')[0].strip()  # Obtener el nombre sin ticker
            f.write(f'<li><a href="#ticker{i}" style="color:blue;">{ticker_symbol}</a></li>\n')
        f.write("</ul>\n\n")

        # Insertar la tabla del DataFrame con la información financiera
        f.write("<h2>Información Financiera</h2>\n")
        
        # Centramos la tabla usando márgenes
        f.write("<div style='display: flex; justify-content: center;'>\n")
        f.write(df.to_html(index=False))  # Convertir el DataFrame a HTML y eliminar el índice
        f.write("</div>\n")  # Cierre del contenedor centrado

        # Guardar las gráficas con sus títulos y asignar ID a cada sección
        for i, fig in enumerate(figs):
            f.write(f'<a id="ticker{i}"></a>\n')  # Asignar un ID a cada gráfico
            f.write(f'<h2>{fig.layout.title.text}</h2>\n')  # Título descriptivo (sin industria)
            f.write(fig.to_html(full_html=True, include_plotlyjs="cdn"))
            f.write(f'<br><a href="#top">Ir al inicio</a><br><br>')  # Enlace para ir al inicio
            f.write("\n")

    print(f"Las gráficas y la tabla han sido guardadas en {html_filename}")


# Nombre del archivo HTML
html_filename = "grafico_precios_historicos.html"

# Obtener la información financiera
financial_data = get_financial_info(tickers_info)
df_financial_data = pd.DataFrame(financial_data)

# Crear un DataFrame de pandas para mostrar la información en formato tabular
print(df_financial_data)

print(f"Imprimiendo graficas")

# Obtener datos y gráficas para cada par de periodo/intervalo
# Supongamos que las funciones obtener_datos y crear_grafica ya están definidas
figs = []
index_id = 0
for ticker in tickers_info.keys():
    for periodo, intervalo in [("1mo", "15m")]:  # Version anemica
        data, weekend_jumps = obtener_datos(ticker, periodo, intervalo)
        if data is not None:
            # Mostrar estadísticas solo si el intervalo es de 1 minuto
            fig = crear_grafica(data, weekend_jumps, periodo, intervalo, ticker, f"ticker{index_id}")
            figs.append(fig)
            index_id += 1

# Guardar todas las gráficas y la tabla de información financiera juntas en un solo archivo HTML
guardar_graficas_html(html_filename, *figs, df=df_financial_data, tickers_info=tickers_info)

