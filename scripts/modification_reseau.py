from initialisation_jeu_de_trace import *
import math

# Génération aléatoire indépendante
rng = random.Random()

def random_tirage_track(tracks, nbre_arcs=2): 
    """
    Tire des traces au hasard dans un jeu de données de trace GPS. Cette fonction sert a initialiser le réseau qu'on va faire évoluer. 
    tracks --> traces GPS en entrée
    nbre_arcs --> estimation du nombre d'arc du réseau final
    """

    nbre = math.ceil(nbre_arcs * math.log(nbre_arcs)) # Nombre de traces a piocher dans le jeu de traces GPS (nlogn, collectionneur de timbre)
    tkl.seed(150)
    indices = rng.sample(range(nbre_arcs), nbre)

    var_traces = []
    for i in indices:
        trace = tracks.getTrack(i)
        var_traces.append(trace)

    liste_traces = tkl.core.TrackCollection(var_traces)
    return liste_traces

def ajouter_arc(reseau, tracks):
    """
    Ajoute un arc a un réseau d'arcs. 
    L'arc peut être un trait tiré aléatoirement dans l'espace (99% de chance) ou une trace récupéré dans le jeu de traces GPS initiales (1% de chance)
    """

    # Tirage du type d'action a faire : 99% tirer un trait droit, 1% tirer une trace dans le jeu de trace initial.
    r = rng.randint(0, 100)
    print(r)
    # r = 99
    if r == 99 :
        new_arc = rng.choice(tracks)
    else :
        p1 = tkl.ENUCoords(rng.randint(0, 100), rng.randint(0, 100),  0.0)
        p2 = tkl.ENUCoords(rng.randint(0, 100), rng.randint(0, 100),  0.0)
        o1 = tkl.Obs(p1)
        o2 = tkl.Obs(p2)
        new_arc = tkl.Track([o1, o2])
    reseau.addTrack(new_arc)

def supprimer_arc(reseau):
    """
    Supprime aléatoirement un arc du réseau. 
    """
    r = rng.randint(0, len(reseau) - 1) # Indice aléatoire de la trace à supprimer
    trace_a_sup = reseau.getTrack(r)
    reseau.removeTrack(trace_a_sup)




def supprimer_vertex(trace, debut, fin):
    """
    Supprime un arc d'une trace GPS.
    L'arc correspond aux observations entre debut et fin inclus.
    """

    if debut < 0 or fin >= trace.size() or debut > fin:
        print("Indices invalides")
        return trace

    observations = trace.getObsList()

    # Conserver les observations avant et après l'arc
    nouvelles_observations = (
        observations[:debut] + observations[fin + 1:]
    )

    trace.setObsList(nouvelles_observations)

    return trace

def deplacer_vertex(trace, indice, nouveau_x, nouveau_y):
    """
    Déplace un point de la trace GPS.
    """

    if indice < 0 or indice >= trace.size():
        print("Indice invalide")
        return trace

    # Récupérer le point à déplacer
    observation = trace.getObs(indice)

    # Modifier ses coordonnées
    observation.position.setX(nouveau_x)
    observation.position.setY(nouveau_y)

    # Réinsérer l'observation modifiée dans la trace
    trace.setObs(indice, observation)

    return trace

if __name__ == "__main__" :

    ### Generer les traces GPS
    tkl.seed(110) #bloque l'aléatoire
    tracks = traces_random(2, 0.1)
    # Bruitage 
    gps_tracks = bruitage(tracks, 10)

    # Affichage des traces GPS
    plt.figure(figsize=(8, 6))
    # for t in gps_tracks:
    #     plt.plot(t.getX(), t.getY(), linewidth=0.7, alpha=0.5)


    ### Initialisation d'un premier réseau 
    reseau = random_tirage_track(gps_tracks)
    # # Affichage
    # for r in reseau:
    #     plt.plot(r.getX(), r.getY(), linewidth=2, alpha=0.5, color='black')

    # # Ajout d'un arc
    # ajouter_arc(reseau, tracks)
    # # Affichage
    # for r in reseau:
    #     plt.plot(r.getX(), r.getY(), linewidth=2, alpha=0.5, color='green')

    # # Suppression d'un vertex
    # trace = reseau[0]
    # supprimer_vertex(trace, 2, 100)

    # Suppression d'un arc
    supprimer_arc(reseau)


    # Affichage
    for r in reseau:
        plt.plot(r.getX(), r.getY(), linewidth=2, alpha=0.5, color='red')
    plt.show()
