from bs4 import BeautifulSoup
import requests
import sqlite3

# crear una base de datos en sqlite3

def create_db():
    conn = sqlite3.connect('titulares.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS titulares
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                pagina text,
                palabra text,
                repeticiones int
                )''')
    conn.commit()
    conn.close()

# insertar datos en la base de datos

def insert_db(pagina, palabra, repeticiones):
    conn = sqlite3.connect('titulares.db')
    c = conn.cursor()
    c.execute('''INSERT INTO titulares
                (pagina, palabra, repeticiones)
                VALUES (?, ?, ?)''', (pagina, palabra, repeticiones))
    conn.commit()
    conn.close()

def get_titular(url, values) -> list:
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

    titulares = []
    tag_html, p1, p2 = values
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.find_all(tag_html, attrs={p1: p2})
    for tag in tags:
        titulares.append(tag.text)

    return titulares

# pagina, palabra buscada, coincidencia

def find_word(string, titular):
    return string.lower() in titular.lower()

def main():
    string = input('Ingresa la palabra a buscar: ')

    create_db()

    # (tag_html, attrs={p1: p2})
    urls = {
       'https://eluniversal.com.mx': ('a', 'data-cta', True),
       # 'https://edition.cnn.com/': ('span', 'class', 'container__headline-text'),
       'https://www.elsoldemexico.com.mx': ('h4', 'class', 'title'),
       'https://www.milenio.com/': ('a', 'class', 'board-module__a'),
       'https://www.excelsior.com.mx/': ('h2', 'class', 'card-title'),
    }

    for url, values in urls.items():
        titulares = get_titular(url, values)
        count_titulares = len(titulares)
        count_coincidences = 0
        
        print(f'Pagina: {url}')
        print(f'Hay {count_titulares} titulares')
        for titular in titulares:
            if find_word(string, titular):
                count_coincidences += 1
                print(titular)    

        print(f'Hay {count_coincidences} coincidencias')

        insert_db(url, string, count_coincidences)

if __name__ == "__main__":
    main()
