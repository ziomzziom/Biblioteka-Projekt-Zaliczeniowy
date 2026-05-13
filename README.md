# System Biblioteczny – Projekt OOP

Projekt obiektowego systemu zarządzania biblioteką z interfejsem konsolowym i webowym (Flask).

## Opis tematu

System umożliwia zarządzanie zbiorami bibliotecznymi: książkami, czasopismami i multimediami.
Wspiera dodawanie materiałów i czytelników, wypożyczanie oraz zwroty, z trwałym zapisem stanu
do plików JSON. Projekt demonstruje paradygmat programowania obiektowego: abstrakcję,
hermetyzację, dziedziczenie i polimorfizm, a także wzorce projektowe Singleton i Factory.

## Struktura projektu

```
Biblioteka-Projekt-Zaliczeniowy-main/
├── material.py          # Abstrakcyjna klasa MaterialBiblioteczny + pochodne (polimorfizm)
├── czytelnik.py         # Klasa Czytelnik (hermetyzacja)
├── exceptions.py        # Własne wyjątki (dziedziczenie po BibliotekaError)
├── fabryka.py           # FabrykaMaterialow – wzorzec Factory
├── biblioteka.py        # Biblioteka – Singleton zarządzający danymi + JSON I/O
├── main.py              # Demonstracja konsolowa wszystkich funkcjonalności
├── app.py               # Interfejs webowy Flask (Bootstrap 5)
├── templates/
│   ├── base.html        # Szablon bazowy (navbar, flash messages)
│   ├── index.html       # Strona główna – tabela materiałów i czytelników
│   ├── borrow.html      # Formularz wypożyczenia
│   ├── return.html      # Formularz zwrotu
│   ├── add_material.html # Formularz dodawania materiału (Factory)
│   └── add_reader.html  # Formularz dodawania czytelnika
├── materialy.json       # Dane materiałów (automatyczny zapis/odczyt)
├── czytelnicy.json      # Dane czytelników (automatyczny zapis/odczyt)
├── requirements.txt     # Zależności
└── README.md            # Ten plik
```

## Uruchomienie

### Wymagania

- Python 3.8+
- Flask (do interfejsu webowego)

```bash
pip install -r requirements.txt
```

### Tryb konsolowy (main.py)

```bash
python3 main.py
```

Demonstruje wszystkie funkcje: tworzenie materiałów (fabryka), dodawanie czytelników,
wypożyczanie, zwrot, obsługę błędów, zapis/odczyt JSON oraz polimorficzne wyświetlanie.

### Tryb webowy (Flask)

```bash
python3 app.py
```

Aplikacja dostępna pod adresem `http://127.0.0.1:5000`.

| Ścieżka             | Opis                                 |
|---------------------|--------------------------------------|
| `/`                 | Lista materiałów i czytelników       |
| `/borrow`           | Wypożycz materiał                    |
| `/return`           | Zwróć materiał                       |
| `/add_material`     | Dodaj nowy materiał (książka, czasopismo, multimedia) |
| `/add_reader`       | Dodaj nowego czytelnika              |

## Elementy paradygmatu OOP

| Cecha           | Miejsce w kodzie                                        |
|-----------------|---------------------------------------------------------|
| **Abstrakcja**  | `MaterialBiblioteczny(ABC)`, `@abstractmethod wyswietl_info()` – `material.py:7,62` |
| **Hermetyzacja**| Atrybuty `__prywatne` we wszystkich klasach; `@property` gettery – `material.py:14-19`, `czytelnik.py:11-15` |
| **Dziedziczenie**| `Ksiazka`, `Czasopismo`, `Multimedia` ← `MaterialBiblioteczny`; wyjątki ← `BibliotekaError`; `super()` – `material.py:119,140,161` |
| **Polimorfizm**  | `wyswietl_info()` w każdej podklasie; funkcja `wyswietl_wszystkie()` iteruje po różnych typach – `main.py:113-116` |

## Wzorce projektowe

- **Singleton** – `Biblioteka` (tylko jedna instancja w systemie) – `biblioteka.py:15-22`
- **Factory** – `FabrykaMaterialow.utworz()` tworzy obiekty na podstawie typu – `fabryka.py:9-44`

## Jakość kodu

- Type hinting we wszystkich modułach (oprócz tras Flask)
- Własne wyjątki z hierarchią (`BibliotekaError` → `MaterialNieDostepnyError` itd.)
- Try-except przy operacjach I/O i logice biznesowej
- Zgodność z DRY, KISS, PEP 8
- Opisy klas i funkcji w docstringach

## Autor

Projekt zaliczeniowy z przedmiotu Programowanie Obiektowe (PO).
