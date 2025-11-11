from dataclasses import dataclass
from database.consumo_DAO import ConsumoDAO

'''
    DTO (Data Transfer Object) dell'entità Impianto
'''

@dataclass()
class Impianto:
    id: int
    nome: str
    indirizzo: str

    # RELAZIONI
    lista_consumi: list = None

    def get_consumi(self):
        """ Aggiorna e Restituisce la lista di consumi (self.lista_consumi) associati all'impianto"""
        # TODO ???

    def __eq__(self, other):
        return isinstance(other, Impianto) and self.id == other.id

    def __str__(self):
        return f"{self.id} | {self.nome} | Indirizzo: {self.indirizzo}"

    def __repr__(self):
        return f"{self.id} | {self.nome} | Indirizzo: {self.indirizzo}"

