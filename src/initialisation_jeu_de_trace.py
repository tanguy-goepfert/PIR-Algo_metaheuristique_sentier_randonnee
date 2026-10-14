import matplotlib.pyplot as plt
import tracklib as tkl
import numpy as np
import random
import datetime

def traces_random(nb, sinuosite=0.2):
    """
    Génère nb traces simulées de complexité paramétrable. Autrement dit, génère un réseau simple.
    :param nb : nombre des traces
    :type nb : int
    :param sinuosite : complexité de la trace. Proche de 0 : très complexe
    :type sinuosite : float
    """
    # Génèration des traces
    liste_traces = []
    for i in range(nb):
        # Liste d'observations
        trace = tkl.generate(sinuosite, dt=10)[::3]
        trace.scale(1)
        liste_traces.append(trace)
    tracks = tkl.core.TrackCollection(liste_traces)
    return tracks


def bruitage(tracks, N):
    # nombre de traces bruitées souhaitées
    gps_tracks = tkl.core.TrackCollection()
    for trace in tracks :
        traces_bruitees = tkl.core.TrackCollection([trace] * N)
        traces_bruitees.noise(2, tkl.ExponentialKernel(50))  # erreur GPS : 5 m, portée 20 m
        gps_tracks += traces_bruitees
    return gps_tracks
     
     
     



if __name__ == "__main__" :

    # ----------------------------------------------------------
    # Generer les traces
    # ----------------------------------------------------------

    tkl.seed(110) #bloque l'aléatoire
    tracks = traces_random(2, 0.1)


    # ----------------------------------------------------------
    # Bruitage 
    # ----------------------------------------------------------

    gps_tracks = bruitage(tracks, 10)


    # ----------------------------------------------------------
    # Manipulation
    # ----------------------------------------------------------
    for t in gps_tracks:
        print("Nouvelle trace")
        for obs in t.getObsList():
            plt.plot(t.getX(), t.getY(), 'k-', linewidth=2, label=f'originale')



    # ----------------------------------------------------------
    # Affichage
    # ----------------------------------------------------------

    plt.figure(figsize=(8, 6))

    # Affichage des traces
    for t in gps_tracks:
        plt.plot(t.getX(), t.getY(), linewidth=0.7, alpha=0.5)
    
    # Trace originale par dessus
    for t in tracks:
        plt.plot(t.getX(), t.getY(), 'k-', linewidth=2, label=f'originale')
        
    plt.axis('equal')
    plt.legend()
    plt.show()



