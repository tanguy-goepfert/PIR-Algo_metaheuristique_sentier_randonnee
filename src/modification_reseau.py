from initialisation_jeu_de_trace import *
import math



def random_tirage_track(tracks):
    nbre_arcs = 2
    nbre = math.ceil(nbre_arcs * math.log(nbre_arcs))
    tkl.seed(150)
    indices = random.sample(range(nbre_arcs), nbre)

    var_traces = []
    for i in indices:
        trace = tracks.getTrack(i)
        var_traces.append(trace)

    liste_traces = tkl.core.TrackCollection(var_traces)
    return liste_traces

def ajout_d_un_arc(reseau, tracks):
    # Tirage du type d'action a faire : 99% tirer un trait droit, 1% tirer une trace dans le jeu de trace initial.
    r = random.randint(0, 100)
    if r == 99 :
        new_arc = random.choice(tracks)
    else :
        tkl.seed(3)
        p1 = tkl.ENUCoords(random.randint(0, 100), random.randint(0, 100),  0.0)
        tkl.seed(4)
        p2 = tkl.ENUCoords(random.randint(0, 100), random.randint(0, 100),  0.0)
        o1 = tkl.Obs(p1)
        o2 = tkl.Obs(p2)
        new_arc = tkl.Track([o1, o2])
    reseau.addTrack(new_arc)

def supprimer_arc(trace, debut, fin):
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
    ### ----------------------
    tkl.seed(110) #bloque l'aléatoire
    tracks = traces_random(2, 0.1)
    # Bruitage 
    gps_tracks = bruitage(tracks, 10)
    # Initialisation d'un premier réseau 
    reseau = random_tirage_track(gps_tracks)
    # Ajout d'un arc
    ajout_d_un_arc(reseau, tracks)

    # Affichage
    plt.figure(figsize=(8, 6))
    for r in reseau:
        plt.plot(r.getX(), r.getY(), linewidth=5, alpha=0.5, color='black')

    for t in gps_tracks:
        plt.plot(t.getX(), t.getY(), linewidth=0.7, alpha=0.5)
    plt.axis('equal')
    plt.legend()
    plt.show()
