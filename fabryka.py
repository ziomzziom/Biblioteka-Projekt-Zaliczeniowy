"""Wzorzec Factory – fabryka tworząca różne typy materiałów bibliotecznych."""

from material import Ksiazka, Czasopismo, Multimedia, MaterialBiblioteczny

class FabrykaMaterialow:
    """Fabryka do tworzenia materiałów bibliotecznych bez bezpośredniego używania konstruktorów."""

    @staticmethod
    def utworz(typ: str, **dane) -> MaterialBiblioteczny:
        """
        Tworzy i zwraca materiał odpowiedniego typu.

        :param typ: 'ksiazka', 'czasopismo', 'multimedia'
        :param dane: słownik z wymaganymi parametrami
        :return: instancja klasy pochodnej MaterialBiblioteczny
        :raises ValueError: dla nieznanego typu
        """
        typ = typ.lower()
        if typ == 'ksiazka':
            return Ksiazka(
                tytul=dane['tytul'],
                autor=dane['autor'],
                rok=dane['rok'],
                sygnatura=dane['sygnatura'],
                liczba_stron=dane.get('liczba_stron', 0)
            )
        elif typ == 'czasopismo':
            return Czasopismo(
                tytul=dane['tytul'],
                autor=dane['autor'],
                rok=dane['rok'],
                sygnatura=dane['sygnatura'],
                numer_wydania=dane.get('numer_wydania', 1)
            )
        elif typ == 'multimedia':
            return Multimedia(
                tytul=dane['tytul'],
                autor=dane['autor'],
                rok=dane['rok'],
                sygnatura=dane['sygnatura'],
                czas_trwania=dane.get('czas_trwania', 0)
            )
        else:
            raise ValueError(f"Nieznany typ materiału: {typ}")