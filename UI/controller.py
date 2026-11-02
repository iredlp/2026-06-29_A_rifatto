import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDCountry(self):
        try:
            self._view._ddCountry.options.clear()
            attori = self._model.getAllCountries()
            for actor in attori:
                self._view._ddCountry.options.append(ft.dropdown.Option(actor))#key=actor.ArtistId,
                                                                        #text=actor.Name))
        # self._view.update_page()
        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore nel recupero DEI VALORI: {ex}", color="red"))

        self._view.update_page()


    def handleCreaGrafo(self, e):
        country = self._view._ddCountry.value

        if not country:
            self._view.create_alert("Selezionare il GENERE prima di creare il grafo.", color="red")
            return
        try:
            self._model.creaGrafo(country)
            n_nodes = self._model.get_num_nodes()
            n_edges = self._model.get_num_edges()
            # Stampa immediata numero di vertici e archi (Punto 1.c)
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text(f"Grafo creato con successo!\nNumero vertici: {n_nodes}\nNumero archi: {n_edges}",
                        color="green"))
            # RIEMPIO IL DROPDOWN DEI FILM DEL GRAFO
            self.fillDDNodi(country)
        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore durante la creazione del grafo: {ex}", color="red"))
            # return
        self._view.update_page()

    def handleStampaInfo(self,e):

        # CONTROLLER:
        top = self._model.getTopArcoInfluenz()
        # self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"  Arco influenza max: {top}", color="green"))

        top5 = self._model.getTop5Archi()
        self._view._txt_result.controls.append(ft.Text(f"Archi di peso maggiore", color="green"))

        for i, arco in enumerate(top5, start=1):
            a1, a2, dati = arco
            self._view._txt_result.controls.append(ft.Text(
                f"{i})   {a1.LastName} {a1.FirstName} ({a1. Country}) -- {a2.FirstName} {a2.LastName} ({a1. Country}) "
                f"(Peso: {dati['weight']})")
            )
        self._view.update_page()

    def fillDDNodi(self, country):
        try:
            self._view._ddClienti.options.clear()
            attori = self._model.getAllNodes(country)
            for actor in attori:
                self._view._ddClienti.options.append(ft.dropdown.Option(key=actor.CustomerId,
                                                                        text=actor.LastName))
        # self._view.update_page()
        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore nel recupero dei clienti: {ex}", color="red"))

        self._view.update_page()

    def handleSequenza(self,e):
        self._view._txt_result.controls.clear()
        if self._model.get_num_nodes() == 0 :
            self._view.create_alert("Creare prima il grafo!", color="red")
            return
        start = self._model.getProdottoById(self._view._ddClienti.value)
        # end = self._model.getProdottoById(self._view._ddProdEnd.value)
        # qui dovremmo fare i solti controlli sulla validità

        if start is None:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore ! devi inserire i nodi iniziali   per procedere!", color="red")
            )
            self._view.update_page()
            return

        # Calcolo il percorso di peso massimo
        percorso, peso = self._model.getGruppoClienti(start)

        # Visualizzo il risultato
        self._view._txt_result.controls.append(
            ft.Text("Percorso :", weight="bold", color="orange"))

        for i in range(len(percorso)):
            self._view._txt_result.controls.append(
                ft.Text(f"Ordine {percorso[i].CustomerId} - " f" {percorso[i].fatturato}"))

        self._view._txt_result.controls.append(
            ft.Text(f"Lunghezza percorso trovato:{len(percorso)-1}", color="green")
            #metto il -1 PK CHIEDE IL NUMERO DI ARCHI
        )
        self._view._txt_result.controls.append(
            ft.Text(f"Fatturato totale: {peso}", color="green")
        )
     #   fatturato_tot=0.0
      #  for f in percorso:
       #     fatturato_tot += f.fatturato
       # self._view._txt_result.controls.append(
         #   ft.Text(f"Fattturato totale:{fatturato_tot}", color="green")  )

        self._view.update_page()