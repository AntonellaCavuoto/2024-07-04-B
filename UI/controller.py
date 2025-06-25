import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._selectedYear = None
        self._selectedState = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        state = self._selectedState
        year = self._selectedYear
        if state is None:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text(f"Attenzione, scegliere uno stato!", color = "red"))
            self._view.update_page()
            return

        if year is None:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text(f"Attenzione, scegliere un anno!", color = "red"))
            self._view.update_page()
            return

        numNodi, numArchi = self._model.buildGraph(state, year)
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {numNodi}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {numArchi}"))

        numConn, connMax, listConn = self._model.getConnesse()
        self._view.txt_result1.controls.append(ft.Text(f"Il grafo ha: {numConn} componenti connesse"))
        self._view.txt_result1.controls.append(ft.Text(f"La componente connessa più grande è "
                                                       f"costituita da {connMax} nodi"))
        for lc in listConn:
            self._view.txt_result1.controls.append(ft.Text(f"{lc}"))
        self._view.update_page()


    def handle_path(self, e):
        bestPath, bestScore = self._model.getBestPath()
        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f"Il punteggio del percorso ottimo è {bestScore}"))
        self._view.txt_result2.controls.append(ft.Text(f"Il percorso ottimo è costituito da {len(bestPath)}"))
        for node in bestPath:
            self._view.txt_result2.controls.append(ft.Text(f"{node}"))
        self._view.update_page()

    def fillDDYears(self):
        years = self._model.getYears()
        yearsDD = []
        for year in years:
            self._view.ddyear.options.append(ft.dropdown.Option(data=year, text=year, on_click=self.readDDYear))
        self._view.update_page()


    def readDDYear(self, e):
        if e.control.data is None:
            self._selectedYear = None
        else:
            self._selectedYear = e.control.data
            self.fillDDState(self._selectedYear)

        print(f"readDDYears -- {self._selectedYear}")
        
    def fillDDState(self, year):
        states = self._model.getStates(year)
        yearsDD = []
        for state in states:
            self._view.ddstate.options.append(ft.dropdown.Option(data=state, text=state, on_click=self.readDDState))
        self._view.update_page()
        
    def readDDState(self, e):
        if e.control.data is None:
            self._selectedState = None
        else:
            self._selectedState = e.control.data

        print(f"readDDStates -- {self._selectedState}")

