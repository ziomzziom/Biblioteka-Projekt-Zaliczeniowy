"""Własne wyjątki dla systemu bibliotecznego."""

class BibliotekaError(Exception):
    """Klasa bazowa dla wyjątków bibliotecznych."""
    pass

class MaterialNieDostepnyError(BibliotekaError):
    """Wyjątek rzucany gdy materiał nie jest dostępny do wypożyczenia."""
    def __init__(self, sygnatura: str):
        self.sygnatura = sygnatura
        super().__init__(f"Materiał o sygnaturze '{sygnatura}' jest niedostępny.")

class CzytelnikNieZnalezionyError(BibliotekaError):
    """Wyjątek rzucany gdy czytelnik nie istnieje."""
    def __init__(self, czytelnik_id: int):
        self.czytelnik_id = czytelnik_id
        super().__init__(f"Czytelnik o ID '{czytelnik_id}' nie istnieje.")

class MaterialNieZnalezionyError(BibliotekaError):
    """Wyjątek rzucany gdy materiał o podanej sygnaturze nie istnieje."""
    def __init__(self, sygnatura: str):
        self.sygnatura = sygnatura
        super().__init__(f"Materiał o sygnaturze '{sygnatura}' nie istnieje w bibliotece.")