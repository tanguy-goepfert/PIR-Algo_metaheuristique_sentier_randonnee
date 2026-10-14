# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 2026

@author: Thomas Nguyen
"""

#%% imports
import numpy as np
import random

#%% fonctions

def RJMCMC(modele,perturbations,objectif,arret,prob_perturbations=[]):
    """
    Parameters
    ----------
    modele : TYPE : couple reseau et liste de traces
        DESCRIPTION : contient le réseau à l'état 0 et les traces sur 
        lesquelles il est construit.
    perturbations : TYPE liste de fonctions (reseau -> reseau)
        DESCRIPTION : une liste contenant la liste de toutes les actions à
        explorer.
    objectif : TYPE fonction (modele -> float)
        DESCRIPTION : Evalue la qualite d'un reseau (de l'état donné d'un modèle).
    arret : TYPE int
        DESCRIPTION : Le nombre de saut a effectuer 
        (changer en rayon de convergence ?)
        
    prob_perturbations : TYPE liste de float
        DESCRIPTION : contient les probabilites d'effectuer chaque action lors
        des sauts. (refaire la fonction avec proba variables ?)
        vide par defaut pour contenir une equiprobabilite

    Returns
    -------
    modele : TYPE : couple reseau et liste de traces
        DESCRIPTION : reseau apres le passage dans le RJMCMC

    """
    #initialisation
    reseau = modele[0]
    reseau_potentiel=modele[0]
    traces = modele[1]
    
    
    if prob_perturbations==[]: #equiprobatilite
        prob_perturbations = np.ones(len(perturbations))*1/len(perturbations)
    
    for i in range(arret):
        #tirage_au_sort
        action=random.choices(perturbations,prob_perturbations)
        #saut
        reseau_potentiel=action(reseau,traces)
        #evaluation
        if random.random()<=min(1,objectif(reseau_potentiel)/objectif(reseau)):
            reseau=reseau_potentiel
    
    return (reseau,traces)