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
        new_arc = tkl.TrackCollection([tracks[random.randint(0, len(tracks))]])
    else :
        x_o1 = random.randint(0, 100)
        y_o1 = random.randint(0, 100)
        x_o2 = random.randint(0, 100)
        y_o2 = random.randint(0, 100)
        new_arc = tkl.track(tkl.Obs(x_o1, y_o1), tkl.Obs(x_o2, y_o2))
    new_reseau = reseau.addTrack(new_arc) 
    return new_reseau

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

    reseau = random_tirage_track(gps_tracks)

    # Affichage
    plt.figure(figsize=(8, 6))
    for t in reseau:
        plt.plot(t.getX(), t.getY(), linewidth=0.7, alpha=0.5)
    plt.axis('equal')
    plt.legend()
    plt.show()

    # Affichage des traces GPS
    plt.figure(figsize=(8, 6))
    for t in gps_tracks:
        plt.plot(t.getX(), t.getY(), linewidth=0.7, alpha=0.5)
    plt.axis('equal')
    plt.legend()
    plt.show()
