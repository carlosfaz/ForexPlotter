import requests
from bs4 import BeautifulSoup

# URL de la página
url = "https://eoddata.com/symbols.aspx"

# Realizar la solicitud HTTP para obtener el contenido de la página
response = requests.get(url)

# Comprobar si la solicitud fue exitosa
if response.status_code == 200:
    # Analizar el contenido de la página con BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Buscar la tabla que contiene los símbolos
    table = soup.find('table', {'class': 'data'})
    
    # Lista para almacenar los tickers
    tickers = []

    # Iterar sobre las filas de la tabla
    for row in table.find_all('tr')[1:]:  # Empezamos en la segunda fila para saltarnos los encabezados
        cols = row.find_all('td')
        if len(cols) > 1:
            ticker = cols[0].text.strip()  # Primer columna contiene el ticker
            tickers.append(ticker)

    # Imprimir los primeros 10 tickers obtenidos
    print(tickers[:10])

    # Exportar los tickers a un archivo de texto
    with open("tickers.txt", "w") as file:
        for ticker in tickers:
            file.write(f"{ticker}\n")

    print(f"Se han guardado {len(tickers)} tickers en 'tickers.txt'")

else:
    print(f"Error al obtener la página: {response.status_code}")

import requests
from bs4 import BeautifulSoup

# URL de la página
url = "https://eoddata.com/symbols.aspx"

# Realizar la solicitud HTTP para obtener el contenido de la página
response = requests.get(url)

# Comprobar si la solicitud fue exitosa
if response.status_code == 200:
    # Analizar el contenido de la página con BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Buscar la tabla que contiene los símbolos
    table = soup.find('table')  # Sin especificar la clase por ahora

    if table:
        # Lista para almacenar los tickers
        tickers = []

        # Iterar sobre las filas de la tabla
        for row in table.find_all('tr')[1:]:  # Empezamos en la segunda fila para saltarnos los encabezados
            cols = row.find_all('td')
            if len(cols) > 1:
                ticker = cols[0].text.strip()  # Primer columna contiene el ticker
                tickers.append(ticker)

        # Imprimir los primeros 10 tickers obtenidos
        print(tickers[:10])

        # Exportar los tickers a un archivo de texto
        with open("tickers.txt", "w") as file:
            for ticker in tickers:
                file.write(f"{ticker}\n")

        print(f"Se han guardado {len(tickers)} tickers en 'tickers.txt'")
    else:
        print("No se pudo encontrar la tabla de símbolos en la página.")
else:
    print(f"Error al obtener la página: {response.status_code}")

