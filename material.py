"""Klasy reprezentujące materiały biblioteczne (abstrakcja, dziedziczenie, polimorfizm)."""

from abc import ABC, abstractmethod
from typing import Optional
from exceptions import MaterialNieDostepnyError

class MaterialBiblioteczny(ABC):
    """
    Abstrakcyjna klasa bazowa dla wszystkich materiałów w bibliotece.
    Definiuje wspólny interfejs.
    """

    def __init__(self, tytul: str, autor: str, rok: int, sygnatura: str):
        self.__tytul = tytul
        self.__autor = autor
        self.__rok = rok
        self.__sygnatura = sygnatura
        self.__wypozyczony = False
        self.__wypozyczony_przez: Optional[int] = None  # ID czytelnika

    # Gettery i settery (hermetyzacja)
    @property
    def tytul(self) -> str:
        return self.__tytul

    @property
    def autor(self) -> str:
        return self.__autor

    @property
    def rok(self) -> int:
        return self.__rok

    @property
    def sygnatura(self) -> str:
        return self.__sygnatura

    @property
    def wypozyczony(self) -> bool:
        return self.__wypozyczony

    @property
    def wypozyczony_przez(self) -> Optional[int]:
        return self.__wypozyczony_przez

    def wypozycz(self, czytelnik_id: int) -> None:
        """Wypożycza materiał – zmienia stan na niedostępny."""
        if self.__wypozyczony:
            raise MaterialNieDostepnyError(self.__sygnatura)
        self.__wypozyczony = True
        self.__wypozyczony_przez = czytelnik_id

    def zwroc(self) -> None:
        """Zwraca materiał – zmienia stan na dostępny."""
        self.__wypozyczony = False
        self.__wypozyczony_przez = None

    def czy_dostepny(self) -> bool:
        """Zwraca True jeśli materiał jest dostępny."""
        return not self.__wypozyczony

    @abstractmethod
    def wyswietl_info(self) -> str:
        """Zwraca szczegółowy opis materiału – metoda polimorficzna."""
        pass

    def to_dict(self) -> dict:
        """Konwersja do słownika (do zapisu JSON)."""
        return {
            'typ': self.__class__.__name__,
            'tytul': self.__tytul,
            'autor': self.__autor,
            'rok': self.__rok,
            'sygnatura': self.__sygnatura,
            'wypozyczony': self.__wypozyczony,
            'wypozyczony_przez': self.__wypozyczony_przez,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'MaterialBiblioteczny':
        """Tworzy obiekt z słownika (odczyt z JSON)."""
        if data['typ'] == 'Ksiazka':
            obj = Ksiazka(
                tytul=data['tytul'],
                autor=data['autor'],
                rok=data['rok'],
                sygnatura=data['sygnatura'],
                liczba_stron=data.get('liczba_stron', 0)
            )
        elif data['typ'] == 'Czasopismo':
            obj = Czasopismo(
                tytul=data['tytul'],
                autor=data['autor'],
                rok=data['rok'],
                sygnatura=data['sygnatura'],
                numer_wydania=data.get('numer_wydania', 1)
            )
        elif data['typ'] == 'Multimedia':
            obj = Multimedia(
                tytul=data['tytul'],
                autor=data['autor'],
                rok=data['rok'],
                sygnatura=data['sygnatura'],
                czas_trwania=data.get('czas_trwania', 0)
            )
        else:
            raise ValueError(f"Nieznany typ materiału: {data['typ']}")

        # Przywrócenie stanu wypożyczenia
        if data.get('wypozyczony'):
            obj._MaterialBiblioteczny__wypozyczony = True
            obj._MaterialBiblioteczny__wypozyczony_przez = data.get('wypozyczony_przez')
        return obj

class Ksiazka(MaterialBiblioteczny):
    """Klasa reprezentująca książkę."""

    def __init__(self, tytul: str, autor: str, rok: int, sygnatura: str, liczba_stron: int):
        super().__init__(tytul, autor, rok, sygnatura)
        self.__liczba_stron = liczba_stron

    @property
    def liczba_stron(self) -> int:
        return self.__liczba_stron

    def wyswietl_info(self) -> str:
        status = "dostępna" if self.czy_dostepny() else f"wypożyczona (ID czytelnika: {self.wypozyczony_przez})"
        return f"Książka: '{self.tytul}', {self.autor}, {self.rok} r., {self.liczba_stron} str., sygn. {self.sygnatura} - {status}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['liczba_stron'] = self.__liczba_stron
        return data


class Czasopismo(MaterialBiblioteczny):
    """Klasa reprezentująca czasopismo."""

    def __init__(self, tytul: str, autor: str, rok: int, sygnatura: str, numer_wydania: int):
        super().__init__(tytul, autor, rok, sygnatura)
        self.__numer_wydania = numer_wydania

    @property
    def numer_wydania(self) -> int:
        return self.__numer_wydania

    def wyswietl_info(self) -> str:
        status = "dostępne" if self.czy_dostepny() else f"wypożyczone (ID czytelnika: {self.wypozyczony_przez})"
        return f"Czasopismo: '{self.tytul}', {self.autor}, {self.rok} r., nr wyd. {self.numer_wydania}, sygn. {self.sygnatura} - {status}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['numer_wydania'] = self.__numer_wydania
        return data


class Multimedia(MaterialBiblioteczny):
    """Klasa reprezentująca multimedia (DVD, audio)."""

    def __init__(self, tytul: str, autor: str, rok: int, sygnatura: str, czas_trwania: int):
        super().__init__(tytul, autor, rok, sygnatura)
        self.__czas_trwania = czas_trwania  # w minutach

    @property
    def czas_trwania(self) -> int:
        return self.__czas_trwania

    def wyswietl_info(self) -> str:
        status = "dostępne" if self.czy_dostepny() else f"wypożyczone (ID czytelnika: {self.wypozyczony_przez})"
        return f"Multimedia: '{self.tytul}', {self.autor}, {self.rok} r., {self.czas_trwania} min, sygn. {self.sygnatura} - {status}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['czas_trwania'] = self.__czas_trwania
        return data