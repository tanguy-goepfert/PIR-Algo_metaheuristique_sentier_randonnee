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
    tracks = traces_random(nb=1, sinuosite=0.1)
    # Sous échantillonage
    tracks[0].resample(npts=30)

    # Bruitage 
    gps_tracks = bruitage(tracks, 3)

    ### Initialisation d'un premier réseau 
    tkl.seed(2)
    reseau = traces_random(nb=1, sinuosite=0.5)
    # Sous échantillonage
    reseau[0].resample(npts=12)



    ### Affichage
    plt.figure(figsize=(8, 6))

    # Affichage des traces
    for t in gps_tracks:
        plt.plot(t.getX(), t.getY(), linewidth=1, color='black')
    
    # Reseau par dessus
    for t in reseau:
        plt.plot(t.getX(), t.getY(), linewidth=3, color='blue')



    ### RJMCMC
    actions = [deplacer_vertex_prox]
    
    solution = RJMCMC_reseau_traces(r0=reseau, traces=gps_tracks, perturbations=actions, objectif=objectif, arret=10000, plot=False, print_infos=False)
    print("Score initial : ", objectif(reseau=reseau, gps_tracks=gps_tracks, print_infos=True))
    print("Score solution : ", objectif(reseau=solution, gps_tracks=gps_tracks, print_infos=True))

    # Affichage solution
    for s in solution:
        plt.plot(s.getX(), s.getY(), linewidth=2, color='red')
    plt.show()
