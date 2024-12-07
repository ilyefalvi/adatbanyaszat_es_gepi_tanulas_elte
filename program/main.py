from math import sqrt
from k_means_clustering import *
from books import Book
from points import Point
books = Book.beolvas('program/books.csv')
# pontok = Point.beolvas_tikz('program/test.tikz')
print(len(books))
# print(len(pontok))


# print('\n'.join([f'{i}. {b.average_rating} - {b.text_reviews_count}' for i,b in enumerate(books)]))
average_ratings = [b.average_rating*2 for i,b in enumerate(books)]
text_reviews_counts = [b.text_reviews_count/10000 for i,b in enumerate(books)]
ratings_counts = [b.ratings_count for i,b in enumerate(books)]

print(f'average ratings min: {min(average_ratings)}\naverage_rating max: {max(average_ratings)}\ntextreviews_count min: {min(text_reviews_counts)}\ntextreviews_count max: {max(text_reviews_counts)}\nratings_count min: {min(ratings_counts)}\nratings_count max: {max(ratings_counts)}\n')

# legjobb_clusters, legjobb_sum_of_distances = best_clustering_2d_for_elbow(
#     N = 20, 
#     K = 10, 
#     table = [book for book in books if book.ratings_count>1000], 
#     nev = lambda b: b.bookID, 
#     px = lambda b: b.average_rating*2, 
#     py = lambda b: b.text_reviews_count/10000, 
#     )


# tikz_elbow([s/200 if s else None for s in legjobb_sum_of_distances], 'elbow.tikz')


legjobb_clusters, legjobb_sum_of_distances = best_clustering_2d(
    N = 100, 
    K = 5, 
    table = [book for book in books if book.ratings_count>1000], 
    nev = lambda b: b.bookID, 
    px = lambda b: b.average_rating*2, 
    py = lambda b: b.text_reviews_count/10000, 
    )


# legjobb_clusters = best_clustering_2d(
#     N = 1, 
#     K = 2, 
#     table = pontok, 
#     nev = lambda p: p.nev, 
#     px = lambda p: p.x, 
#     py = lambda p: p.y, 
#     tav = lambda p,q: sqrt((p.x-q.x)**2+((p.y-q.y)**2))
#     )

# print(clusters_to_tikz(
#     clusters = legjobb_clusters, 
#     tikzlabel = lambda b: '',
#     tikznev = lambda b: '',
#     px = lambda b: b.average_rating*2, 
#     py = lambda b: b.text_reviews_count/10000, 
#     ))

with open('output.tikz', 'w', encoding='utf-8') as f:
    f.write(clusters_to_tikz(
    clusters = legjobb_clusters, 
    tikzlabel = lambda b: '',
    tikznev = lambda b: '',
    tikzszoveg= lambda b: b.bookID,
    px = lambda b: b.average_rating*2, 
    py = lambda b: b.text_reviews_count/10000, 
    ))