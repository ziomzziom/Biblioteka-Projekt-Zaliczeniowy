# Prezentacja – System Biblioteczny (Projekt PPO)

---

## 1. Abstrakcja

**Plik:** `material.py:7-65`

Klasa `MaterialBiblioteczny(ABC)` dziedziczy po `ABC` z modułu `abc`, co czyni ją **klasą abstrakcyjną**. Nie można utworzyć jej instancji bezpośrednio – próba `MaterialBiblioteczny(...)` kończy się błędem `TypeError`.

Metoda abstrakcyjna `wyswietl_info()` (linia 62) z dekoratorem `@abstractmethod` **wymusza** implementację w każdej podklasie. Jeśli podklasa jej nie zdefiniuje, Python nie pozwoli na utworzenie instancji tej podklasy.

Wspólny interfejs (zestaw metod dostępnych dla każdego materiału):
- `wypozycz(czytelnik_id)` – wypożyczenie materiału
- `zwroc()` – zwrot materiału
- `czy_dostepny()` – sprawdzenie dostępności
- `to_dict()` / `from_dict()` – serializacja do/z JSON

---

## 2. Hermetyzacja

Wszystkie atrybuty przechowujące stan obiektów są **prywatne** – użyto podwójnego podkreślenia `__`, co uruchamia _name mangling_ Pythona. Dostęp do nich możliwy jest wyłącznie przez publiczne właściwości (`@property`) i metody.

| Klasa | Atrybuty prywatne |
|-------|--------------------|
| `MaterialBiblioteczny` (`material.py:14-19`) | `__tytul`, `__autor`, `__rok`, `__sygnatura`, `__wypozyczony`, `__wypozyczony_przez` |
| `Ksiazka` (`material.py:120`) | `__liczba_stron` |
| `Czasopismo` (`material.py:141`) | `__numer_wydania` |
| `Multimedia` (`material.py:162`) | `__czas_trwania` |
| `Czytelnik` (`czytelnik.py:11-15`) | `__id`, `__imie`, `__nazwisko`, `__wypozyczone_sygnatury` |
| `Biblioteka` (`biblioteka.py:20-21`) | `__materialy`, `__czytelnicy` |

**Przykład getterów** – `material.py:22-44`:
```python
@property
def tytul(self) -> str:
    return self.__tytul
```

Metoda `wypozycz()` (`material.py:46-51`) zmienia stan wewnętrzny tylko przez własną logikę – nie da się bezpośrednio ustawić `__wypozyczony = True` z zewnątrz.

---

## 3. Dziedziczenie

### Hierarchia materiałów

```
MaterialBiblioteczny (ABC)          – klasa abstrakcyjna
├── Ksiazka      (material.py:115)  – dodaje liczba_stron
├── Czasopismo   (material.py:136)  – dodaje numer_wydania
└── Multimedia   (material.py:157)  – dodaje czas_trwania
```

Wszystkie trzy podklasy wywołują `super().__init__()` w konstruktorze (linie 119, 140, 161), przekazując wspólne dane do klasy bazowej i rozszerzając je o własne atrybuty.

Metoda `to_dict()` w podklasach wywołuje `super().to_dict()` (linie 131, 152, 173), a następnie dodaje do słownika swoje specyficzne pole:
```python
# Ksiazka.to_dict() – material.py:130-133
def to_dict(self) -> dict:
    data = super().to_dict()
    data['liczba_stron'] = self.__liczba_stron
    return data
```

### Hierarchia wyjątków

```
BibliotekaError (Exception)         – exceptions.py:3
├── MaterialNieDostepnyError        – exceptions.py:7
├── MaterialNieZnalezionyError      – exceptions.py:19
└── CzytelnikNieZnalezionyError     – exceptions.py:13
```

Wszystkie dziedziczą po `BibliotekaError`, co umożliwia łapanie wszystkich wyjątków bibliotecznych jednym `except BibliotekaError`.

---

## 4. Polimorfizm

Metoda `wyswietl_info()` ma **tę samą nazwę i sygnaturę** we wszystkich trzech podklasach, ale zwraca różne informacje:

| Klasa | Co wyświetla dodatkowo |
|-------|------------------------|
| `Ksiazka` (`material.py:126-128`) | liczba stron |
| `Czasopismo` (`material.py:147-149`) | numer wydania |
| `Multimedia` (`material.py:168-170`) | czas trwania (minuty) |

### Demonstracja – main.py:113-118

Funkcja `wyswietl_wszystkie()` przetwarza kolekcję obiektów różnych typów (pochodzących z tej samej klasy bazowej) w jednej pętli:

```python
def wyswietl_wszystkie(lista_materialow):
    for m in lista_materialow:
        print(m.wyswietl_info())  # polimorfizm – sama nazwa, różne działanie
```

Wywołana dla listy `[Ksiazka, Czasopismo, Multimedia]` – Python sam dobiera odpowiednią implementację na podstawie rzeczywistego typu obiektu.

Dodatkowo `__str__()` w `Czytelnik` (`czytelnik.py:61-62`) to też przykład polimorfizmu (nadpisanie metody wbudowanej).

---

## 5. Wzorce projektowe

### Singleton – `biblioteka.py:15-22`

```python
class Biblioteka:
    _instancja = None

    def __new__(cls):
        if cls._instancja is None:
            cls._instancja = super().__new__(cls)
            cls._instancja.__materialy = {}
            cls._instancja.__czytelnicy = {}
        return cls._instancja
```

Gwarantuje, że w całym programie istnieje tylko **jedna instancja** biblioteki. Zarówno `main.py` (demo CLI), jak i `app.py` (serwer Flask) operują na tym samym obiekcie – zapobiega to rozjechaniu się stanu danych.

### Factory (Metoda wytwórcza) – `fabryka.py:5-44`

```python
class FabrykaMaterialow:
    @staticmethod
    def utworz(typ: str, **dane) -> MaterialBiblioteczny:
        ...
```

Na podstawie parametru `typ` (`ksiazka`, `czasopismo`, `multimedia`) tworzy odpowiednią podklasę. Kod klienta nie musi znać konkretnych konstruktorów – wystarczy wywołać `FabrykaMaterialow.utworz(...)`.

---

## 6. Obsługa błędów

### Własne wyjątki – `exceptions.py`

Każdy wyjątek niesie informację specyficzną dla kontekstu błędu (sygnatura lub ID) i formatuje czytelny komunikat:
- `MaterialNieDostepnyError(sygnatura)` – "Materiał o sygnaturze 'X' jest niedostępny."
- `MaterialNieZnalezionyError(sygnatura)` – "Materiał o sygnaturze 'X' nie istnieje w bibliotece."
- `CzytelnikNieZnalezionyError(czytelnik_id)` – "Czytelnik o ID 'Y' nie istnieje."

### Try-except w kodzie

| Miejsce | Co obsługuje |
|---------|--------------|
| `app.py:38-47` | 3 możliwe wyjątki przy wypożyczeniu |
| `app.py:75-80` | Wyjątki przy zwrocie materiału |
| `app.py:101-105` | `ValueError` przy parsowaniu roku/liczby stron |
| `main.py:78-79` | Przechwytywanie błędów w demo |
| `biblioteka.py:91-92` | `FileNotFoundError` przy wczytywaniu JSON (brak pliku = pomiń) |

---

## 7. Typowanie (Type Hints)

Każda metoda ma podpowiedzi typów w sygnaturze:

```python
# biblioteka.py:24
def dodaj_material(self, material: MaterialBiblioteczny) -> None:

# biblioteka.py:44
def wypozycz(self, sygnatura: str, czytelnik_id: int) -> None:

# czytelnik.py:30
def wypozyczone_sygnatury(self) -> List[str]:

# material.py:79
def from_dict(cls, data: dict) -> 'MaterialBiblioteczny':
```

Importy typów: `from typing import Dict, List, Optional`.

---

## 8. Typy sekwencyjne

Zgodnie z przeznaczeniem:

| Typ | Miejsce | Zastosowanie |
|-----|---------|--------------|
| `Dict[str, MaterialBiblioteczny]` | `biblioteka.py:20` | Materiały indeksowane sygnaturą |
| `Dict[int, Czytelnik]` | `biblioteka.py:21` | Czytelnicy indeksowani ID |
| `List[str]` | `czytelnik.py:15` | Lista wypożyczonych sygnatur |
| `List[MaterialBiblioteczny]` | `biblioteka.py:69-71` | Lista wszystkich materiałów |
| `List[Czytelnik]` | `biblioteka.py:73-74` | Lista wszystkich czytelników |

---

## 9. Pliki (JSON) – trwałość danych

**`biblioteka.py:76-101`** – metody `zapisz_do_pliku()` i `wczytaj_z_pliku()`:

- **Zapis**: Każdy obiekt serializowany jest do słownika przez `to_dict()`, następnie lista zapisywana do pliku JSON z `indent=4` i `ensure_ascii=False` (poprawne polskie znaki).
- **Odczyt**: `from_dict()` odtwarza obiekty odpowiedniego typu i przywraca stan wypożyczenia (włącznie z ID czytelnika, który wypożyczył).
- Jeśli pliki nie istnieją (`FileNotFoundError`) – program działa dalej z pustymi kolekcjami.

Pliki: `materialy.json`, `czytelnicy.json`.

---

## 10. Zasada DRY (Don't Repeat Yourself)

- Logika serializacji/deserializacji JSON jest w **jednym miejscu** – klasa `Biblioteka`. Poszczególne klasy dostarczają tylko `to_dict()` / `from_dict()`.
- Fabryka (`FabrykaMaterialow`) eliminuje powtarzanie się konstruktorów w kodzie klienta.
- Walidacja danych wejściowych w `app.py` korzysta z tego samego wzorca dla każdego formularza (sprawdzenie pustych pól → walidacja typu → próba operacji → obsługa wyjątku).

---

## 11. Zasada KISS (Keep It Simple, Stupid)

- Każdy plik `.py` ma jedną, jasną odpowiedzialność (Single Responsibility):
  - `material.py` – definicje typów materiałów
  - `czytelnik.py` – definicja czytelnika
  - `biblioteka.py` – logika wypożyczeń i stan systemu
  - `exceptions.py` – tylko wyjątki
  - `fabryka.py` – tworzenie obiektów
  - `app.py` – warstwa prezentacji (Flask)
  - `main.py` – demo w konsoli
- Endpointy Flask to krótkie, czytelne funkcje.
- Nazwy zmiennych i metod są samoopisujące (np. `czy_dostepny()`, `lista_materialow()`).

---

## 12. Dokumentacja

Każda klasa i kluczowa metoda ma docstring (PEP 257):

- `material.py:7-11` – opis klasy `MaterialBiblioteczny`
- `biblioteka.py:9-12` – opis klasy `Biblioteka` z adnotacją "Singleton"
- `czytelnik.py:5-6` – opis klasy `Czytelnik`
- `fabryka.py:5-6` – opis wzorca Factory
- `main.py:1` – opis całego pliku demo

---

## 13. Scenariusz testowy (main.py)

Plik `main.py:1-123` po uruchomieniu (`python3 main.py`) demonstruje **wszystkie funkcjonalności**:

1. Wczytanie stanu z plików JSON
2. Tworzenie materiałów przez fabrykę (książka, czasopismo, multimedia)
3. Dodawanie czytelników
4. Wyświetlenie stanu biblioteki
5. Wypożyczenie materiału
6. Próba ponownego wypożyczenia tego samego (oczekiwany błąd)
7. Zwrot materiału
8. Próba wypożyczenia nieistniejącej sygnatury (oczekiwany błąd)
9. Zapis stanu do plików JSON
10. **Demonstracja polimorfizmu** – funkcja `wyswietl_wszystkie()` przetwarzająca listę różnych typów materiałów
