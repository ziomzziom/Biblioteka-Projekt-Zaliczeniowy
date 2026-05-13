"""Singleton – klasa zarządzająca zbiorami biblioteki oraz wypożyczeniami."""

import json
from typing import Dict, List, Optional
from material import MaterialBiblioteczny
from czytelnik import Czytelnik
from exceptions import MaterialNieZnalezionyError, CzytelnikNieZnalezionyError

class Biblioteka:
    """
    Singleton – tylko jedna instancja biblioteki.
    Przechowuje materiały i czytelników.
    """

    _instancja = None

    def __new__(cls):
        if cls._instancja is None:
            cls._instancja = super().__new__(cls)
            cls._instancja.__materialy: Dict[str, MaterialBiblioteczny] = {}
            cls._instancja.__czytelnicy: Dict[int, Czytelnik] = {}
        return cls._instancja

    def dodaj_material(self, material: MaterialBiblioteczny) -> None:
        """Dodaje materiał do biblioteki (klucz = sygnatura)."""
        self.__materialy[material.sygnatura] = material

    def usun_material(self, sygnatura: str) -> None:
        """Usuwa materiał z biblioteki."""
        if sygnatura not in self.__materialy:
            raise MaterialNieZnalezionyError(sygnatura)
        del self.__materialy[sygnatura]

    def znajdz_material(self, sygnatura: str) -> Optional[MaterialBiblioteczny]:
        """Zwraca materiał o danej sygnaturze lub None."""
        return self.__materialy.get(sygnatura)

    def dodaj_czytelnika(self, czytelnik: Czytelnik) -> None:
        self.__czytelnicy[czytelnik.id] = czytelnik

    def znajdz_czytelnika(self, czytelnik_id: int) -> Optional[Czytelnik]:
        return self.__czytelnicy.get(czytelnik_id)

    def wypozycz(self, sygnatura: str, czytelnik_id: int) -> None:
        """
        Wypożycza materiał czytelnikowi.
        Rzuca wyjątki jeśli materiał nie istnieje, jest niedostępny lub czytelnik nie istnieje.
        """
        material = self.znajdz_material(sygnatura)
        if material is None:
            raise MaterialNieZnalezionyError(sygnatura)
        czytelnik = self.znajdz_czytelnika(czytelnik_id)
        if czytelnik is None:
            raise CzytelnikNieZnalezionyError(czytelnik_id)
        material.wypozycz(czytelnik_id)
        czytelnik.dodaj_wypozyczenie(sygnatura)

    def zwroc(self, sygnatura: str, czytelnik_id: int) -> None:
        """Zwraca materiał do biblioteki."""
        material = self.znajdz_material(sygnatura)
        if material is None:
            raise MaterialNieZnalezionyError(sygnatura)
        czytelnik = self.znajdz_czytelnika(czytelnik_id)
        if czytelnik is None:
            raise CzytelnikNieZnalezionyError(czytelnik_id)
        material.zwroc()
        czytelnik.usun_wypozyczenie(sygnatura)

    def lista_materialow(self) -> List[MaterialBiblioteczny]:
        """Zwraca listę wszystkich materiałów."""
        return list(self.__materialy.values())

    def lista_czytelnikow(self) -> List[Czytelnik]:
        return list(self.__czytelnicy.values())

    def zapisz_do_pliku(self, plik_materialy: str = "materialy.json", plik_czytelnicy: str = "czytelnicy.json") -> None:
        """Zapisuje stan biblioteki do plików JSON."""
        with open(plik_materialy, 'w', encoding='utf-8') as f:
            json.dump([m.to_dict() for m in self.__materialy.values()], f, indent=4, ensure_ascii=False)
        with open(plik_czytelnicy, 'w', encoding='utf-8') as f:
            json.dump([c.to_dict() for c in self.__czytelnicy.values()], f, indent=4, ensure_ascii=False)

    def wczytaj_z_pliku(self, plik_materialy: str = "materialy.json", plik_czytelnicy: str = "czytelnicy.json") -> None:
        """Wczytuje dane z plików JSON i odtwarza stan."""
        try:
            with open(plik_materialy, 'r', encoding='utf-8') as f:
                dane = json.load(f)
                for item in dane:
                    mat = MaterialBiblioteczny.from_dict(item)
                    self.dodaj_material(mat)
        except FileNotFoundError:
            pass  # Brak pliku – nie wczytujemy

        try:
            with open(plik_czytelnicy, 'r', encoding='utf-8') as f:
                dane = json.load(f)
                for item in dane:
                    cz = Czytelnik.from_dict(item)
                    self.dodaj_czytelnika(cz)
        except FileNotFoundError:
            pass