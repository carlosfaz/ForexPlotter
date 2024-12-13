import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

#tickers = ["AAPL", "TSLA"]


df=pd.read_csv("mis_tickers.txt")
tickers = df["0"].to_list()

def obtener_datos(ticker_symbol, period, interval):
    """Obtiene los datos históricos de un ticker con el periodo e intervalo especificados."""
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period=period, interval=interval)
    
    if data.empty:
        print(f"No se han encontrado datos para {ticker_symbol}.")
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
        name=f'{ticker_symbol}',  # Usar solo el ticker en el nombre
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
    
    # Titulo dinámico basado en periodo e intervalo
    title = f"{ticker_symbol} - Periodo: {periodo}, Intervalo: {intervalo}"

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


# Función para mostrar una barra de progreso
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    # Imprimir una nueva línea al completar
    if iteration == total: 
        print()


# Función para obtener la información financiera
def get_financial_info(tickers):
    financial_data = []
    total_tickers = len(tickers)
    for i, ticker in enumerate(tickers):
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Recopilando la información financiera abreviada
        financial_info = {
            "Ticker": ticker,
            "Nombre": info.get("longName", 0),
            "Sector": info.get("sector", 0),
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


def agregar_busqueda_y_script(f):
    """Agrega el campo de búsqueda y el script para ordenar y filtrar las tablas."""
    busqueda_y_script = """
    <label for="search">Buscar en la tabla:</label>
    <input type="text" id="search" onkeyup="filterTable()" placeholder="Buscar...">
    <br><br>

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
                return parseFloat(value.replace('%', '').trim());
            }

            window.filterTable = function() {
                const input = document.getElementById("search");
                const filter = input.value.toLowerCase();
                const rows = document.querySelectorAll("table tr");

                rows.forEach(function(row, index) {
                    if (index === 0) return;  // Ignorar la primera fila (encabezados)

                    const cells = row.querySelectorAll("td");
                    let found = false;

                    cells.forEach(function(cell) {
                        if (cell.innerText.toLowerCase().includes(filter)) {
                            found = true;
                        }
                    });

                    row.style.display = found ? "" : "none";
                });
            };

            // Función para copiar la tabla al portapapeles
            window.copyTableToClipboard = function(tableId) {
                const table = document.getElementById(tableId);
                let range, selection;

                if (document.body.createTextRange) {  // Para IE
                    range = document.body.createTextRange();
                    range.moveToElementText(table);
                    range.select();
                    document.execCommand('copy');
                } else if (window.getSelection) {  // Para otros navegadores
                    selection = window.getSelection();
                    range = document.createRange();
                    range.selectNodeContents(table);
                    selection.removeAllRanges();
                    selection.addRange(range);
                    document.execCommand('copy');
                }

                alert("Tabla copiada al portapapeles");
            };
        });
    </script>
    """
    f.write(busqueda_y_script)


def guardar_graficas_html(html_filename, *figs, df):
    """Guarda gráficas y datos financieros organizados por sector en un archivo HTML."""
    # Agrupar los datos por sector
    sectors = df.groupby("Sector")
    
    # Guardar la información en HTML
    with open(html_filename, 'w', encoding='utf-8') as f:  # Codificación UTF-8
        # Crear el índice al inicio del archivo HTML
        f.write("<h1 id='top'>Índice de Gráficas y Datos Financieros</h1>\n")
        f.write("<ul style='columns: 5;'>\n")  # Índice en varias columnas
        
        # Crear enlaces al índice de los tickers (gráficas)
        for i, fig in enumerate(figs):
            ticker_symbol = fig.layout.title.text.split('(')[0].strip()  # Obtener el nombre sin ticker
            f.write(f'<li><a href="#ticker{i}" style="color:blue;">{ticker_symbol}</a></li>\n')
        f.write("</ul>\n\n")

        # Llamada a la función de búsqueda y ordenación
        agregar_busqueda_y_script(f)

        # Crear tabla por sector
        for sector, group in sectors:
            f.write(f'<h2>Sector: {sector}</h2>\n')
            # Asegurarse de que los encabezados de las tablas se muestren correctamente
            f.write(group.to_html(index=False, header=True))

        # Guardar las gráficas con sus títulos y asignar ID a cada sección
        for i, fig in enumerate(figs):
            f.write(f'<h2 id="ticker{i}">{fig.layout.title.text}</h2>\n')  # Título con ID
            f.write(f'<button onclick="window.location.href=\'#top\'">Volver al Inicio</button>\n')  # Botón para ir al inicio
            f.write(fig.to_html(full_html=True, include_plotlyjs="cdn"))
            f.write("<br><br>\n")

    print(f"Las gráficas y las tablas por sector han sido guardadas en {html_filename}")

# Procesar los tickers
figs = []
index_id = 0
total_tasks = len(tickers) * 1  # Solo 1 intervalo por ticker
current_task = 0  # Contador para la barra de progreso

# Bucle para procesar los tickers
for ticker in tickers:
    for periodo, intervalo in [("1d", "1m")]:  # Ejemplo de intervalo
        data, weekend_jumps = obtener_datos(ticker, periodo, intervalo)
        if data is not None:
            # Crear gráfico
            fig = crear_grafica(data, weekend_jumps, periodo, intervalo, ticker, index_id)
            figs.append(fig)
            index_id += 1
        current_task += 1
        print_progress_bar(current_task, total_tasks)

# Crear DataFrame de datos financieros
financial_data = get_financial_info(tickers)
df_financial_data = pd.DataFrame(financial_data)

# Guardar en HTML
html_filename = "grafico_precios_historicos.html"
guardar_graficas_html(html_filename, *figs, df=df_financial_data)

print("\nProcesamiento completado.")
