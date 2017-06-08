from py2neo.ogm import GraphObject, Property, RelatedTo
import numpy as np


class Match(GraphObject):
    date = Property()

    contains = RelatedTo("State")


class State(GraphObject):
    turno = Property()
    samurais = Property()
    tabuleiro = Property()
    budget = Property()
    player = Property()
    qtd_visitas = Property()

    moved_to = RelatedTo("State")

    def to_vect(self):
        tam = 33 + len(self.tabuleiro)**2
        vect = np.ndarray((1, tam))
        vect[0][0] = self.turno
        k = 1
        for i in range(len(self.samurais)):
            for j in range(5):
                vect[0][k] = self.samurais[i][j]
                k += 1
        for i in range(len(self.tabuleiro)):
            for j in range(len(self.tabuleiro)):
                vect[0][k] = self.tabuleiro[i][j]
                k += 1
        vect[0][k] = self.budget
        k += 1
        vect[0][k] = self.player
        return vect
