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
    
    tracks = traces_random(2, 0.1)
    gps_tracks = bruitage(tracks, 10)
    
    reseau = random_tirage_track(gps_tracks)
    
    perturbations = [ajouter_arc,supprimer_arc]
    
    test_rjmcmc=RJMCMC_reseau_traces(reseau,gps_tracks,perturbations,objectif,100)
    for r in test_rjmcmc:
        plt.plot(r.getX(), r.getY(), linewidth=2, alpha=0.5, color='red')
    plt.show()
