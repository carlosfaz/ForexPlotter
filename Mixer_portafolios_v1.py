import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize
import time

# Guardamos el tiempo inicial
start_time = time.time()

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

print(f"Obteniendo data en {time.time() - start_time:.2f}.")

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
    
    # Regularization to avoid invertibility issues
    epsilon = 1e-6
    cov_matrix += np.eye(len(cov_matrix)) * epsilon
    
    return media_retornos, cov_matrix

# Function to calculate portfolio weights with non-negative constraints
def optimizar_pesos(cov_matrix, media_retornos=None, objetivo='min_var', tasa_libre_riesgo=0.02):
    n = len(cov_matrix)
    ones = np.ones(n)

    def minima_varianza(w):
        return w.T @ cov_matrix @ w

    def sharpe_ratio(w):
        exceso_retorno = media_retornos - tasa_libre_riesgo
        return -((w @ exceso_retorno) / np.sqrt(w @ cov_matrix @ w))

    # Objective function selection
    if objetivo == 'min_var':
        fun = minima_varianza
    elif objetivo == 'max_sharpe':
        fun = sharpe_ratio
    else:
        raise ValueError("Objetivo no válido. Use 'min_var' o 'max_sharpe'.")

    # Constraints and bounds
    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]  # Weights sum to 1
    bounds = [(0, 1) for _ in range(n)]  # No short selling (no negative weights)

    # Initial guess: equal weights
    w0 = np.ones(n) / n

    # Optimization
    result = minimize(fun, w0, bounds=bounds, constraints=constraints)
    if not result.success:
        raise ValueError(f"Optimization failed: {result.message}")
    
    return result.x

# Generate portfolios for each optimization model
def generar_portafolios(media_retornos, cov_matrix):
    portafolios = {
        'Mínima Varianza': optimizar_pesos(cov_matrix, objetivo='min_var'),
        'Tangente (Sharpe)': optimizar_pesos(cov_matrix, media_retornos, objetivo='max_sharpe'),
        'Igual Peso': np.ones(len(media_retornos)) / len(media_retornos),
    }
    return portafolios


# Fecha de inicio y fin
start_date = '2020-01-01'
end_date = '2024-11-24'

# Obtener precios y retornos
precios, retornos = obtener_datos(tickers_info, start_date, end_date)
media_retornos, cov_matrix = calcular_metricas(retornos)

print(f"Obteniendo info financiera en {time.time() - start_time:.2f}.")


# Agrupar los tickers por industria
industries = {}
for ticker, (nombre_completo, industria) in tickers_info.items():
    if industria not in industries:
        industries[industria] = []
    industries[industria].append(ticker)

# Generar portafolios por industria
for industria, tickers in industries.items():
    # Filtrar los tickers disponibles en los precios
    tickers_disponibles = [ticker for ticker in tickers if ticker in precios.columns]
    
    if tickers_disponibles:
        # Calcular métricas para los tickers disponibles
        sub_retornos = retornos[tickers_disponibles]
        sub_media_retornos = sub_retornos.mean() * 252
        sub_cov_matrix = sub_retornos.cov() * 252
        
        # Generar portafolios optimizados
        portafolios = generar_portafolios(sub_media_retornos, sub_cov_matrix)

# Función para mostrar la barra de progreso en la consola
def mostrar_progreso(progreso, total, largo_barra=50):
    """
    Muestra la barra de progreso en la consola sin usar sys.
    
    :param progreso: Número actual de la iteración.
    :param total: Número total de iteraciones.
    :param largo_barra: El largo máximo de la barra de progreso.
    """
    porcentaje = (progreso / total) * 100
    barra = '#' * int(porcentaje // 2) + '-' * (largo_barra - int(porcentaje // 2))
    print(f'\r[{barra}] {porcentaje:.2f}%', end='')  # Utiliza `end=''` para evitar salto de línea
    if progreso == total:  # Si es el último progreso, realiza un salto de línea.
        print()

# Obtener información financiera de todos los tickers
def obtener_informacion_financiera(tickers):
    info_financiera = {}
    total_tickers = len(tickers)  # Número total de tickers
    
    for i, ticker in enumerate(tickers):
        try:
            info = yf.Ticker(ticker).info
            info_financiera[ticker] = {
                "P/E": info.get("trailingPE", 0),
                "EPS": info.get("trailingEps", 0),
                "BV": info.get("bookValue", 0),
                "Div Yld": info.get("dividendYield", 0),
                "Div/Sh": info.get("dividendRate", 0),
                "D/E": info.get("debtToEquity", 0),
                "Beta": info.get("beta", 0),
                "ROI": info.get("returnOnInvestment", 0),
                "ROE": info.get("returnOnEquity", 0),
                "Vol": info.get("fiftyDayAverage", 0),
            }
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            info_financiera[ticker] = {key: 0 for key in [
                "P/E", "EPS", "BV", "Div Yld", "Div/Sh", "D/E", "Beta", "ROI", "ROE", "Vol"
            ]}
        
        # Actualizar la barra de progreso
        mostrar_progreso(i + 1, total_tickers)  # +1 porque las listas son 0-indexadas

    return info_financiera

# Recopilar datos financieros una sola vez
all_tickers = list(tickers_info.keys())
info_financiera = obtener_informacion_financiera(all_tickers)

print(f"Imprimiendo resultados en en {time.time() - start_time:.2f}.")


# Generar portafolios por industria con información financiera
html_filename = 'portfolios_optimizados.html'
with open(html_filename, 'w', encoding='utf-8') as f:  # UTF-8 encoding
    f.write('<html>')

    # Añadir estilos CSS en el <head> para que el índice esté siempre en azul
    f.write("""
    <head>
        <style>
            #index a {
                color: blue;
                text-decoration: none;
            }
            #index a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
    """)

    # Agregar JavaScript para ordenar tablas
    f.write("""
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            const tables = document.querySelectorAll("table");
    
            tables.forEach(function (table) {
                const headers = table.querySelectorAll("th");
    
                headers.forEach(function (header, index) {
                    header.addEventListener('click', function () {
                        sortTable(table, index);
                    });
                });
            });
    
            function sortTable(table, colIndex) {
                const rows = Array.from(table.rows).slice(1);
    
                rows.sort(function (rowA, rowB) {
                    const cellA = rowA.cells[colIndex].innerText.trim();
                    const cellB = rowB.cells[colIndex].innerText.trim();
    
                    // Intentar parsear como números (incluye manejo de porcentajes)
                    const valueA = parseValue(cellA);
                    const valueB = parseValue(cellB);
    
                    if (!isNaN(valueA) && !isNaN(valueB)) {
                        return valueB - valueA; // Orden numérico descendente
                    } else {
                        return cellA.localeCompare(cellB); // Orden alfabético
                    }
                });
    
                rows.forEach(function (row) {
                    table.appendChild(row);
                });
            }
    
            function parseValue(value) {
                // Remover símbolos como "%" y convertir a número
                return parseFloat(value.replace('%', '').trim());
            }
        });
    </script>
    """)

    # Índice al inicio
    f.write('<h1>Portfolio Optimization - Index</h1>')
    f.write('<ul id="index">')
    for industria in industries.keys():
        f.write(f'<li><a href="#{industria.replace(" ", "_")}">{industria} Industry</a></li>')
    f.write('</ul>')

    # Iterar sobre las industrias
    for industria, tickers in industries.items():
        tickers_disponibles = [ticker for ticker in tickers if ticker in precios.columns]

        if tickers_disponibles:
            # Calcular portafolios optimizados
            sub_retornos = retornos[tickers_disponibles]
            sub_media_retornos = sub_retornos.mean() * 252
            sub_cov_matrix = sub_retornos.cov() * 252
            portafolios = generar_portafolios(sub_media_retornos, sub_cov_matrix)

            # Agregar una sección por industria
            f.write(f'<h2 id="{industria.replace(" ", "_")}">{industria} Industry</h2>')
            f.write('<table border="1"><tr><th>Activo</th><th>Ticker</th>')

            # Agregar columnas de información financiera
            financial_headers = ["P/E", "EPS", "BV", "Div Yld", "Div/Sh", "D/E", "Beta", "ROI", "ROE", "Vol"]
            for header in financial_headers:
                f.write(f'<th>{header}</th>')

            # Agregar columnas de los modelos de optimización
            for modelo in portafolios.keys():
                f.write(f'<th>{modelo}</th>')

            f.write('</tr>')

            # Generar filas con datos financieros y portafolios
            for i, ticker in enumerate(tickers_disponibles):
                f.write(f'<tr><td>{tickers_info[ticker][0]}</td><td>{ticker}</td>')

                # Agregar columnas de información financiera
                for value in info_financiera[ticker].values():
                    f.write(f'<td>{value:.2f}</td>')

                # Agregar columnas de portafolios optimizados
                for modelo, pesos in portafolios.items():
                    peso = pesos[i] * 100  # Convertir a porcentaje
                    f.write(f'<td>{peso:.2f}%</td>')

                f.write('</tr>')

            f.write('</table><br>')
            f.write(f'<button onclick="window.location.href=\'#\'">Back to Index</button>')

    f.write('</body></html>')

print(f"Portfolio mixes have been saved to {html_filename}")



