from initialisation_jeu_de_trace import *
import math
import random
from scipy.spatial import cKDTree

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


def supprimer_arc(reseau, tracks):
    """
    Supprime aléatoirement un arc du réseau. 
    """
    r = rng.randint(0, len(reseau) - 1) # Indice aléatoire de l'arc à supprimer
    arc_a_sup = reseau.getTrack(r)
    reseau.removeTrack(arc_a_sup)



def supprimer_vertex(reseau, tracks):
    """
    Supprime un arc d'une trace GPS.
    L'arc correspond aux observations entre debut et fin inclus.
    """
    r = rng.randint(0, len(reseau) - 1)
    trace = reseau.getTrack(r) # Sélectionne une trace au hasard
    debut = rng.randint(0, len(trace) - 1)
    fin = rng.randint(debut, len(trace) - 1)
    print(len(trace))
    print(debut, fin)
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

def deplacer_vertex(reseau, tracks):
    """
    Déplace un point d'un arc du réseau
    """
    # Séléction de l'arc à modifier
    r = rng.randint(0, len(reseau) - 1) # Indice aléatoire de la trace à supprimer
    arc_a_modif = reseau.getTrack(r)

    # Supprimer l'ancien arc
    reseau.removeTrack(arc_a_modif)

    ### Modification de l'arc

    # Indice aléatoire du vertex à déplacer
    indice = rng.randint(0, len(arc_a_modif) - 1) 

    # Nouvelles coordonnées aléatoires
    bbox = tracks.bbox()
    nouveau_x = rng.uniform(bbox[0], bbox[1])
    nouveau_y = rng.uniform(bbox[2], bbox[3])

    if indice < 0 or indice >= arc_a_modif.size():
        print("Indice invalide")
        return False

    # Récupérer le point à déplacer
    observation = arc_a_modif.getObs(indice)

    # Modifier ses coordonnées
    observation.position.setX(nouveau_x)
    observation.position.setY(nouveau_y)

    # Réinsérer l'observation modifiée dans l'arc
    arc_a_modif.setObs(indice, observation)

    # Réinsérer l'arc dans réseau
    reseau.addTrack(arc_a_modif)

def deplacer_vertex_prox(reseau,tracks):
    """
    Déplace un point d'un arc du réseau
    """
    # Séléction de l'arc à modifier
    r = rng.randint(0, len(reseau) - 1) # Indice aléatoire de la trace à supprimer
    arc_a_modif = reseau.getTrack(r)

    # Supprimer l'ancien arc
    reseau.removeTrack(arc_a_modif)

    ### Modification de l'arc

    # Indice aléatoire du vertex à déplacer
    indice = rng.randint(0, len(arc_a_modif) - 1) 


    if indice < 0 or indice >= arc_a_modif.size():
        print("Indice invalide")
        return False

    # Récupérer le point à déplacer
    observation = arc_a_modif.getObs(indice)
    x=observation.position.getX()
    y=observation.position.getY()
    
    
    # Nouvelles coordonnées aléatoires
    nouveau_x = x + random.gauss()
    nouveau_y = y + random.gauss()

    # Modifier ses coordonnées
    observation.position.setX(nouveau_x)
    observation.position.setY(nouveau_y)

    # Réinsérer l'observation modifiée dans l'arc
    arc_a_modif.setObs(indice, observation)

    # Réinsérer l'arc dans réseau
    reseau.addTrack(arc_a_modif)

def detecter_points_proches(reseau, tracks):
    """
    Détecte les points appartenant à des traces différentes
    qui sont situés à une distance inférieure ou égale au seuil.

    Utilise un KDTree pour accélérer la recherche des points proches.

    Paramètres :
    reseau : collection de traces GPS
    tracks : collection de traces GPS initiales

    Retour :
    Liste de couples sous la forme :
    (indice_trace1, indice_point1, indice_trace2, indice_point2)
    """

    seuil = 15
    coordonnees = []
    indices_traces = []
    indices_points = []

    # Récupérer les coordonnées de toutes les traces
    for i, trace in enumerate(reseau):

        points = np.column_stack((trace.getX(), trace.getY()))

        for k in range(len(points)):

            coordonnees.append(points[k])
            indices_traces.append(i)
            indices_points.append(k)

    # Vérifier que le réseau contient des points
    if len(coordonnees) == 0:
        return []

    coordonnees = np.array(coordonnees)

    # Construire le KDTree à partir de toutes les coordonnées
    arbre = cKDTree(coordonnees)

    # Rechercher les couples de points situés à moins du seuil
    couples = arbre.query_pairs(r=seuil)

    points_proches = []

    # Parcourir les couples de points détectés
    for a, b in couples:

        # Récupérer les indices des traces
        i = indices_traces[a]
        j = indices_traces[b]

        # Ne comparer que des points appartenant à des traces différentes
        if i != j:

            # Récupérer les indices des points dans leurs traces respectives
            k = indices_points[a]
            l = indices_points[b]

            # Enregistrer les indices des deux traces et des deux points
            points_proches.append((i, k, j, l))

    return points_proches



def snap_points(reseau, points_proches):
    """
    Regroupe les points proches en leur attribuant une position commune.

    Les traces conservent leurs vertex.
    """

    # Parcourir les couples de points proches
    for i, k, j, l in points_proches:

        # Récupérer les deux traces
        trace1 = reseau.getTrack(i)
        trace2 = reseau.getTrack(j)

        # Récupérer les deux observations
        point1 = trace1.getObs(k)
        point2 = trace2.getObs(l)

        # Récupérer les coordonnées du premier point
        nouveau_x = point1.position.getX()
        nouveau_y = point1.position.getY()

        # Déplacer le deuxième point sur le premier
        point2.position.setX(nouveau_x)
        point2.position.setY(nouveau_y)

        # Réinsérer le point modifié
        trace2.setObs(l, point2)

    return reseau


def trouver_noeuds(reseau, points_proches):
    """
    Repère les nœuds qui délimitent les arcs.

    Les extrémités des portions communes sont considérées comme des nœuds.
    """

    indices_proches = {}

    # Récupérer les indices des points proches pour chaque trace
    for i, k, j, l in points_proches:

        if i not in indices_proches:
            indices_proches[i] = set()

        if j not in indices_proches:
            indices_proches[j] = set()

        indices_proches[i].add(k)
        indices_proches[j].add(l)

    noeuds = {}

    # Parcourir les traces
    for i, trace in enumerate(reseau):

        # Les extrémités sont toujours des nœuds
        indices = {0, trace.size() - 1}

        # Récupérer les points proches de cette trace
        proches = sorted(indices_proches.get(i, []))

        if len(proches) > 0:

            debut = proches[0]
            precedent = proches[0]

            # Regrouper les indices consécutifs
            for indice in proches[1:]:

                if indice != precedent + 1:

                    # Fin d'une portion commune
                    indices.add(debut)
                    indices.add(precedent)

                    debut = indice

                precedent = indice

            # Ajouter la dernière portion commune
            indices.add(debut)
            indices.add(precedent)

        noeuds[i] = sorted(indices)

    return noeuds


def construire_arcs(reseau, noeuds):
    """
    Découpe les traces en arcs délimités par les nœuds.
    """

    arcs = []

    # Parcourir les traces
    for i, trace in enumerate(reseau):

        observations = trace.getObsList()
        indices = noeuds[i]

        # Découper la trace entre deux nœuds consécutifs
        for j in range(len(indices) - 1):

            debut = indices[j]
            fin = indices[j + 1]

            # Récupérer les observations de l'arc
            observations_arc = observations[debut:fin + 1]

            # Un arc doit contenir au moins deux points
            if len(observations_arc) >= 2:

                arc = tkl.Track(observations_arc)
                arcs.append(arc)

    return tkl.core.TrackCollection(arcs)


def supprimer_arcs_doubles(reseau):
    """
    Supprime les arcs qui sont présents en double.
    Deux arcs sont considérés identiques si leurs vertex
    sont identiques, même si leur sens de parcours est inversé.
    """

    arcs_uniques = []
    arcs_vus = set()

    for trace in reseau:

        coordonnees = []

        # Récupérer les coordonnées des vertex
        for j in range(trace.size()):

            point = trace.getObs(j)

            x = round(point.position.getX(), 6)
            y = round(point.position.getY(), 6)

            coordonnees.append((x, y))

        # Créer une représentation de l'arc dans les deux sens
        sens_direct = tuple(coordonnees)
        sens_inverse = tuple(reversed(coordonnees))

        # Garder la représentation la plus petite
        cle = min(sens_direct, sens_inverse)

        # Vérifier si l'arc existe déjà
        if cle not in arcs_vus:

            arcs_vus.add(cle)
            arcs_uniques.append(trace)

    return tkl.core.TrackCollection(arcs_uniques)


def reconstruire_reseau(reseau, points_proches):
    """
    Regroupe les points proches, découpe les traces en arcs
    et supprime les arcs présents en double.
    """

    # Regrouper les points proches
    reseau = snap_points(reseau, points_proches)

    # Trouver les nœuds du réseau
    noeuds = trouver_noeuds(reseau, points_proches)

    # Découper les traces en arcs
    reseau = construire_arcs(reseau, noeuds)

    # Supprimer les arcs en double
    reseau = supprimer_arcs_doubles(reseau)

    return reseau

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

    # # Suppression d'un arc
    # supprimer_vertex(reseau)

    # Déplacer un vertex
    deplacer_vertex(reseau, tracks)

    # Affichage
    for r in reseau:
        plt.plot(r.getX(), r.getY(), linewidth=2, alpha=0.5, color='red')
    plt.show()

    ###main pour le snap
     # # Création de la première trace
    # trace1 = tkl.Track([
    #     tkl.Obs(tkl.ENUCoords(0, 0, 0)),
    #     tkl.Obs(tkl.ENUCoords(20, 20, 0)),
    #     tkl.Obs(tkl.ENUCoords(40, 40, 0)),
    #     tkl.Obs(tkl.ENUCoords(80, 80, 0)),
    #     tkl.Obs(tkl.ENUCoords(100, 100, 0)),
    #     tkl.Obs(tkl.ENUCoords(120, 120, 0))
    # ])

    # # Création de la deuxième trace
    # trace2 = tkl.Track([
    #     tkl.Obs(tkl.ENUCoords(0, 60, 0)),
    #     tkl.Obs(tkl.ENUCoords(20, 50, 0)),
    #     tkl.Obs(tkl.ENUCoords(40, 55, 0)),
    #     tkl.Obs(tkl.ENUCoords(60, 65, 0)),
    #     tkl.Obs(tkl.ENUCoords(80, 85, 0)),
    #     tkl.Obs(tkl.ENUCoords(120, 150, 0))
    # ])

    # # Création du réseau avec les deux traces
    # reseau = tkl.core.TrackCollection([trace1, trace2])

    # # Affichage avant Snap
    # plt.figure(figsize=(8, 6))

    # for r in reseau:
    #     plt.plot(r.getX(), r.getY(), linewidth=2, alpha=0.5)

    # # Détection des points proches
    # points_proches = detecter_points_proches(reseau, None)

    # print("Points proches :", points_proches)

    # # Reconstruction du réseau
    # reseau = reconstruire_reseau(reseau, points_proches)

    # print("Nombre d'arcs après reconstruction :", len(reseau))

    # # Affichage après reconstruction
    # for r in reseau:
    #     plt.plot(r.getX(), r.getY(), linewidth=2)

    # plt.show()

    # # Affichage des coordonnées des arcs
    # for i in range(len(reseau)):

    #     trace = reseau.getTrack(i)

    #     print("\nArc", i)

    #     for j in range(trace.size()):

    #         obs = trace.getObs(j)

    #         x = obs.position.getX()
    #         y = obs.position.getY()

    #         print("Point", j, ":", (x, y))
