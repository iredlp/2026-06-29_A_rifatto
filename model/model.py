import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()  # grafo semplice
        self._idMapA = {}

    def getAllCountries(self):
        return DAO.getAllCountries()

    def creaGrafo(self, country):
        self._grafo.clear()
        self._idMapA.clear()

        clienti = DAO.getAllNodes(country)
        for a in  clienti:
            self._idMapA[a. CustomerId] = a
            self._grafo.add_node(a)
            # aggiungo i nodi
        print("2 - Nodi aggiunti")

        for a in clienti:
            a.list_artisti.clear()
            a.fatturato = 0
            a.list_artisti= set(DAO.getArtistiPerCliente(country,a.CustomerId))
           # a.list_clienti = DAO.getClientiPerArtista(a.ArtistId, genere)
            a.fatturato = DAO.getFatturatoPerCliente(a.CustomerId)
        print("3 - Informazioni recuperate")

        for i in range(len(clienti)):
            a1 = clienti[i]
            p1 = a1.fatturato
            for j in range(i + 1, len(clienti)):
                a2 = clienti[j]
                p2 = a2.fatturato
                clientiComuni = (set(a1.list_artisti) & set(a2.list_artisti))
                #  peso = 0
                # ND: & FUNZIONA SOLO CON I SET! SE HAI LE LISTE CONSERVTILE IN SET E POI CONFRONTALE
                #  for film in  clientiComuni:
                #     incasso=DAO.getIncassiPerFilm(film)
                #    peso+=incasso[0]
                if len(clientiComuni) > 0 and a1 != a2 :
                    peso = p1 + p2
                    if p1 > p2:
                        self._grafo.add_edge(a1, a2, weight=peso)
                    elif p2 > p1:
                        self._grafo.add_edge(a2, a1, weight=peso)
                    else:
                        self._grafo.add_edge(a1, a2, weight=peso)
                        self._grafo.add_edge(a2, a1, weight=peso)

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_num_nodes(self) -> int:
        return self._grafo.number_of_nodes()

    def get_num_edges(self) -> int:
        return self._grafo.number_of_edges()

    def getAllNodes(self, genere):
        return DAO.getAllNodes(genere)
    def getProdottoById(self, idP):
        return self._idMapA[int(idP)]

    def getTopArcoInfluenz(self):
        # return sorted(self._grafo.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:10]
        # archi = self._grafo.edges(data=True)
        risultati = []

        for p in self._grafo.nodes:
            uscenti = self._grafo.out_edges(p, data=True)
            entranti = self._grafo.in_edges(p, data=True)
            numero = len(uscenti)
            peso = sum(d["weight"] for _, _, d in uscenti) - \
                   sum(d["weight"] for _, _, d in entranti)

            risultati.append((p, peso))
            # risultati.append((p, numero, peso))
        risultati.sort(key=lambda x: x[1], reverse=True)
        if len(risultati) == 0:
            return None

        return risultati[0]

    def getTop5Archi(self):
        # return sorted(self._grafo.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:10]
        archi = self._grafo.edges(data=True)
        return sorted(
            archi,
            key=lambda x: (x[2]["weight"]),
            reverse=True)[:5]  # SE LASCIO REVERSE=TRUE ORDINO PER OORDINE ALFAB DECRESCENTE!!

    def getGruppoClienti(self, start_node):
        self._best_path = []
        self._best_score = float("-inf")

        parziale = [start_node]
        score = start_node.fatturato

        #self._ricorsione(parziale,  score)
        self._ricorsione(parziale, 0,)
        return self._best_path, self._best_score

    def _ricorsione(self, parziale, score):
        ultimo = parziale[-1]
        # Controllo se il percorso attuale è migliore
        if len(parziale) > len(self._best_path): #massimizzare il numero di archi.
            self._best_path = list(parziale)
            self._best_score = score

        # Caso terminale: abbiamo raggiunto la lunghezza richiesta
        # if len(parziale) == k:
        # if ultimo == end_node:
       # if score < self._best_score: #QUESTA MINIMIZZA IL FATTURATO COMPLESSIVO
           # self._best_score = score
          #  self._best_path = list(parziale)

        # Esploro i vicini raggiungibili con un arco uscente
        for vicino in self._grafo.successors(ultimo):

            # Non posso visitare due volte lo stesso nodo
            if vicino not in parziale:
                # Il fatturato deve essere decrescente
                if vicino.fatturato <= ultimo.fatturato:
                    # Recupero il peso dell'arco
               # peso = self._grafo[ultimo][vicino]["weight"]
                # I pesi devono essere strettamente decrescenti
               # if ultimo_peso is None or peso <= ultimo_peso:
                    # Aggiungo il vicino al percorso
                    parziale.append(vicino)
                    # Continuo la ricorsione aggiornando il punteggio
                    self._ricorsione(parziale, score + vicino.fatturato)
                    # Tolgo il vicino per provare un'altra possibilità
                    parziale.pop()
