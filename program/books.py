from datetime import date

class Book:
    def __init__(b, t) -> None:
        b.bookID = int(t[0])
        b.title = t[1]
        b.authors = [cella.strip() for cella in t[2].split('/')]
        b.average_rating = float(t[3])
        b.isbn = t[4]
        b.isbn13 = t[5]
        b.language_code = t[6]
        b.num_pages = int(t[7])
        b.ratings_count = int(t[8])
        b.text_reviews_count = int(t[9])
        honap, nap, ev = t[10].split('/')
        b.publication_date = date(int(ev), int(honap), int(nap))
        b.publisher = t[11]

    def __str__(b) -> str:
        return f'{", ".join(b.authors)}: {b.title}'

    def __repr__(b) -> str:
        return f'{", ".join(b.authors)}: {b.title}'

    def beolvas(fajlnev) -> list:
        lista = []
        with open(fajlnev, 'r', encoding="utf-8") as f:
            next(f)
            for sor in f:
                lista.append(Book([cella.strip() for cella in sor.split(',')]))
            return lista


