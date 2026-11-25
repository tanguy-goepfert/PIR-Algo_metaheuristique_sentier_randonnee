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
import time

#%% fonctions


def init_affichage(reseau, traces):
    global fig, ax, ligne_interactive
    plt.ion()
    fig, ax = plt.subplots()
    # Afficher le réseau
    for arc in reseau:
        plt.plot(arc.getX(), arc.getY(), linewidth=1, color='red')
    # Afficher les traces
    for trace in traces:
        plt.plot(trace.getX(), trace.getY(), linewidth=0.5, color='black')
    (ligne_interactive,) = ax.plot([], [])


def afficher(arc, iteration, cout, temperature, pause=0.05):
    # A faire : afficher tous les arcs du réseau
    xs, ys = arc.getX(), arc.getY()  # sépare les x et les y
    
    ligne_interactive.set_data(xs, ys)
    ax.set_title(f"Itération {iteration}, cout : {cout}, T : {round(temperature, 3)}")   # mise à jour du titre
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()
    plt.pause(pause)



def T0_choix_delta(reseau, indices_actions, prob_perturbations, perturbations, traces):
    """
    Mesure la moyenne des degradations de cout sur 100 itérations du RJMCMC
    """
 
    liste_delta=[]
    for i in range(100):
        print("itération calcul d0", i)
        #tirage_au_sort, d'une des perturbations avec la loi de probabilite 
        #en entree
        action=random.choices(indices_actions,prob_perturbations)[0]
        #saut
        reseau_potentiel=reseau.copy()
        perturbations[action](reseau_potentiel,traces)
        #evaluation : si on minimise la fonction cout, on accepte, sinon on
        #tire au sort avec proba cout(i)/cout(i+1 potentiel)
        ecart_cout = objectif(reseau=reseau_potentiel,gps_tracks=traces)-objectif(reseau=reseau,gps_tracks=traces)
        print("ecart_cout= ", ecart_cout)
        if ecart_cout > 0 :
            liste_delta.append(ecart_cout)
    delta=np.mean(liste_delta)
    print("delta=",delta)
    return delta

def T0_choix_alpha(delta=10, p0=0.8, T_final=0.01, duree_palier=100, N=20000):
    """
        Parameters
        ----------
        delta : TYPE int
            DESCRIPTION : Degradation à chaque itération du RJMCMC
        p0 : TYPE float
                    DESCRIPTION : probabilité d'acceptation initiale
        T_final : TYPE float 
            DESCRIPTION : Température à la fin des itérations
        duree_palier : TYPE int
            DESCRIPTION : durée d'un palier --> nombre itération avant de changer d'un palier
            explorer.
        N : TYPE int 
            DESCRIPTION : Nombre d'itérations du RJMCMC
    
        Returns
        -------
        alpha : TYPE float
            DESCRIPTION : facteur de refroidissement par palier : plus alpha est grand, plus la descente est brutale
        """
    # Calcul T0
    T0 = -delta / np.log(p0)
    print("T0= ", T0)
    # Calcul alpha
    nb_palier = N // duree_palier
    alpha = (T0 / T_final) ** (1/nb_palier)
    print("alpha= ", alpha)
    return alpha

def temperature(i, delta=10, p0=0.8, alpha=2, duree_palier=100):
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
    duree_palier : TYPE integer
                DESCRIPTION : Nombre d'itération avant de changer de palier
    """
    T0 = -delta / np.log(p0)
    try:
        return T0 / (alpha ** (i // duree_palier))
    except :
        return 0

def RJMCMC_reseau_traces(r0,traces,perturbations,objectif,arret,prob_perturbations=[],plot=False, print_infos=True):
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
    plot : TYPE bool
            DESCRIPTION : affiche ou non l'évolution du réseau

    Returns
    -------
    etats : TYPE : liste de reseaux
        DESCRIPTION : contient tous les sauts effectues par le RJMCMC (tires au
        au sort puis valides)
        
    suivi_sauts : TYPE : liste de couples d'entiers
        DESCRIPTION : la liste des couples (indice d'action et booleen d'acceptation) 
    """
    #initialisation
    t0=time.time()
    reseau = r0.copy()
    reseau_potentiel=reseau.copy()
    action=-1 #memoire de l'indice de la perturbation selectionnee par tirage au sort
    indices_actions=list(range(len(perturbations))) 

    if prob_perturbations==[]: #equiprobatilite
        prob_perturbations = np.ones(len(perturbations))/len(perturbations)
    
    # Calcul initialisation température
    d0 = T0_choix_delta(reseau, indices_actions, prob_perturbations, perturbations, traces)
    alpha = T0_choix_alpha(delta=d0, p0=0.8, T_final=0.01, duree_palier=100, N=20000)

    # Affichage
    if plot == True:
        init_affichage(reseau, traces)

    
    
    for i in range(arret):
        print("itération rjmcmc", i)
        ti=time.time()
        print('temps_calcul = ', ti-t0)
        #tirage_au_sort, d'une des perturbations avec la loi de probabilite 
        #en entree
        action=random.choices(indices_actions,prob_perturbations)[0]
        #saut
        reseau_potentiel=reseau.copy()
        perturbations[action](reseau_potentiel,traces)
        #evaluation : si on minimise la fonction cout, on accepte, sinon on
        #tire au sort avec proba cout(i)/cout(i+1 potentiel)

        temp = temperature(i, delta=d0, alpha=alpha, duree_palier=100)

        cout_actuel = objectif(reseau=reseau, gps_tracks=traces, print_infos=False)
        cout_potentiel = objectif(reseau=reseau_potentiel, gps_tracks=traces, print_infos=False)
        
        rapport =  min(1,np.exp(
                            -(cout_potentiel-cout_actuel)
                            /temp 
                            ))

        k = random.random()

        if print_infos==True:
            print("Cout actuel = ", cout_actuel)
            print("Cout potentiel = ", cout_potentiel)
            print("Rapport = ", rapport)
            print("k = ", k)
            print("Température = ", temp)


        if rapport == 1 :
            reseau=reseau_potentiel
            print("OK")
            # Affichage
            if plot == True:
                afficher(reseau[0], iteration=i, cout=cout_actuel, temperature=temp)
        elif k <= rapport :
            reseau=reseau_potentiel
            print("BOF MAIS OK")
        else :
            print("NON")
        print()

    if plot == True:
        plt.ioff()
        plt.show()

    tf=time.time()
    print("temps de calcul final = ",tf-t0)    
    return reseau


if __name__=="__main__" :

    # ### Generer les traces GPS
    # tkl.seed(110) #bloque l'aléatoire
    # tracks = traces_random(nb=2, sinuosite=0.1)
    # # Bruitage 
    # gps_tracks = bruitage(tracks, 5)

    ### Initialisation d'un premier réseau 
    tkl.seed(2)
    reseau = traces_random(nb=1, sinuosite=0.5)
    reseau[0].resample(npts=25)
    afficher(reseau[0], pause=0.05)
    # reseau[1].resample(npts=50)
    
    # for i in reseau:
    #     print(len(i))
    # ### Affichage
    # plt.figure(figsize=(8, 6))

    # # Affichage des traces
    # for t in gps_tracks:
    #     plt.plot(t.getX(), t.getY(), linewidth=2, color='black')
    
    # # Reseau par dessus
    # for t in reseau:
    #     plt.plot(t.getX(), t.getY(), linewidth=1, color='blue')




    # ### RJMCMC
    
    # actions = [deplacer_vertex_prox]
    
    # solution = RJMCMC_reseau_traces(r0=reseau, traces=gps_tracks, perturbations=actions, objectif=objectif, arret=100)
    # print("Score initial : ", objectif(reseau=reseau,gps_tracks= gps_tracks))
    # print("Score solution : ", objectif(reseau = solution, gps_tracks= gps_tracks))

    # # Affichage solution
    # for s in solution:
    #     plt.plot(s.getX(), s.getY(), linewidth=1, color='red')
    # plt.show()
