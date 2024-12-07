from points import Point
from random import randint
from typing import Callable
from math import sqrt

def shuffled(t:list):
    l = t.copy()
    n = len(l)
    for i in range(n):
        r = randint(i, n-1)
        l[i],l[r] = (l[r], l[i])
    return l


def clusters_atlagos_abszolut_eltereseinek_osszege(clusters:dict, px:Callable, py:Callable):
    return sum(cluster_centroid_koruli_atlagos_abszolut_elterese(centroid, clusters[centroid], px, py) for centroid in clusters.keys())

def jobb_clusters(clusters1:dict, clusters2:dict, px:Callable, py:Callable):
    return clusters_atlagos_abszolut_eltereseinek_osszege(clusters1, px, py) > clusters_atlagos_abszolut_eltereseinek_osszege(clusters1, px, py)

def pont_rekord_tav_2D(p:Point, r, px:Callable, py:Callable) -> float:
    return sqrt((p.x-px(r))**2 + (p.y-py(r))**2)

def cluster_centroid_koruli_atlagos_abszolut_elterese(centroid:Point, cluster:list, px:Callable, py:Callable):
    return atlag([pont_rekord_tav_2D(centroid, rekord, px, py) for rekord in cluster])

def random_kivalaszt_visszateves_nelkul(table:list, K:int):
    return shuffled(table)[0:K]

def clustering_2d_with_random(K, table, nev, px, py):
    centroid_rekordok = random_kivalaszt_visszateves_nelkul(table, K)
    centroids = [Point(nev(crekord), px(crekord), py(crekord)) for crekord in centroid_rekordok]
    return clustering_2d(centroids, table, nev, px, py)

def best_clustering_2d(N:int, K:int, table:list, nev: Callable, px:Callable, py:Callable):
    best_clusters, best_sum_of_distances = clustering_2d_with_random(K, table, nev, px, py)
    print(f'az {0}. próbálkozásban a távolságok összege {best_sum_of_distances} lett')
    for i in range(N-1):
        clusters, sum_of_distances = clustering_2d_with_random(K, table, nev, px, py)
        print(f'az {i+1}. próbálkozásban a távolságok összege {sum_of_distances} lett')
        if best_sum_of_distances > sum_of_distances:
            print(f'Ez jobb, mint a {best_sum_of_distances}, így cserélem')
            best_clusters = clusters
            best_sum_of_distances = sum_of_distances
    return best_clusters, sum_of_distances

def best_clustering_2d_for_elbow(N:int, K:int, table:list, nev: Callable, px:Callable, py:Callable) -> tuple[dict, list[float]]:
    clusters_lista = [None]*K
    sum_of_distances_lista = [None]*K
    for k in range(2,K):
        print(f'---- K = {k} ----')
        clusters, sum_of_distances = best_clustering_2d(N, k, table, nev, px, py)
        clusters_lista[k] = (clusters)
        sum_of_distances_lista[k] = (sum_of_distances)

    return clusters_lista, sum_of_distances_lista




def clustering_2d(regi_centroidok:list[Point], table:list, nev: Callable, px:Callable, py:Callable):
    vege = False
    while not vege:
        # clusterek inicializálása a centroidok körül
        clusters = {}
        for centroid in regi_centroidok:
            clusters[centroid] = set()

        # pontok clusterekbe sorolása
        for rekord in table:
            legkozelebbi_centroid = get_legkozelebbi_centroid([(centroid, pont_rekord_tav_2D(centroid,rekord,px,py)) for centroid in clusters.keys()])
            clusters[legkozelebbi_centroid].add(rekord)

        #centroidok újraszámolása
        uj_centroidok = clusterek_sulypontjai(clusters, px, py)

        vege = ponthalmaz(uj_centroidok,3) == ponthalmaz(regi_centroidok,3)
        regi_centroidok = uj_centroidok
    return (clusters, sum([sum_of_distances(clusters, centroid, px, py) for centroid in clusters.keys()]))

def sum_of_distances(clusters, centroid:Point, px:Callable, py:Callable) -> float:
     return sum([pont_rekord_tav_2D(centroid, rekord, px, py) for rekord in clusters[centroid]])

def ponthalmaz(centroidok, pontossag:int):
    return {(round(centroid.x,pontossag), round(centroid.y,pontossag)) for centroid in centroidok}

def clusterek_sulypontjai(clusters:dict, px:Callable, py:Callable):
    return [Point(f'm{centroid.nev}', rekordok_atlaga(clusters[centroid], px), rekordok_atlaga(clusters[centroid], py)) for centroid in clusters.keys()]

def rekordok_atlaga(cluster, p:Callable):
    return atlag([ p(rekord) for rekord in cluster])

def atlag(t):
    return sum(t)/len(t)

def get_legkozelebbi_centroid(centroid_tavok):
    best_centroid = centroid_tavok[0][0]
    best_tav = centroid_tavok[0][1]
    # print(f'eleinte: \n best_centroid: {best_centroid}\n best_tav: {best_tav}')
    for centroid, tavolsag in centroid_tavok:
        if tavolsag < best_tav:
            best_centroid = centroid
            best_tav = tavolsag
    return best_centroid

# TikZ-szel kapcsolatos kiírások

def tikz_elbow(sum_of_distances_lista:list[float], fajlnev:str):
    nonementes = [elem for elem in sum_of_distances_lista if elem]
    print(nonementes)
    maksz = max(nonementes)
    K = len(nonementes)
    s = r'\begin{tikzpicture}[pont/.style={fill = black}]'
    s += f'\n\\pgfmathsetmacro{{\\K}}{{{K}}}\n'
    s += f'\n\\draw[step=1.0] (0,0) grid ({K},{str(maksz+1)});'
    for k in range(2,K):
        s+=f'\n\\node[pont](n{k}) at ({k}, {sum_of_distances_lista[k]}){{}};'
    s+= f'\n\\foreach \\k in {{1,2,...,{K}}}{{\n \\node[] at(\k, -.25){{\k}};}}'
    s+=r'\n\end{tikzpicture}'
    open(fajlnev, 'w', encoding='utf-8').write(s)


def centroid_to_tikzname(centroid:Point):
    return 'c' + centroid.nev.replace('m', '')

def rekord_to_tikz(rekord, centroid:Point, tikzlabel:Callable, tikznev:Callable, tikzszoveg:Callable, px:Callable, py:Callable):
    return f'\t\\node[rekord, {centroid_to_tikzname(centroid)} {tikzlabel(rekord)}]({tikznev(rekord)}) at ({px(rekord)},{py(rekord)}){{}};%{tikzszoveg(rekord)}\n'

def point_to_tikz(p:Point):
    return f'\t\\node[pont]({p.nev}) at ({p.x},{p.y}){{}};\n'

def clusters_to_tikz(clusters:dict, tikzlabel:Callable, tikznev:Callable, tikzszoveg:Callable, px:Callable, py:Callable) -> str:
    clusterstilusok = ''

    szin = ['red','green','blue','cyan','magenta','yellow','black', 'white','gray','white','darkgray','lightgray','brown','lime','olive','orange','pink','purple','teal','violet', ]

    clusterstilusok = ',\n'.join([ f'{centroid_to_tikzname(centroid)}/.style={{fill={szin[i]}}}' for i, centroid in enumerate(clusters.keys())])

    s = '''\\begin{tikzpicture}[
pont/.style={fill = black},
rekord/.style={circle, draw=black},
''' + clusterstilusok +'\n]'

    for centroid in clusters.keys():
        for rekord in clusters[centroid]:
            s += rekord_to_tikz(rekord, centroid, tikzlabel, tikznev, tikzszoveg, px, py)
    for centroid in clusters.keys():
        s += point_to_tikz(centroid)
    
    return s+r'\end{tikzpicture}'

