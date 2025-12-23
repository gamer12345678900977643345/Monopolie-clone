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
speler2 = Speler(
    naam = "nig",
    balans= 1500,
    eigendommen= 0,
    effects= None #dit kan bv zijn ga naar jail
)
bot1 = Speler(
    naam = "bot",
    balans= 1500,
    eigendommen= 0,
    effects= None
)
