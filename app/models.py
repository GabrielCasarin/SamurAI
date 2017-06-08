from py2neo.ogm import GraphObject, Property, RelatedTo


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
