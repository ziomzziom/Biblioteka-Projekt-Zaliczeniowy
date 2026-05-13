"""Demonstracja działania systemu bibliotecznego."""

from biblioteka import Biblioteka
from czytelnik import Czytelnik
from fabryka import FabrykaMaterialow
from exceptions import MaterialNieDostepnyError, MaterialNieZnalezionyError, CzytelnikNieZnalezionyError

def main():
    print("=== SYSTEM BIBLIOTECZNY ===\n")

    # Singleton – pobieramy instancję biblioteki
    biblioteka = Biblioteka()

    # Wczytanie poprzedniego stanu (jeśli istnieje)
    biblioteka.wczytaj_z_pliku()
    print("Wczytano dane z plików (jeśli istniały).\n")

    # Tworzenie materiałów za pomocą fabryki
    ksiazka1 = FabrykaMaterialow.utworz(
        'ksiazka',
        tytul='Wiedźmin: Ostatnie życzenie',
        autor='Andrzej Sapkowski',
        rok=1993,
        sygnatura='SAP-WIE-01',
        liczba_stron=320
    )
    ksiazka2 = FabrykaMaterialow.utworz(
        'ksiazka',
        tytul='Pan Tadeusz',
        autor='Adam Mickiewicz',
        rok=1834,
        sygnatura='MIC-PAN-02',
        liczba_stron=400
    )
    czasopismo = FabrykaMaterialow.utworz(
        'czasopismo',
        tytul='National Geographic',
        autor='Redakcja',
        rok=2023,
        sygnatura='NAT-GEO-03',
        numer_wydania=234
    )
    multimedia = FabrykaMaterialow.utworz(
        'multimedia',
        tytul='Python dla każdego',
        autor='Jan Kowalski',
        rok=2022,
        sygnatura='DVD-PYT-04',
        czas_trwania=120
    )

    # Dodanie materiałów do biblioteki
    biblioteka.dodaj_material(ksiazka1)
    biblioteka.dodaj_material(ksiazka2)
    biblioteka.dodaj_material(czasopismo)
    biblioteka.dodaj_material(multimedia)

    # Dodanie czytelników
    czytelnik1 = Czytelnik("Anna", "Nowak")
    czytelnik2 = Czytelnik("Piotr", "Wiśniewski")
    biblioteka.dodaj_czytelnika(czytelnik1)
    biblioteka.dodaj_czytelnika(czytelnik2)

    print("Materiały w bibliotece:")
    # Polimorfizm – wywołanie metody wyswietl_info() dla każdego materiału
    for material in biblioteka.lista_materialow():
        print(f"  - {material.wyswietl_info()}")

    print("\nCzytelnicy:")
    for cz in biblioteka.lista_czytelnikow():
        print(f"  - {cz}")

    # Przykład wypożyczenia
    print("\n--- Wypożyczanie 'SAP-WIE-01' przez Annę Nowak (ID: 1) ---")
    try:
        biblioteka.wypozycz("SAP-WIE-01", czytelnik1.id)
        print("Wypożyczono pomyślnie.")
    except (MaterialNieZnalezionyError, MaterialNieDostepnyError, CzytelnikNieZnalezionyError) as e:
        print(f"Błąd: {e}")

    # Próba ponownego wypożyczenia tego samego
    print("\n--- Próba ponownego wypożyczenia tej samej książki przez Piotra ---")
    try:
        biblioteka.wypozycz("SAP-WIE-01", czytelnik2.id)
    except MaterialNieDostepnyError as e:
        print(f"Oczekiwany błąd: {e}")

    # Wyświetlenie stanu po wypożyczeniu
    print("\nStan po wypożyczeniu:")
    for material in biblioteka.lista_materialow():
        print(f"  - {material.wyswietl_info()}")

    # Zwrot
    print("\n--- Zwrot książki przez Annę ---")
    biblioteka.zwroc("SAP-WIE-01", czytelnik1.id)
    print("Zwrócono pomyślnie.")
    print("Stan po zwrocie:")
    for material in biblioteka.lista_materialow():
        print(f"  - {material.wyswietl_info()}")

    # Próba wypożyczenia nieistniejącego materiału
    print("\n--- Próba wypożyczenia nieistniejącej sygnatury ---")
    try:
        biblioteka.wypozycz("NIE-ISTNIEJE", czytelnik1.id)
    except MaterialNieZnalezionyError as e:
        print(f"Oczekiwany błąd: {e}")

    # Zapis stanu do plików
    biblioteka.zapisz_do_pliku()
    print("\nZapisano stan biblioteki do plików JSON.")

    # Polimorfizm – funkcja przyjmująca listę różnych materiałów
    def wyswietl_wszystkie(lista_materialow):
        print("\n--- Polimorfizm: wyświetlenie wszystkich materiałów za pomocą jednej funkcji ---")
        for m in lista_materialow:
            print(m.wyswietl_info())

    wyswietl_wszystkie(biblioteka.lista_materialow())

    print("\n=== KONIEC DEMONSTRACJI ===")

if __name__ == "__main__":
    main()