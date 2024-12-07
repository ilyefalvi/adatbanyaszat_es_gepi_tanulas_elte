from re import findall

class Point:
    def __init__(p, nev, x, y) -> None:
        p.nev = nev
        p.x = float(x)
        p.y = float(y)

    def __str__(p) -> str:
        return p.__repr__()

    def __repr__(p) -> str:
        return f'{p.nev}({p.x},{p.y})'
    

    def beolvas_tikz(fajlnev):
        szoveg = open(fajlnev, 'r', encoding='utf-8').read()
        matches = findall(r'\((a\d*?)\) at \((-?\d*\.?\d?),(-?\d*\.?\d?)\)', szoveg)
        
        lista = []
        for match in matches:
            lista.append(Point(match[0], match[1], match[2]))
        return lista
    
    