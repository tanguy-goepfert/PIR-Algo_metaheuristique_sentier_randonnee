import math
import statistics
from initialisation_jeu_de_trace import *
from modification_reseau import *
import numpy as np
     
def ecart_traces(trace1, trace2):
    x1 = trace1.getX()
    y1 = trace1.getY()

    x2 = trace2.getX()
    y2 = trace2.getY()

    distances = []

    # Pour chaque point on va chercher le point du reseau le plus proche 
    for i in range(len(x1)):
        d_min = float("inf")

        for j in range(len(x2)):
            d = math.sqrt(
                (x1[i] - x2[j])**2
                + (y1[i] - y2[j])**2
            )

            if d < d_min:
                d_min = d

        distances.append(d_min)

    moyenne = statistics.mean(distances)
    ecart_type = statistics.pstdev(distances)

    return moyenne, ecart_type
        

# def comparer_toutes_traces(gps_tracks):
#     resultats = []
#     n = len(gps_tracks)

#     for i in range(n):
#         trace1 = gps_tracks.getTrack(i)

#         for j in range(i + 1, n):
#             trace2 = gps_tracks.getTrack(j)

#             # Calcul dans les deux sens pour une mesure symétrique
#             d1 = ecart_traces(trace1, trace2)
#             d2 = ecart_traces(trace2, trace1)

#             ecart = (d1 + d2) / 2

#             resultats.append((i, j, ecart))

#     return resultats


# #fonctions qui augmentent quand on dépasse d'un nombre nmax d'objet dans le reseau
# def maximum_arcs(reseau,gps_tracks,nmax=500): #assez limitant à voir plus tard
#     return max(0,len(reseau)-nmax) # a multiplier par un facteur selon le reste

# def maximum_vertex(reseau,gps_tracks,nmax=10000): #assez limitant à voir plus tard
#     compteur=0
#     n=len(reseau)
#     track=[]
#     for i in range(n):
#         track=reseau.getTrack(i)
#         compteur+=len(track.getX())
#     return max(0,compteur - nmax(10000)) # a multiplier par un facteur selon le reste


def objectif(reseau, gps_tracks) :
    n = len(gps_tracks)
    m = len(reseau)
    print(n,m)
    print("Nombre de comparaisons :", n*m)

    scores = []
    for i in range(n):
        print("i : ", i)
        trace_i = gps_tracks.getTrack(i)

        for j in range(m):
            arc_j = reseau.getTrack(j)

            # Calcul dans les deux sens pour une mesure symétrique
            d1 = ecart_traces(trace_i, arc_j)[1]
            d2 = ecart_traces(arc_j, trace_i)[1]
            ecart = (d1 + d2) / 2
            scores.append(ecart)
    return np.mean(scores)




    




if __name__ == "__main__" :

    # ----------------------------------------------------------
    # Generer les traces
    # ----------------------------------------------------------

    tkl.seed(110) #bloque l'aléatoire
    tracks = traces_random(nb=2, sinuosite=0.1)


    # ----------------------------------------------------------
    # Bruitage 
    # ----------------------------------------------------------

    gps_tracks = bruitage(tracks, 10)


    # ----------------------------------------------------------
    # Generer le réseau
    # ----------------------------------------------------------

    reseau = random_tirage_track(gps_tracks, nbre_arcs=2)


    # ----------------------------------------------------------
    # Affichage
    # ----------------------------------------------------------

    plt.figure(figsize=(8, 6))

    # Affichage des traces
    for t in gps_tracks:
        plt.plot(t.getX(), t.getY(), linewidth=0.7, color='blue')
    
    # Reseau par dessus
    for t in reseau:
        plt.plot(t.getX(), t.getY(), linewidth=1, color='red')

    
    # -----------------------------------------------------------
    # Fonction objectif
    # -----------------------------------------------------------
    
    resultat = objectif(reseau, gps_tracks)

    print("RESULTAT : ", resultat)

    
    



    plt.show()
    
