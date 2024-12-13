import pandas as pd
import yfinance as yf
import time

start_time = time.time()

print(f"Empezando en {time.time() - start_time:.2f}.")

# Leer los tickers desde el archivo
df=pd.read_csv("tickers/sp500x.txt")
tickers = df["0"].to_list()
#df = pd.read_csv('sp500.txt', delimiter='\t', on_bad_lines='skip')
#tickers = df["Symbol"].to_list()[:20]

inactive_tickers = pd.read_csv("tickers/inactive_tickers.txt")
in_tickers = inactive_tickers["0"].to_list()
tickers = [ticker for ticker in tickers if ticker not in in_tickers]


# Función para mostrar una barra de progreso
def mostrar_progreso(actual, total, largo_barra=30):
    progreso = actual / total
    longitud_completada = int(largo_barra * progreso)
    barra = "=" * longitud_completada + "-" * (largo_barra - longitud_completada)
    porcentaje = progreso * 100
    print(f"\r[{barra}] {porcentaje:.2f}%", end="", flush=True)

# Obtener información financiera junto con el sector con barra de progreso
def obtener_informacion_financiera(tickers):
    info_financiera = {}
    total_tickers = len(tickers)
    tickers_verificados = 0

    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
            if not info:
                raise ValueError("No data fetched")
            info_financiera[ticker] = {
                "Nombre": info.get("longName", "N/A"),
                "Sector": info.get("sector", "N/A"),
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
            pass  # Ignorar errores y continuar con el siguiente ticker

        tickers_verificados += 1
        mostrar_progreso(tickers_verificados, total_tickers)

    print()  # Salto de línea al terminar
    return info_financiera

# Función para dividir la lista de tickers en bloques
def dividir_tickers_en_bloques(tickers, tamano_bloque=100):
    """Divide una lista de tickers en bloques de un tamaño específico."""
    for i in range(0, len(tickers), tamano_bloque):
        yield tickers[i:i + tamano_bloque]

# FUNCIONES DE HTML #

def escribir_encabezado_html(f, bloque_id):
    """Escribe el encabezado básico del archivo HTML con estilo."""
    encabezado_html = f'''
    <h1>Información Financiera - Bloque {bloque_id}</h1>
    <html><head><style>
        table {{border-collapse: collapse; width: 100%;}} 
        th, td {{border: 1px solid black; padding: 5px;}} 
        th {{background-color: #f2f2f2;}} 
        a {{color: blue; text-decoration: none; font-weight: bold;}}
    </style></head><body id="top">
    '''
    f.write(encabezado_html)

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
                    // Inicializamos el estado del orden en ascendente
                    let sortOrder = true;
    
                    header.addEventListener('click', function () {
                        sortTable(table, index, sortOrder);
                        // Alternamos el orden para la próxima vez
                        sortOrder = !sortOrder;
                    });
                });
            });
    
            function sortTable(table, colIndex, ascending) {
                const rows = Array.from(table.rows).slice(1);
    
                rows.sort(function (rowA, rowB) {
                    const cellA = rowA.cells[colIndex].innerText.trim();
                    const cellB = rowB.cells[colIndex].innerText.trim();
    
                    const valueA = parseValue(cellA);
                    const valueB = parseValue(cellB);
    
                    if (!isNaN(valueA) && !isNaN(valueB)) {
                        // Orden numérico
                        return ascending ? valueA - valueB : valueB - valueA;
                    } else {
                        // Orden alfabético
                        return ascending ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
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

def agregar_vinculo_volver_inicio(f):
    """Agrega un enlace para volver al inicio de la página."""
    f.write('<br><a href="#top">Volver al inicio</a><br><br>')


# TERMINA FUNCIONES DE HTML

def generar_html_por_bloques(info_financiera, bloque_id):
    """Genera un archivo HTML para un bloque específico de tickers con un índice."""
    html_filename = f'informacion_financiera_bloque_{bloque_id}.html'
    sectores = {}

    # Agrupar por sector
    for ticker, data in info_financiera.items():
        sector = data.get("Sector", "N/A")
        if sector != "N/A":  # Omitir sectores "N/A"
            if sector not in sectores:
                sectores[sector] = []
            sectores[sector].append((ticker, data))

    with open(html_filename, 'w', encoding='utf-8') as f:
        # Escribir encabezado HTML
        escribir_encabezado_html(f, bloque_id)

        # Agregar campo de búsqueda y script
        agregar_busqueda_y_script(f)

        # Generar índice de sectores
        f.write('<h2>Índice de Sectores</h2><ul>')
        for sector in sectores.keys():
            f.write(f'<li><a href="#"{sector.replace(" ", "_")}">{sector}</a></li>')
        f.write('</ul>')

        # Crear una tabla por cada sector
        for sector, tickers in sectores.items():
            # Anclaje para cada sector
            f.write(f'<h2 id="{sector.replace(" ", "_")}">{sector} Sector</h2>')
            f.write(f'<button onclick="copyTableToClipboard(\'table_{sector.replace(" ", "_")}\')">Copiar tabla</button><br><br>')

            # Crear la tabla
            f.write(f'<table id="table_{sector.replace(" ", "_")}"><tr><th>Activo</th><th>Ticker</th>')

            # Agregar encabezados de información financiera
            financial_headers = ["P/E", "EPS", "BV", "Div Yld", "Div/Sh", "D/E", "Beta", "ROI", "ROE", "Vol"]
            for header in financial_headers:
                f.write(f'<th>{header}</th>')

            f.write('</tr>')

            # Agregar filas con información financiera
            for ticker, data in tickers:
                f.write(f'<tr><td>{data["Nombre"]}</td>')
                # Agregar hipervínculo para el ticker
                f.write(f'<td><a href="https://finance.yahoo.com/quote/{ticker}" target="_blank">{ticker}</a></td>')
                for key in financial_headers:
                    valor = data.get(key, 'N/A')
                    if valor != 'N/A':  # Omitir celdas con "N/A"
                        if isinstance(valor, (int, float)):  # Si el valor es numérico
                            f.write(f'<td>{valor:.2f}</td>')
                        else:  # Si el valor no es numérico
                            f.write(f'<td>{valor}</td>')
                    else:
                        f.write('<td></td>')  # Dejar la celda vacía
                f.write('</tr>')

            f.write('</table><br><br>')

            # Agregar el vínculo para volver al inicio
            agregar_vinculo_volver_inicio(f)

        f.write('</body></html>')

    print(f"Archivo generado: {html_filename}")

# Procesar la lista completa de tickers y exportar en bloques
def procesar_tickers_en_bloques(tickers, tamano_bloque=100):
    """Procesa tickers en bloques, obteniendo su información financiera y generando archivos HTML por bloque."""
    bloques = dividir_tickers_en_bloques(tickers, tamano_bloque)
    
    total_bloques = (len(tickers) + tamano_bloque - 1) // tamano_bloque
    for bloque_id, bloque in enumerate(bloques, start=1):
        print(f"\nProcesando bloque {bloque_id} de {total_bloques}...")
        info_financiera = obtener_informacion_financiera(bloque)
        generar_html_por_bloques(info_financiera, bloque_id)

# Ejemplo de uso
procesar_tickers_en_bloques(tickers, tamano_bloque=8000)

print(f"Codigo finalizado en {time.time() - start_time:.2f}.")
