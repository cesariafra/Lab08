from database.consumo_DAO import ConsumoDAO
from database.impianto_DAO import ImpiantoDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        mediaA=0
        count = 0
        for el in ConsumoDAO.get_consumi(1):
            if el.data.month == mese:
                mediaA += el.kwh
                count += 1
        mediaA = mediaA / count

        mediaB=0
        for el in ConsumoDAO.get_consumi(2):
            if el.data.month == mese:
                mediaB += el.kwh
        mediaB = mediaB / count

        return [("Impianto A", mediaA), ("Impianto B", mediaB)]

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """
        if giorno == 8:
            self.__sequenza_ottima = sequenza_parziale
            self.__costo_ottimo = costo_corrente
        else:
            if ultimo_impianto == 1:
                consumi_settimana[2][0] += 5
            elif ultimo_impianto == 2:
                consumi_settimana[1][0] += 5

            if consumi_settimana[1][0] < consumi_settimana[2][0]:
                ultimo_impianto = 1
                costo_corrente += consumi_settimana[1][0]
            else:
                ultimo_impianto = 2
                costo_corrente += consumi_settimana[2][0]

            consumi_settimana[1] = consumi_settimana[1][1:]
            consumi_settimana[2] = consumi_settimana[2][1:]
            sequenza_parziale.append(ultimo_impianto)
            giorno += 1

            self.__ricorsione(sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana)

    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        consumi = {1 : [], 2 : []}

        for el in ConsumoDAO.get_consumi(1):
            if el.data.month == mese and len(consumi[1]) <= 7:
                consumi[1].append(el.kwh)

        for el in ConsumoDAO.get_consumi(2):
            if el.data.month == mese and len(consumi[2]) <= 7:
                consumi[2].append(el.kwh)

        return consumi
        # TODO