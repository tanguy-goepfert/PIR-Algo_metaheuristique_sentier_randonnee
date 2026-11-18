# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 2026

@author: thomas
"""
from modification_reseau import *
from initialisation_jeu_de_trace import *
from fonction_objectif import *
from RJMCMC import *


if __name__=="__main__":
    
    
    ### Generer les traces GPS
    tkl.seed(110) #bloque l'aléatoire
    tracks = traces_random(nb=2, sinuosite=0.1)
    # Bruitage 
    gps_tracks = bruitage(tracks, 5)

    ### Initialisation d'un premier réseau 
    tkl.seed(2)
    reseau = traces_random(nb=2, sinuosite=0.5)
    # Sous échantillonage
    reseau[0].resample(npts=50)
    reseau[1].resample(npts=50)



    ### Affichage
    plt.figure(figsize=(8, 6))

    # Affichage des traces
    for t in gps_tracks:
        plt.plot(t.getX(), t.getY(), linewidth=2, color='black')
    
    # Reseau par dessus
    for t in reseau:
        plt.plot(t.getX(), t.getY(), linewidth=1, color='blue')



    ### RJMCMC
    actions = [deplacer_vertex_prox]
    
    solution = RJMCMC_reseau_traces(r0=reseau, traces=gps_tracks, perturbations=actions, objectif=objectif, arret=100)
    print("Score initial : ", objectif(reseau=reseau, gps_tracks=gps_tracks))
    print("Score solution : ", objectif(reseau=solution, gps_tracks=gps_tracks))

    # Affichage solution
    for s in solution:
        plt.plot(s.getX(), s.getY(), linewidth=1, color='red')
    plt.show()
