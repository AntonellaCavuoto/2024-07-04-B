import copy

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._bestPath = []
        self._bestScore = 0
        self._avvistamentiMese = {}

    def getBestPath(self):
        self._bestPath = []
        self._bestScore = 0
        parziale = []
        self._avvistamentiMese = {}

        for n in self._graph.nodes:
            parziale.append(n)
            if n.datetime.month in self._avvistamentiMese:
                self._avvistamentiMese[n.datetime.month] = self._avvistamentiMese[n.datetime.month] + 1
                self._ricorsione(parziale, n, 100)
                self._avvistamentiMese[n.datetime.month] = self._avvistamentiMese[n.datetime.month] - 1
                parziale.pop()
            else:
                self._avvistamentiMese[n.datetime.month] = 1
                self._ricorsione(parziale, n, 100)
                self._avvistamentiMese[n.datetime.month] = 0
                parziale.pop()

        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, node, score):
        if score > self._bestScore:
            self._bestScore = score
            self._bestPath = copy.deepcopy(parziale)

        for vicino in self._graph.neighbors(node):
            if vicino not in parziale:
                if self.isAmmissibile(vicino, parziale):
                    if vicino.datetime.month == parziale[-1].datetime.month:
                        scoreNuovo = 300
                        parziale.append(vicino)
                        self._ricorsione(parziale, vicino, score + scoreNuovo)
                        self._avvistamentiMese[vicino.datetime.month] = self._avvistamentiMese[
                                                                            vicino.datetime.month] - 1
                        parziale.pop()
                    else:
                        scoreNuovo = 100
                        parziale.append(vicino)
                        self._ricorsione(parziale, vicino, score + scoreNuovo)
                        self._avvistamentiMese[vicino.datetime.month] = self._avvistamentiMese[
                                                                            vicino.datetime.month] - 1
                        parziale.pop()

    def isAmmissibile(self, nodo, parziale):
        """Gli avvistamenti devono avere durata strettamente crescente
        Massimo tre avvistamenti nello stesso mese"""
        ammissibile = False
        if nodo.datetime.month in self._avvistamentiMese:
            if self._avvistamentiMese[nodo.datetime.month] != 3:
                if nodo.duration > parziale[-1].duration and nodo not in parziale:
                    ammissibile = True
                else:
                    ammissibile = False
        else:
            self._avvistamentiMese[nodo.datetime.month] = 1
            if nodo.duration > parziale[-1].duration and nodo not in parziale:
                ammissibile = True
            else:
                ammissibile = False

        return ammissibile

    def buildGraph(self, state, year):
        self._graph.clear()
        self._idMap.clear()

        nodes = DAO.getNodes(state, year)
        for n in nodes:
            self._idMap[n.id] = n

        self._graph.add_nodes_from(nodes)

        possibleEdges = (DAO.getEdges(state, year, state, year, self._idMap))
        for pe in possibleEdges:
            distanza = pe[0].distance_HV(pe[1])
            if distanza < 100:
                self._graph.add_edge(pe[0], pe[1])

        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getConnesse(self):
        conn = list(nx.connected_components(self._graph))
        numConn = len(conn)

        maxNum = 0
        listaOff = []
        for c in conn:
            if len(list(c)) > maxNum:
                maxNum = len(list(c))
                listaOff = list(c)

        return numConn, maxNum, listaOff

    def getYears(self):
        return DAO.getYears()

    def getStates(self, year):
        return DAO.getStates(year)
