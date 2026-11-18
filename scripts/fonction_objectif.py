import math
import statistics
import numpy as np
import time
from shapely.geometry import LineString
from initialisation_jeu_de_trace import *
from modification_reseau import *



def distance_hausdorff(trace, arc):
    """
    Calcule la distance de Hausdorff discrète entre deux lignes (ensembles de points)
    """
    # Passage des Tracks en lignes
    ligne_trace = []
    ligne_arc = []
    liste_coords_trace = trace.getCoord()
    liste_coords_arc = arc.getCoord()
    for coords in liste_coords_trace :
        ligne_trace.append([coords.getX(), coords.getY(), coords.getZ()])
    for coords in liste_coords_arc :
        ligne_arc.append([coords.getX(), coords.getY(), coords.getZ()])
    ligne_trace = np.array(ligne_trace)
    ligne_arc = np.array(ligne_arc)

    # Calcul de la matrice des distances euclidiennes entre chaque point de ligne_trace et ligne_arc
    # ligne_trace: shape (N, D), ligne_arc: shape (M, D) (D -> dimension : 2 ou 3)
    diff = ligne_trace[:, np.newaxis, :] - ligne_arc[np.newaxis, :, :]
    dist_matrix = np.linalg.norm(diff, axis=-1)

    # # Pour chaque point de ligne_trace, la plus petite distance vers ligne_arc
    H12 = np.min(dist_matrix, axis=1)
    # Pour chaque point de ligne_arc, la plus petite distance vers ligne_trace
    H21 = np.min(dist_matrix, axis=0)

    # La somme des maximums de ces minimums
    return np.max(H12) + np.max(H21)

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

    # Pour chaque point de ligne1, la moyenne des distances vers ligne2
    d = np.mean(dist_matrix)
    return d

def autointersection(arc) :
    """
    Test si un arc s'autointersecte. True si auto intersection, False sinon
    """

    liste = []
    for i in range(len(arc)) :
        obs = arc.getObs(i)
        pos = (obs.position.getX(), obs.position.getY())
        liste.append(pos)

    poly = LineString(liste)
    intersection = not poly.is_simple
    if intersection : print("Intersection : ", intersection)
        
    return intersection




def objectif(gps_tracks, reseau) :
    """
    distance de hausdorf entre chaque arc et sa trace la plus "proche".
    return : moyenne des couts de chaque arc
    """
    n = len(gps_tracks)
    m = len(reseau)
    # print("Nombre de comparaisons :", n*m)

    H = []
    for i in range(n): # Pour chaque trace du réseau
        H_i = []
        trace_i = gps_tracks.getTrack(i)


        for j in range(m): # Distance avec chaque arc
            arc_j = reseau.getTrack(j)
            
            # Calcul de la distance de hausdorf
            H12 = distance_hausdorff(trace_i, arc_j)
            H_i.append(H12)

        # On garde la distance de Hausdorf min
        H_i_min = min(H_i)
        H.append(H_i_min)

    cout_H = np.mean(H)  

    # # print(couts)
    # for j in range(m): # Pour chaque trace
    #     # print("trace =", j)
    #     cout_j = math.inf
    #     trace_j = gps_tracks.getTrack(j)


    #     for i in range(n): # Pour chaque arc du réseau
    #         # print("arc =", i)
    #         arc_i = reseau.getTrack(i)

    #         # Calcul de la distance de hausdorf
    #         dH = distance_hausdorff(trace_j, arc_i)
    #         if cout_j > dH:
    #             cout_j = dH
    #     couts.append(cout_j)
    #     # print(cout_j)



    # ### Distance moyenne 
    # couts_M = []
    # for i in range(n): # Pour chaque arc du réseau
    #     # print("arc =", i)
    #     arc_i = reseau.getTrack(i)


    #     for j in range(m): # Distance avec chaque trace
    #         # print("trace =", j)
    #         trace_j = gps_tracks.getTrack(j)

    #         # Calcul de la distance moyenne
    #         dM = distance_moyenne(arc_i, trace_j)
    #         couts_M.append(dM)
    # cout_M = np.mean(couts_M)

     
    ### Intersection
    couts_I = 0
    for j in range(m): # Pour chaque arc
        arc_j = reseau.getTrack(j)
        if autointersection(arc_j): # Autointersections
            couts_I += 100
        for k in range(j): # Si l'arc intersecte un des arcs précédemment traités :
            arc_k = reseau.getTrack(k)
            if tkl.util.intersects(arc_j, arc_k): # Intersections avec d'autres arcs
                couts_I += 10

    cout = cout_H  + couts_I #+ cout_M
    
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

    gps_tracks = bruitage(tracks, 1)


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
    
