"""Klasa reprezentująca czytelnika biblioteki."""

from typing import List

class Czytelnik:
    """Czytelnik posiadający ID, imię, nazwisko oraz listę wypożyczonych materiałów."""

    _next_id = 1

    def __init__(self, imie: str, nazwisko: str):
        self.__id = Czytelnik._next_id
        Czytelnik._next_id += 1
        self.__imie = imie
        self.__nazwisko = nazwisko
        self.__wypozyczone_sygnatury: List[str] = []  # sygnatury aktualnie wypożyczonych

    @property
    def id(self) -> int:
        return self.__id

    @property
    def imie(self) -> str:
        return self.__imie

    @property
    def nazwisko(self) -> str:
        return self.__nazwisko

    @property
    def wypozyczone_sygnatury(self) -> List[str]:
        return self.__wypozyczone_sygnatury.copy()  # zwracamy kopię

    def dodaj_wypozyczenie(self, sygnatura: str) -> None:
        """Dodaje sygnaturę do listy wypożyczeń czytelnika."""
        self.__wypozyczone_sygnatury.append(sygnatura)

    def usun_wypozyczenie(self, sygnatura: str) -> None:
        """Usuwa sygnaturę z listy wypożyczeń."""
        if sygnatura in self.__wypozyczone_sygnatury:
            self.__wypozyczone_sygnatury.remove(sygnatura)

    def to_dict(self) -> dict:
        return {
            'id': self.__id,
            'imie': self.__imie,
            'nazwisko': self.__nazwisko,
            'wypozyczone_sygnatury': self.__wypozyczone_sygnatury
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Czytelnik':
        """Tworzy czytelnika z danych słownika (odczyt z JSON)."""
        # Ustawienie globalnego licznika _next_id, żeby nie kolidował
        if data['id'] >= cls._next_id:
            cls._next_id = data['id'] + 1
        cz = cls(data['imie'], data['nazwisko'])
        cz.__id = data['id']  # nadpisanie wygenerowanego ID
        cz.__wypozyczone_sygnatury = data['wypozyczone_sygnatury']
        return cz

    def __str__(self) -> str:
        return f"{self.imie} {self.nazwisko} (ID: {self.id})"