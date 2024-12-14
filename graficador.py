import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

#tickers = ["AAPL", "TSLA"]


df=pd.read_csv("tickers/mis_tickers.txt")
tickers = df["0"].to_list()

def obtener_datos(ticker_symbol, period, interval):
    """Obtiene los datos historicos de un ticker con el periodo e intervalo especificados."""
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period=period, interval=interval)
    
    if data.empty:
        print(f"No se han encontrado datos para {ticker_symbol}.")
        return None, None

    # Filtrar saltos mayores a 1 dia
    data = data[~data.index.to_series().diff().dt.days.gt(1)]
    
    # Convertir indices a fecha con formato "dia mes abreviado y año"
    data['Date'] = data.index.strftime('%d-%b-%Y %H:%M:%S')  # Dia, mes abreviado y año (4 digitos)
    
    # Identificar los saltos entre dias
    data['Delta'] = data.index.to_series().diff().dt.days.fillna(0)
    weekend_jumps = data[data['Delta'] > 1].index  # Fechas con saltos

    return data, weekend_jumps


def crear_grafica(data, weekend_jumps, periodo, intervalo, ticker_symbol, index_id):
    """Crea una grafica de velas con los datos y añade las lineas de saltos."""
    fig = go.Figure()

    # Crear grafico de velas
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

    # Añadir lineas rojas para los saltos de fin de semana
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
    
    # Titulo dinamico basado en periodo e intervalo
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


# Funcion para mostrar una barra de progreso
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    # Imprimir una nueva linea al completar
    if iteration == total: 
        print()

def get_financial_info(tickers):
    financial_data = []
    total_tickers = len(tickers)
    
    for i, ticker in enumerate(tickers):
        stock = yf.Ticker(ticker)
        info = stock.info

        # Calculo y obtencion de datos adicionales
        profit_margin = info.get("profitMargins", 0) * 100  # Convertir a porcentaje
        operating_margin = info.get("operatingMargins", 0) * 100  # Convertir a porcentaje
        revenue_growth = info.get("revenueGrowth", 0)
        revenue = info.get("totalRevenue", 0)  # Ingresos totales
        net_income = info.get("netIncomeToCommon", 0)  # Ingreso neto
        ebitda = info.get("ebitda", 0)  # EBITDA

        # Recopilando la informacion financiera abreviada
        financial_info = {
            "Ticker": ticker,
            "Nombre": info.get("longName", "N/A"),
            "Sector": info.get("sector", "N/A"),
            "P/E": info.get("trailingPE", 0),
            "EPS": info.get("trailingEps", 0),
            "BV": info.get("bookValue", 0),
            "Div Yld": info.get("dividendYield", 0),
            "Div/Sh": info.get("dividendRate", 0),
            "D/E": info.get("debtToEquity", 0),
            "Beta": info.get("beta", 0),
            "Profit Margin": f"{profit_margin:,.2f}%",  # Formato porcentaje
            "Operating Margin": f"{operating_margin:,.2f}%",  # Formato porcentaje
            "Revenue Growth": f"{revenue_growth * 100:,.2f}%",  # Formato con comas, con porcentaje
            "ROE": info.get("returnOnEquity", 0),
            "Vol": info.get("fiftyDayAverage", 0),
            "Revenue": f"{revenue:,.0f}",  # Formato con comas
            "Net Income": f"{net_income:,.0f}",  # Formato con comas
            "EBITDA": f"{ebitda:,.0f}",  # Formato con comas
        }
        financial_data.append(financial_info)
        
        # Actualizar la barra de progreso (si tienes una implementada)
        print_progress_bar(i + 1, total_tickers, prefix='Progreso:', suffix='Completado', length=50)
    
    return pd.DataFrame(financial_data)

# Funcion para crear una tabla HTML con toda la informacion
def crear_tabla_general(df, f):
    """Crea una tabla HTML con todos los datos financieros y la escribe en el archivo."""
    f.write('<table id="tabla-general">\n<thead>\n<tr>\n')

    # Escribir encabezados
    for col in df.columns:
        f.write(f'<th>{col}</th>\n')
    f.write('</tr>\n</thead>\n<tbody>\n')

    # Escribir datos
    for _, row in df.iterrows():
        f.write('<tr>\n')
        for col in df.columns:
            value = row[col]
            # Si la columna es un ticker, agregar el hipervinculo
            if col == "Ticker":  # Suponiendo que la columna se llama "Ticker"
                ticker = row[col]
                f.write(f'<td><a href="https://finance.yahoo.com/quote/{ticker}" target="_blank">{ticker}</a></td>\n')
            else:
                # Si la columna es numerica, formatear con 2 decimales
                if isinstance(value, (int, float)):
                    value = f"{value:.2f}"
                f.write(f'<td>{value}</td>\n')
        f.write('</tr>\n')
    f.write('</tbody>\n</table>\n')

# Funcion principal para guardar graficas y tablas en un HTML con indice de acceso rapido a las graficas
def guardar_graficas_html(html_filename, *figs, df):
    """Guarda graficas y datos financieros en un archivo HTML con indice de acceso rapido."""
    with open(html_filename, 'w', encoding='utf-8') as f:
        # Escribir encabezado basico
        escribir_encabezado_html(f, bloque_id=1)
        agregar_busqueda_y_script(f)

        # Agregar indice con enlaces a las graficas
        f.write('<h1>Indice de Graficas</h1>\n')
        f.write('<ul style="columns: 5; list-style-type: none; padding: 0;">\n')  # Usamos columns para dividir en 5 columnas
        
        # Crear un indice con las graficas distribuidas en 5 columnas
        for i, fig in enumerate(figs):
            f.write(f'<li><a href="#grafico{i}">{fig.layout.title.text}</a></li>\n')
        
        f.write('</ul>\n')

        # Agregar la tabla general con todos los datos
        f.write('<h1>Informacion Financiera</h1>\n')
        crear_tabla_general(df, f)

        # Guardar las graficas con titulos y navegacion
        f.write('<h1>Graficas de Precios Historicos</h1>\n')
        for i, fig in enumerate(figs):
            f.write(f'<h2 id="grafico{i}">{fig.layout.title.text}</h2>\n')  # Titulo con ID
            f.write(fig.to_html(full_html=False, include_plotlyjs="cdn"))
            f.write('<br><br>\n')
            agregar_vinculo_volver_inicio(f)

        f.write('</body></html>\n')

    print(f"Las tablas y graficas han sido guardadas en {html_filename}")



def escribir_encabezado_html(f, bloque_id):
    """Escribe el encabezado basico del archivo HTML con estilo."""
    encabezado_html = f'''
    <h1>Informacion Financiera - Bloque {bloque_id}</h1>
    <html><head><style>
        table {{border-collapse: collapse; width: 100%;}} 
        th, td {{border: 1px solid black; padding: 5px;}} 
        th {{background-color: #f2f2f2;}} 
        a {{color: blue; text-decoration: none; font-weight: bold;}}
    </style></head><body id="top">
    '''
    f.write(encabezado_html)

def agregar_busqueda_y_script(f):
    """Agrega el campo de busqueda y el script para ordenar y filtrar las tablas."""
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
            // Inicializamos el estado del orden en ascendente
            let sortOrder = true;

            header.addEventListener('click', function () {
                sortTable(table, index, sortOrder);
                // Alternamos el orden para la proxima vez
                sortOrder = !sortOrder;
            });
        });
    });

    function sortTable(table, colIndex, ascending) {
        const rows = Array.from(table.rows).slice(1); // Excluir la fila de los encabezados

        // Ordenar las filas usando la funcion de comparacion optimizada
        rows.sort(function (rowA, rowB) {
            const cellA = rowA.cells[colIndex].textContent.trim();
            const cellB = rowB.cells[colIndex].textContent.trim();

            const valueA = parseValue(cellA);
            const valueB = parseValue(cellB);

            if (!isNaN(valueA) && !isNaN(valueB)) {
                // Orden numerico
                return ascending ? valueA - valueB : valueB - valueA;
            } else {
                // Orden alfabetico
                return ascending ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
            }
        });

        // Usar documentFragment para manipular el DOM de manera eficiente
        const fragment = document.createDocumentFragment();
        rows.forEach(function (row) {
            fragment.appendChild(row); // Agregar filas al fragmento
        });

        // Añadir todas las filas reordenadas de una vez al DOM
        table.appendChild(fragment);
    }

    function parseValue(value) {
        // Eliminar comas y convertir a float
        return parseFloat(value.replace(/,/g, '').replace('%', '').trim());
    }

    window.filterTable = function () {
        const input = document.getElementById("search");
        const filter = input.value.toLowerCase();
        const rows = document.querySelectorAll("table tr");

        rows.forEach(function (row, index) {
            if (index === 0) return;  // Ignorar la primera fila (encabezados)

            const cells = row.querySelectorAll("td");
            let found = false;

            cells.forEach(function (cell) {
                if (cell.textContent.toLowerCase().includes(filter)) {
                    found = true;
                }
            });

            row.style.display = found ? "" : "none";
        });
    };

    // Funcion para copiar la tabla al portapapeles
    window.copyTableToClipboard = function (tableId) {
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

def agregar_vinculo_volver_inicio(f):
    """Agrega un enlace para volver al inicio de la pagina."""
    f.write('<br><a href="#top">Volver al inicio</a><br><br>')



# Procesar tickers y generar archivo HTML
figs = []
index_id = 0
total_tasks = len(tickers)
current_task = 0

for ticker in tickers:
    for periodo, intervalo in [("1mo", "1h")]:  # Ejemplo de intervalo
        data, weekend_jumps = obtener_datos(ticker, periodo, intervalo)
        if data is not None:
            # Crear grafico
            fig = crear_grafica(data, weekend_jumps, periodo, intervalo, ticker, index_id)
            figs.append(fig)
            index_id += 1
        current_task += 1
        print_progress_bar(current_task, total_tasks)

# Crear DataFrame con la informacion financiera
financial_data = get_financial_info(tickers)
df_financial_data = pd.DataFrame(financial_data)

# Guardar tablas y graficas en HTML
html_filename = "grafico_precios_historicos.html"
guardar_graficas_html(html_filename, *figs, df=df_financial_data)

print("\nProcesamiento completado.")
