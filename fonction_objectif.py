import matplotlib.pyplot as plt
import tracklib as tkl
import math
import statistics

def traces_random(nb, sinuosite=0.2):
    """
    Génère nb traces simulées de complexité paramétrable. Autrement dit, génère un réseau simple.
    :param nb : nombre des traces
    :type nb : int
    :param sinuosite : complexité de la trace. Proche de 0 : très complexe
    :type sinuosite : float
    """
    # Génèration des traces
    liste_traces = []
    for i in range(nb):
        # Liste d'observations
        trace = tkl.generate(sinuosite, dt=10)[::3]
        trace.scale(1)
        liste_traces.append(trace)
    tracks = tkl.core.TrackCollection(liste_traces)
    return tracks


def bruitage(N):
    # nombre de traces bruitées souhaitées
    gps_tracks = tkl.core.TrackCollection()
    for trace in tracks :
        traces_bruitees = tkl.core.TrackCollection([trace] * N)
        traces_bruitees.noise(2, tkl.ExponentialKernel(50))  # erreur GPS : 5 m, portée 20 m
        gps_tracks += traces_bruitees
    return gps_tracks
     
     


def ecart_traces(trace1, trace2):
    x1 = trace1.getX()
    y1 = trace1.getY()

    x2 = trace2.getX()
    y2 = trace2.getY()

    distances = []

    # Pour chaque point on va chercher le point du reseau le plus proche 
    for i in range(len(x1)):
        d_min = float("inf")

        for j in range(len(x2)):
            d = math.sqrt(
                (x1[i] - x2[j])**2
                + (y1[i] - y2[j])**2
            )

            if d < d_min:
                d_min = d

        distances.append(d_min)

    moyenne = statistics.mean(distances)
    ecart_type = statistics.pstdev(distances)

    return moyenne, ecart_type
        

def comparer_toutes_traces(gps_tracks):
    resultats = []
    n = gps_tracks.size()

    for i in range(n):
        trace1 = gps_tracks.getTrack(i)

        for j in range(i + 1, n):
            trace2 = gps_tracks.getTrack(j)

            # Calcul dans les deux sens pour une mesure symétrique
            d1 = ecart_traces(trace1, trace2)
            d2 = ecart_traces(trace2, trace1)

            ecart = (d1 + d2) / 2

            resultats.append((i, j, ecart))

    return resultats



if __name__ == "__main__" :

    # ----------------------------------------------------------
    # Generer les traces
    # ----------------------------------------------------------

    tkl.seed(110) #bloque l'aléatoire
    tracks = traces_random(2, 0.1)


    # ----------------------------------------------------------
    # Bruitage 
    # ----------------------------------------------------------

    gps_tracks = bruitage(10)


    # ----------------------------------------------------------
    # Manipulation
    # ----------------------------------------------------------
    for t in gps_tracks:
        print("Nouvelle trace")
        for obs in t.getObsList():
            plt.plot(t.getX(), t.getY(), 'k-', linewidth=2, label=f'originale')



    # ----------------------------------------------------------
    # Affichage
    # ----------------------------------------------------------

    plt.figure(figsize=(8, 6))

    # Affichage des traces
    for t in gps_tracks:
        plt.plot(t.getX(), t.getY(), linewidth=0.7, alpha=0.5)
    
    # Trace originale par dessus
    for t in tracks:
        plt.plot(t.getX(), t.getY(), 'k-', linewidth=2, label=f'originale')



    plt.axis('equal')
    plt.legend()
    plt.show()
    
    resultats = comparer_toutes_traces(gps_tracks)
    
    for i, j, ecart in resultats:
        print(f"Trace {i} - Trace {j} : écart = {ecart:.3f}")
    
    print("Nombre de comparaisons :", len(resultats))