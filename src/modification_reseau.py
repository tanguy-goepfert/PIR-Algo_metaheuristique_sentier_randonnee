from initialisation_jeu_de_trace import *




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

def ajout_d_un_arc(reseau):
    
    pass



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
    plt.plot(reseau.getX(), reseau.getY(), linewidth=0.7, alpha=0.5)
    plt.axis('equal')
    plt.legend()
    plt.show()

