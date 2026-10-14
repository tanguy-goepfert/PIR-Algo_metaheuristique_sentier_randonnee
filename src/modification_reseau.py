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