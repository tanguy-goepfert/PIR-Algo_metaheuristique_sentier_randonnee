import math
import statistics
from initialisation_jeu_de_trace import *
from modification_reseau import *
import numpy as np
import time
     
def ecart_traces(trace1, trace2):
    """
    Distance de hausdorf
    """
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

    return np.max(distances), moyenne, ecart_type


def distance_hausdorff(trace1, trace2):
    """
    Calcule la distance de Hausdorff discrète entre deux lignes (ensembles de points)
    """
    # Passage des Tracks en lignes
    ligne1 = []
    ligne2 = []
    liste_coords_1 = trace1.getCoord()
    liste_coords_2 = trace2.getCoord()
    for coords in liste_coords_1 :
        ligne1.append([coords.getX(), coords.getY(), coords.getZ()])
    for coords in liste_coords_2 :
        ligne2.append([coords.getX(), coords.getY(), coords.getZ()])
    ligne1 = np.array(ligne1)
    ligne2 = np.array(ligne2)

    # Calcul de la matrice des distances euclidiennes entre chaque point de ligne1 et ligne2
    # ligne1: shape (N, D), ligne2: shape (M, D) (D -> dimension : 2 ou 3)
    diff = ligne1[:, np.newaxis, :] - ligne2[np.newaxis, :, :]
    dist_matrix = np.linalg.norm(diff, axis=-1)

    # Pour chaque point de ligne1, la plus petite distance vers ligne2
    d1 = np.min(dist_matrix, axis=1)
    # Pour chaque point de ligne2, la plus petite distance vers ligne1
    d2 = np.min(dist_matrix, axis=0)

    # Le maximum de ces minimums
    return max(np.max(d1), np.max(d2))

def distance_moyenne(trace1, trace2):
    """
    Calcule la distance de Hausdorff discrète entre deux lignes (ensembles de points)
    """
    # Passage des Tracks en lignes
    ligne1 = []
    ligne2 = []
    liste_coords_1 = trace1.getCoord()
    liste_coords_2 = trace2.getCoord()
    for coords in liste_coords_1 :
        ligne1.append([coords.getX(), coords.getY(), coords.getZ()])
    for coords in liste_coords_2 :
        ligne2.append([coords.getX(), coords.getY(), coords.getZ()])
    ligne1 = np.array(ligne1)
    ligne2 = np.array(ligne2)

    # Calcul de la matrice des distances euclidiennes entre chaque point de ligne1 et ligne2
    # ligne1: shape (N, D), ligne2: shape (M, D) (D -> dimension : 2 ou 3)
    diff = ligne1[:, np.newaxis, :] - ligne2[np.newaxis, :, :]
    dist_matrix = np.linalg.norm(diff, axis=-1)
    print(np.shape(dist_matrix))
    print(dist_matrix)

    # Pour chaque point de ligne1, la moyenne des distances vers ligne2
    d = np.mean(dist_matrix)
    return d




def objectif(reseau, gps_tracks) :
    """
    distance de hausdorf entre chaque arc et sa trace la plus "proche".
    return : moyenne des couts de chaque arc
    """
    m = len(gps_tracks)
    n = len(reseau)
    # print("Nombre de comparaisons :", n*m)

    couts = []
    for i in range(n): # Pour chaque arc du réseau
        # print("arc =", i)
        cout_i = math.inf
        arc_i = reseau.getTrack(i)


        for j in range(m): # Distance avec chaque trace
            # print("trace =", j)
            trace_j = gps_tracks.getTrack(j)

            # Calcul de la distance de hausdorf
            dH = distance_hausdorff(arc_i, trace_j)
            if cout_i > dH:
                cout_i = dH
        couts.append(cout_i)
        print(cout_i)

    # print(couts)
    for j in range(m): # Pour chaque trace
        # print("trace =", j)
        cout_j = math.inf
        trace_j = gps_tracks.getTrack(j)


        for i in range(n): # Pour chaque arc du réseau
            # print("arc =", i)
            arc_i = reseau.getTrack(i)

            # Calcul de la distance de hausdorf
            dH = distance_hausdorff(trace_j, arc_i)
            if cout_j > dH:
                cout_j = dH
        couts.append(cout_j)
        print(cout_j)

        
    # print(couts)
    cout = np.mean(couts)

     
    ### Intersection
    for i in range(n): # Pour chaque arc du réseau
        arc_i = reseau.getTrack(i)
        if tkl.util.intersects(arc_i, arc_i): # Autointersections
            cout += 10
        for j in range(m):
            if tkl.util.intersects(arc_i, arc_i): # Intersections
                cout += 10
    return cout










if __name__ == "__main__" :

    # ----------------------------------------------------------
    # Generer les traces
    # ----------------------------------------------------------

    tkl.seed(110) #bloque l'aléatoire
    tracks = traces_random(nb=2, sinuosite=0.1)


    # ----------------------------------------------------------
    # Bruitage 
    # ----------------------------------------------------------

    gps_tracks = bruitage(tracks, 5)


    # ----------------------------------------------------------
    # Generer le réseau
    # ----------------------------------------------------------

    # reseau = random_tirage_track(gps_tracks, nbre_arcs=2)
    tkl.seed(2)
    reseau = traces_random(nb=2, sinuosite=0.5)
    # reseau = tracks.copy() 
    # supprimer_arc(reseau)
    # ajouter_arc(reseau, tracks)


    # ----------------------------------------------------------
    # Affichage
    # ----------------------------------------------------------

    plt.figure(figsize=(8, 6))

    # Affichage des traces
    
    for t in tracks:
        plt.plot(t.getX(), t.getY(), linewidth=1, color='black')
    
    # Reseau par dessus
    for t in reseau:
        plt.plot(t.getX(), t.getY(), linewidth=2, color='blue')

    
    # -----------------------------------------------------------
    # Fonction objectif
    # -----------------------------------------------------------
    
    print("resultat obj ", objectif(reseau, gps_tracks))

    plt.show()
    
