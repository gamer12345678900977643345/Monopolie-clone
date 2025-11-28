class Speler():
    def __init__(self, naam, balans, eigendommen, effects):
        self.naam = naam
        self.balans = balans
        self.eigendom = eigendommen
        self.effects = effects

speler1 = Speler(
    naam= "91",
    balans= 1500,
    eigendommen= 0,
    effects= None
)
# print(speler1.naam)
