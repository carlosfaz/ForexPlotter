import yfinance as yf
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


# Diccionarios por industria
ticker_tech = {
    "AAPL": ("Apple Inc.", "Technology"),
    "ADBE": ("Adobe Inc.", "Technology"),
    "AMD": ("Advanced Micro Devices Inc.", "Technology"),
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
    "AMZN": ("Amazon.com, Inc.", "Technology"),
    "ADSK": ("Autodesk Inc.", "Technology"),
    "NET": ("Cloudflare Inc.", "Technology"),
    "TEAM": ("Atlassian Corporation", "Technology"),
    "WDAY": ("Workday Inc.", "Technology")
}

ticker_bank = {
    "AXP": ("American Express Company", "Finance"),
    "BLK": ("BlackRock Inc.", "Finance"),
    "BAC": ("Bank of America Corporation", "Finance"),
    "C": ("Citigroup Inc.", "Finance"),
    "COF": ("Capital One Financial Corp.", "Finance"),
    "GS": ("Goldman Sachs Group Inc.", "Finance"),
    "ICE": ("Intercontinental Exchange Inc.", "Finance"),
    "JPM": ("JPMorgan Chase & Co.", "Finance"),
    "MS": ("Morgan Stanley", "Finance"),
    "MSC": ("MSCI Inc.", "Finance"),
    "PNC": ("PNC Financial Services", "Finance"),
    "SCHW": ("Charles Schwab Corporation", "Finance"),
    "V": ("Visa Inc.", "Finance"),
    "WFC": ("Wells Fargo & Co.", "Finance"),
    "MSCI": ("MSCI Inc.", "Finance"),
    "AIG": ("American International Group Inc.", "Finance"),
    "ALL": ("Allstate Corporation", "Finance"),
    "AON": ("Aon PLC", "Finance"),
    "BRK-B": ("Berkshire Hathaway Inc.", "Finance"),
    "SPGI": ("S&P Global Inc.", "Finance"),
    "RJF": ("Raymond James Financial Inc.", "Finance"),
    "CINF": ("Cincinnati Financial Corporation", "Finance"),
    "IAG": ("Iamgold Corporation", "Finance"),
    "SYF": ("Synchrony Financial", "Finance"),
    "BLKB": ("Blackboard Inc.", "Finance"),
    "STT": ("State Street Corporation", "Finance"),
    "CME": ("CME Group Inc.", "Finance"),
    "PGR": ("Progressive Corporation", "Finance"),
    "TROW": ("T. Rowe Price Group Inc.", "Finance"),
    "TRV": ("The Travelers Companies Inc.", "Finance")
}

ticker_consumer = {
    "BKNG": ("Booking Holdings Inc.", "Consumer"),
    "CMG": ("Chipotle Mexican Grill Inc.", "Consumer"),
    "CL": ("Colgate-Palmolive Company", "Consumer"),
    "CPB": ("Campbell Soup Company", "Consumer"),
    "DIS": ("The Walt Disney Company", "Consumer"),
    "HLT": ("Hilton Worldwide Holdings Inc.", "Consumer"),
    "K": ("Kellogg Company", "Consumer"),
    "KO": ("Coca-Cola Company", "Consumer"),
    "KDP": ("Keurig Dr Pepper Inc.", "Consumer"),
    "MCD": ("McDonald's Corporation", "Consumer"),
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
    "CLX": ("Clorox Company", "Consumer"),
    "PRGO": ("Perrigo Company", "Consumer"),
    "MCK": ("McKesson Corporation", "Consumer"),
    "COTY": ("Coty Inc.", "Consumer"),
    "EXPE": ("Expedia Group Inc.", "Consumer"),
    "MELI": ("Mercado Libre Inc.", "Consumer"),
    "QSR": ("Restaurant Brands International", "Consumer"),
    "MDLZ": ("Mondelez International", "Consumer"),
    "HOG": ("Harley-Davidson Inc.", "Consumer"),
    "CVS": ("CVS Health Corporation", "Consumer"),
    "GIS": ("General Mills Inc.", "Consumer"),
    "NKE": ("Nike Inc.", "Consumer"),
    "TGT": ("Target Corporation", "Consumer"),
    "WMT": ("Walmart Inc.", "Consumer")
}

ticker_healthcare = {
    "ABBV": ("AbbVie Inc.", "Healthcare"),
    "ABT": ("Abbott Laboratories", "Healthcare"),
    "AMGN": ("Amgen Inc.", "Healthcare"),
    "BAX": ("Baxter International Inc.", "Healthcare"),
    "BMY": ("Bristol-Myers Squibb", "Healthcare"),
    "CI": ("Cigna Group", "Healthcare"),
    "DHR": ("Danaher Corporation", "Healthcare"),
    "GILD": ("Gilead Sciences Inc.", "Healthcare"),
    "HUM": ("Humana Inc.", "Healthcare"),
    "IDXX": ("IDEXX Laboratories Inc.", "Healthcare"),
    "IQV": ("IQVIA Holdings Inc.", "Healthcare"),
    "ISRG": ("Intuitive Surgical Inc.", "Healthcare"),
    "JNJ": ("Johnson & Johnson", "Healthcare"),
    "LLY": ("Eli Lilly and Co.", "Healthcare"),
    "MRK": ("Merck & Co. Inc.", "Healthcare"),
    "MDT": ("Medtronic PLC", "Healthcare"),
    "PFE": ("Pfizer Inc.", "Healthcare"),
    "REGN": ("Regeneron Pharmaceuticals", "Healthcare"),
    "SYK": ("Stryker Corporation", "Healthcare"),
    "UNH": ("UnitedHealth Group Incorporated", "Healthcare"),
    "VRTX": ("Vertex Pharmaceuticals", "Healthcare"),
    "BSX": ("Boston Scientific Corporation", "Healthcare"),
    "BDX": ("Becton, Dickinson and Company", "Healthcare"),
    "EW": ("Edwards Lifesciences Corporation", "Healthcare"),
    "ZBH": ("Zimmer Biomet Holdings Inc.", "Healthcare")
}

ticker_energy = {
    "COP": ("ConocoPhillips", "Energy"),
    "CVX": ("Chevron Corporation", "Energy"),
    "EOG": ("EOG Resources Inc.", "Energy"),
    "FTI": ("TechnipFMC", "Energy"),
    "APA": ("APA Corporation", "Energy"),
    "BP": ("BP PLC", "Energy"),
    "BKR": ("Baker Hughes Company", "Energy"),
    "XLE": ("Energy Select Sector SPDR Fund", "Energy"),
    "HAL": ("Halliburton Company", "Energy"),
    "HES": ("Hess Corporation", "Energy"),
    "ENB": ("Enbridge Inc.", "Energy"),
    "KMI": ("Kinder Morgan Inc.", "Energy"),
    "TRP": ("TransCanada Corporation", "Energy"),
    "KOS": ("Kosmos Energy Ltd.", "Energy"),
    "OXY": ("Occidental Petroleum Corporation", "Energy"),
    "SLB": ("Schlumberger Limited", "Energy"),
    "WMB": ("Williams Companies Inc.", "Energy"),
    "XOM": ("Exxon Mobil Corporation", "Energy")
}

ticker_industrials = {
    "CAT": ("Caterpillar Inc.", "Industrials"),
    "CSX": ("CSX Corporation", "Industrials"),
    "DE": ("Deere & Co.", "Industrials"),
    "EMR": ("Emerson Electric Co.", "Industrials"),
    "FDX": ("FedEx Corporation", "Industrials"),
    "GD": ("General Dynamics Corporation", "Industrials"),
    "GE": ("General Electric Company", "Industrials"),
    "HON": ("Honeywell International Inc.", "Industrials"),
    "ITW": ("Illinois Tool Works Inc.", "Industrials"),
    "LMT": ("Lockheed Martin Corporation", "Industrials"),
    "MMM": ("3M Company", "Industrials"),
    "NSC": ("Norfolk Southern Corporation", "Industrials"),
    "ROK": ("Rockwell Automation", "Industrials"),
    "RSG": ("Republic Services Inc.", "Industrials"),
    "UPS": ("United Parcel Service", "Industrials"),
    "XPO": ("XPO Logistics Inc.", "Industrials"),
    "ARCB": ("ArcBest Corporation", "Logistics"),
    "JBHT": ("J.B. Hunt Transport Services Inc.", "Logistics"),
    "KNX": ("Knight-Swift Transportation Holdings", "Logistics"),
    "MATX": ("Matson Inc.", "Logistics"),
    "ODFL": ("Old Dominion Freight Line Inc.", "Logistics"),
    "R": ("Ryder System Inc.", "Logistics"),
    "UNP": ("Union Pacific Corporation", "Logistics"),
    "WERN": ("Werner Enterprises Inc.", "Logistics"),
    "GWW": ("W.W. Grainger Inc.", "Industrials")
}

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
    "XEL": ("Xcel Energy Inc.", "Utilities")
}
ticker_retail = {
    "BBY": ("Best Buy Co. Inc.", "Retail"),
    "COST": ("Costco Wholesale Corporation", "Retail"),
    "JWN": ("Nordstrom Inc.", "Retail"),
    "KSS": ("Kohl's Corporation", "Retail"),
    "DG": ("Dollar General Corporation", "Retail"),
    "FL": ("Foot Locker Inc.", "Retail"),
    "TJX": ("TJX Companies Inc.", "Retail"),
    "HD": ("Home Depot Inc.", "Retail"),
    "LOW": ("Lowe's Companies Inc.", "Retail"),
    "M": ("Macy's Inc.", "Retail"),
    "ULTA": ("Ulta Beauty Inc.", "Retail")
}

ticker_logistics = {
    "ARCB": ("ArcBest Corporation", "Logistics"),
    "JBHT": ("J.B. Hunt Transport Services Inc.", "Logistics"),
    "KNX": ("Knight-Swift Transportation Holdings", "Logistics"),
    "MATX": ("Matson Inc.", "Logistics"),
    "ODFL": ("Old Dominion Freight Line Inc.", "Logistics"),
    "R": ("Ryder System Inc.", "Logistics"),
    "UNP": ("Union Pacific Corporation", "Logistics"),
    "WERN": ("Werner Enterprises Inc.", "Logistics")
}

# Ahora unimos todos los diccionarios en uno solo

# Unir todos los diccionarios en un solo diccionario
tickers_info = {**ticker_tech, **ticker_bank, **ticker_consumer, **ticker_healthcare, 
                **ticker_energy, **ticker_industrials, **ticker_utilities, 
                **ticker_retail, **ticker_logistics}

# Function to obtain historical data
def obtener_datos(tickers_info, start_date, end_date):
    tickers = list(tickers_info.keys())  # Get tickers from dictionary keys
    precios = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    retornos = precios.pct_change().dropna()
    
    # Check for null values
    if retornos.isnull().any().any():
        print("Warning: There are null values in returns.")
        retornos = retornos.dropna()
    
    return precios, retornos

# Calculate performance metrics and covariance matrix
def calcular_metricas(retornos):
    media_retornos = retornos.mean() * 252  # Annual returns
    cov_matrix = retornos.cov() * 252  # Annualized covariance matrix
    
    # Check if the covariance matrix has null values
    if cov_matrix.isnull().any().any():
        print("Warning: There are null values in the covariance matrix.")
        cov_matrix = cov_matrix.dropna(axis=0, how='all').dropna(axis=1, how='all')
    
    return media_retornos, cov_matrix

# Efficient frontier calculation
def frontera_eficiente(media_retornos, cov_matrix, num_puntos=100):
    num_activos = len(media_retornos)

    # Ensure there are no zeros in the covariance matrix diagonal
    if np.any(np.isclose(np.diagonal(cov_matrix), 0)):
        print("Warning: There are zeros in the covariance matrix diagonal, which could cause issues when inverting.")
        return [], [], []

    # Covariance matrix inversion with error handling
    try:
        inv_cov_matrix = np.linalg.inv(cov_matrix)
    except np.linalg.LinAlgError:
        print("Error: Covariance matrix is not invertible.")
        return [], [], []

    # Auxiliary vectors
    ones = np.ones(num_activos)

    # Calculate constants for the efficient frontier
    A = ones.T @ inv_cov_matrix @ ones
    B = ones.T @ inv_cov_matrix @ media_retornos
    C = media_retornos.T @ inv_cov_matrix @ media_retornos
    D = A * C - B**2

    # Ensure D is not close to zero (avoid division by zero)
    if np.isclose(D, 0): 
        return [], [], []

    # Range of target returns
    retornos_objetivo = np.linspace(media_retornos.min(), media_retornos.max(), num_puntos)

    # Initialize results
    riesgos = []
    retornos = []
    pesos = []

    # Iterate over each target return
    for mu in retornos_objetivo:
        lambda1 = (C - B * mu) / D
        lambda2 = (A * mu - B) / D
        w = lambda1 * inv_cov_matrix @ ones + lambda2 * inv_cov_matrix @ media_retornos

        # Calculate risk and store results
        riesgo = np.sqrt(w.T @ cov_matrix @ w)
        riesgos.append(riesgo)
        retornos.append(mu)
        pesos.append(w)

    return riesgos, retornos, pesos

# Plot efficient frontier for each industry
def graficar_frontera_eficiente(media_retornos, cov_matrix, riesgos, retornos, tickers_info, industria):
    fig = go.Figure()

    # Points for stocks with full names
    for ticker, (nombre_completo, _) in tickers_info.items():
        i = list(tickers_info.keys()).index(ticker)  # Get ticker index
        fig.add_trace(go.Scatter(
            x=[np.sqrt(cov_matrix.iloc[i, i])],  # Standard deviation
            y=[media_retornos.iloc[i]],  # Expected return using iloc[]
            mode='markers+text',
            text=nombre_completo,  # Display full name instead of ticker
            name=ticker,
            textposition="top center",
            marker=dict(size=10, color="red", line=dict(width=1))
        ))

    # Efficient frontier
    fig.add_trace(go.Scatter(
        x=riesgos,
        y=retornos,
        mode='lines',
        name='Efficient Frontier',
        line=dict(color='blue', width=2)
    ))

    fig.update_layout(
        title=f"Efficient Frontier for the {industria} Industry",
        xaxis_title="Risk (Standard Deviation)",
        yaxis_title="Expected Return",
        showlegend=True,
        width=1200,  # Figure width in pixels
        height=800   # Figure height in pixels
    )

    return fig

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


# Fecha de inicio y fin
start_date = '2020-01-01'
end_date = '2024-11-24'

# Obtener precios y retornos
precios, retornos = obtener_datos(tickers_info, start_date, end_date)
media_retornos, cov_matrix = calcular_metricas(retornos)

# Agrupar los tickers por industria y excluir los inactivos
industries = {}
for ticker, (nombre_completo, industria) in tickers_info.items():
    if is_ticker_active(ticker, start_date, end_date):  # Comprobar si el ticker tiene datos válidos
        if industria not in industries:
            industries[industria] = []
        industries[industria].append(ticker)

# Recorrer cada industria para calcular la frontera eficiente y el mix de activos
for industria, tickers in industries.items():
    # Filtrar tickers disponibles en precios para esta industria
    tickers_disponibles = [ticker for ticker in tickers if ticker in precios.columns]

    if tickers_disponibles:
        # Calcular frontera eficiente para la industria
        riesgos, retornos_frontera, pesos = frontera_eficiente(
            media_retornos[tickers_disponibles], 
            cov_matrix.loc[tickers_disponibles, tickers_disponibles]
        )

        # Verificación de que los resultados no están vacíos
        if not riesgos or not retornos_frontera or not pesos:
            print(f"Error al calcular la frontera eficiente para la industria {industria}. Verifica los datos.")
        else:
            # Obtener el mix de activos sugerido (puedes elegir el portafolio con el retorno máximo, mínimo riesgo, etc.)
            indice_optimo = np.argmax(retornos_frontera)
            pesos_optimos = pesos[indice_optimo]

            # Normalizar los pesos para que sumen 1 y asegurarnos de que no haya valores negativos
            pesos_optimos = np.maximum(pesos_optimos, 0)  # Eliminar los pesos negativos
            pesos_optimos = pesos_optimos / np.sum(pesos_optimos)  # Normalizar los pesos para que sumen 1
            
            # Mostrar el mix sugerido por industria
            print(f"\nMix sugerido por el modelo para la industria {industria}:")
            
            # Crear una lista de tuplas con ticker, nombre y peso
            mix_sugerido = [(tickers_info[ticker], ticker, pesos_optimos[i] * 100) for i, ticker in enumerate(tickers_disponibles)]
            
            # Ordenar la lista de mayor a menor según el peso (porcentaje)
            mix_sugerido = sorted(mix_sugerido, key=lambda x: x[2], reverse=True)
            
            # Imprimir el mix ordenado
            for nombre, ticker, peso in mix_sugerido:
                print(f"{nombre} ({ticker}): {peso:.2f}%")
    else:
        print(f"No hay tickers disponibles para la industria {industria}.")


# Generate plots and save to HTML file
html_filename = 'efficient_frontier_industries.html'
with open(html_filename, 'w', encoding='utf-8') as f:  # UTF-8 encoding
    f.write('<html><body>')
    
    for industria, tickers in industries.items():
        # Filter available tickers in the prices (those that have no NaN)
        tickers_disponibles = [ticker for ticker in tickers if ticker in precios.columns]

        # Calculate efficient frontier
        riesgos, retornos, _ = frontera_eficiente(media_retornos[tickers_disponibles], cov_matrix.loc[tickers_disponibles, tickers_disponibles])

        # Generate plot for the industry
        fig = graficar_frontera_eficiente(media_retornos[tickers_disponibles], cov_matrix.loc[tickers_disponibles, tickers_disponibles], riesgos, retornos, {ticker: tickers_info[ticker] for ticker in tickers_disponibles}, industria)
        
        # Write each figure as HTML inside the file, one below the other
        f.write(f'<h2>{industria} Industry</h2>')
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))  # Include Plotly.js from CDN

    f.write('</body></html>')

print(f"All charts have been saved to {html_filename}")
