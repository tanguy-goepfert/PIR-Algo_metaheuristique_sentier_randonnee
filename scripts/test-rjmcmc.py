# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 2026

@author: Thomas Nguyen
"""

#%% imports
import numpy as np
import random
from modification_reseau import *
from fonction_objectif import *

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
        DESCRIPTION : Evalue la qualite d'un reseau (de l'état donné d'un modèle)
        pour l'instant considéré comme 
    arret : TYPE int
        DESCRIPTION : Le nombre de saut a effectuer 
        (changer en rayon de convergence ?)
        
    prob_perturbations : TYPE liste de float
        DESCRIPTION : contient les probabilites d'effectuer chaque action lors
        des sauts. (refaire la fonction avec proba variables ?)
        vide par defaut pour contenir une equiprobabilite

    Returns
    -------
    etats : TYPE : liste de reseaux
        DESCRIPTION : contient tous les sauts effectues par le RJMCMC (tires au
        au sort puis valides)
        
    suivi_sauts : TYPE : liste de couples d'entiers
        DESCRIPTION : la liste des couples (indice d'action et booleen d'acceptation) 
    """
    #initialisation
    etats=[modele[0]] #la liste de tous les reseaux au fil des sauts
    traces = modele[1] #la liste des traces en entree
    action=-1 #memoire de l'indice de la perturbation selectionnee par tirage au sort
    accepte=-1 #memoire de l'acceptation du saut en cours
    indices_actions=list(range(len(perturbations))) 
    suivi_sauts=[(action,accepte)] #suivi des sauts effectues, (-1,-1) pour l'état initial

    if prob_perturbations==[]: #equiprobatilite
        prob_perturbations = np.ones(len(perturbations))/len(perturbations)
    for i in range(arret):
        print(i)
        #tirage_au_sort, d'une des perturbations avec la loi de probabilite 
        #en entree
        action=random.choices(indices_actions,prob_perturbations)[0]
        #saut
        reseau_potentiel=perturbations[action](etats[i],traces)
        #evaluation : si on minimise la fonction cout, on accepte, sinon on
        #tire au sort avec proba cout(i)/cout(i+1 potentiel)
        if random.random()<=objectif(etats[i],traces)/objectif(reseau_potentiel,traces):
            etats.append(reseau_potentiel)
            accepte=1
        else: #on garde l'etat precedent
            etats.append(etats[-1])
            accepte=0
        suivi_sauts.append((action,accepte))
        
    return etats,suivi_sauts


def temperature(i, delta=10, p0=0.5, alpha=2, palier=5):
    """
    Renvoie une température adaptée à une certaine itération du rjmcmc.
    ---------
    i : TYPE integer
            DESCRIPTION : iteration en question
    delta : TYPE integer
            DESCRIPTION : Dégradation (cout)
    p0 : TYPE float
            DESCRIPTION : probabilité d'acceptation initiale (plus p0 est proche de 1, plus T est grand (exploration forte)
    plus p0 est proche de 1, plus T₀ est grand (exploration forte).
    alpha : TYPE integer
                DESCRIPTION : facteur de refroidissement par palier : plus alpha est grand, plus la descente est brutale
    palier : TYPE integer
                DESCRIPTION : Nombre d'itération avant de changer de palier
    """
    T0 = -delta / np.log(p0)
    return T0 / (alpha ** (i // palier))



def RJMCMC_reseau_traces(r0,traces,perturbations,objectif,arret,prob_perturbations=[]):
    """
    Parameters
    ----------
    r0 : TYPE tracklib Trackcollection
        DESCRIPTION : reseau a l'etat initial
    traces : TYPE tracklib Trackcollection
        DESCRIPTION : traces a partir desquelles on veut construire le reseau
    perturbations : TYPE liste de fonctions (reseau -> reseau)
        DESCRIPTION : une liste contenant la liste de toutes les actions à
        explorer.
    objectif : TYPE fonction (modele -> float)
        DESCRIPTION : Evalue la qualite d'un reseau (de l'état donné d'un modèle)
        pour l'instant considéré comme 
    arret : TYPE int
        DESCRIPTION : Le nombre de saut a effectuer 
        (changer en rayon de convergence ?)
        
    prob_perturbations : TYPE liste de float
        DESCRIPTION : contient les probabilites d'effectuer chaque action lors
        des sauts. (refaire la fonction avec proba variables ?)
        vide par defaut pour contenir une equiprobabilite

    Returns
    -------
    etats : TYPE : liste de reseaux
        DESCRIPTION : contient tous les sauts effectues par le RJMCMC (tires au
        au sort puis valides)
        
    suivi_sauts : TYPE : liste de couples d'entiers
        DESCRIPTION : la liste des couples (indice d'action et booleen d'acceptation) 
    """
    #initialisation
    reseau = r0.copy()
    reseau_potentiel=reseau.copy()
    action=-1 #memoire de l'indice de la perturbation selectionnee par tirage au sort
    indices_actions=list(range(len(perturbations))) 

    if prob_perturbations==[]: #equiprobatilite
        prob_perturbations = np.ones(len(perturbations))/len(perturbations)
    for i in range(arret):
        print("itération rjmcmc", i)
        #tirage_au_sort, d'une des perturbations avec la loi de probabilite 
        #en entree
        action=random.choices(indices_actions,prob_perturbations)[0]
        #saut
        reseau_potentiel=reseau.copy()
        perturbations[action](reseau_potentiel,traces)
        #evaluation : si on minimise la fonction cout, on accepte, sinon on
        #tire au sort avec proba cout(i)/cout(i+1 potentiel)

        temp = temperature(i)
        
        rapport = min(1, 
                      np.exp(
                            -(objectif(reseau_potentiel,traces)-objectif(reseau,traces))
                            /temp 
                            ) 
                    )

        k = random.random()

        print("Cout actuel = ", objectif(reseau,traces))
        print("Cout potentiel = ", objectif(reseau_potentiel,traces))

        print("Rapport = ", rapport)
        print("k = ", k)
        print("Température = ", temp)


        if rapport == 1 :
            reseau=reseau_potentiel
            print("OK")
        elif k <= rapport :
            reseau=reseau_potentiel
            print("BOF MAIS OK")
        else :
            print("NON")
        print()
        
    return reseau


if __name__=="__main__" :

    ### Generer les traces GPS
    tkl.seed(110) #bloque l'aléatoire
    tracks = traces_random(nb=2, sinuosite=0.1)
    # Bruitage 
    gps_tracks = bruitage(tracks, 5)

    ### Initialisation d'un premier réseau 
    tkl.seed(2)
    reseau = traces_random(nb=2, sinuosite=0.5)

    ### Affichage
    plt.figure(figsize=(8, 6))

    # Affichage des traces
    for t in gps_tracks:
        plt.plot(t.getX(), t.getY(), linewidth=2, color='black')
    
    # Reseau par dessus
    for t in reseau:
        plt.plot(t.getX(), t.getY(), linewidth=1, color='blue')

    


    ### RJMCMC
    
    actions = [deplacer_vertex]
    
    solution = RJMCMC_reseau_traces(r0=reseau, traces=gps_tracks, perturbations=actions, objectif=objectif, arret=1000) #modèle : un compteur, perturbation +1 -1
    print("Score initial : ", objectif(reseau, gps_tracks))
    print("Score solution : ", objectif(solution, gps_tracks))

    # Affichage solution
    for s in solution:
        plt.plot(s.getX(), s.getY(), linewidth=1, color='red')
    plt.show()
