from flask import Flask, render_template, request, redirect, url_for, flash
from biblioteka import Biblioteka
from czytelnik import Czytelnik
from fabryka import FabrykaMaterialow
from exceptions import MaterialNieDostepnyError, MaterialNieZnalezionyError, CzytelnikNieZnalezionyError

app = Flask(__name__)
app.secret_key = 'biblioteka-secret-key'

# Singleton – ta instancja będzie używana w całej aplikacji
biblioteka = Biblioteka()
biblioteka.wczytaj_z_pliku()


@app.route('/')
def index():
    materialy = biblioteka.lista_materialow()
    czytelnicy = biblioteka.lista_czytelnikow()
    return render_template('index.html', materialy=materialy, czytelnicy=czytelnicy)


@app.route('/borrow', methods=['GET', 'POST'])
def borrow():
    if request.method == 'POST':
        sygnatura = request.form.get('sygnatura', '').strip()
        czytelnik_id_str = request.form.get('czytelnik_id', '').strip()

        if not sygnatura or not czytelnik_id_str:
            flash('Wypełnij wszystkie pola.', 'danger')
            return redirect(url_for('borrow'))

        try:
            czytelnik_id = int(czytelnik_id_str)
        except ValueError:
            flash('ID czytelnika musi być liczbą.', 'danger')
            return redirect(url_for('borrow'))

        try:
            biblioteka.wypozycz(sygnatura, czytelnik_id)
            biblioteka.zapisz_do_pliku()
            flash(f'Pomyślnie wypożyczono materiał "{sygnatura}".', 'success')
        except MaterialNieZnalezionyError as e:
            flash(str(e), 'danger')
        except MaterialNieDostepnyError as e:
            flash(str(e), 'danger')
        except CzytelnikNieZnalezionyError as e:
            flash(str(e), 'danger')

        return redirect(url_for('index'))

    materialy = biblioteka.lista_materialow()
    czytelnicy = biblioteka.lista_czytelnikow()
    return render_template('borrow.html', materialy=materialy, czytelnicy=czytelnicy)


@app.route('/return', methods=['GET', 'POST'])
def return_material():
    if request.method == 'POST':
        sygnatura = request.form.get('sygnatura', '').strip()

        if not sygnatura:
            flash('Wybierz materiał do zwrotu.', 'danger')
            return redirect(url_for('return_material'))

        material = biblioteka.znajdz_material(sygnatura)
        if material is None:
            flash(f'Materiał o sygnaturze "{sygnatura}" nie istnieje.', 'danger')
            return redirect(url_for('return_material'))

        if not material.wypozyczony:
            flash(f'Materiał "{sygnatura}" nie jest wypożyczony.', 'warning')
            return redirect(url_for('return_material'))

        czytelnik_id = material.wypozyczony_przez
        try:
            biblioteka.zwroc(sygnatura, czytelnik_id)
            biblioteka.zapisz_do_pliku()
            flash(f'Pomyślnie zwrócono materiał "{sygnatura}".', 'success')
        except (MaterialNieZnalezionyError, CzytelnikNieZnalezionyError) as e:
            flash(str(e), 'danger')

        return redirect(url_for('index'))

    materialy = [m for m in biblioteka.lista_materialow() if m.wypozyczony]
    return render_template('return.html', materialy=materialy)


@app.route('/add_material', methods=['GET', 'POST'])
def add_material():
    if request.method == 'POST':
        typ = request.form.get('typ', '').strip().lower()
        tytul = request.form.get('tytul', '').strip()
        autor = request.form.get('autor', '').strip()
        rok_str = request.form.get('rok', '').strip()
        sygnatura = request.form.get('sygnatura', '').strip()

        if not all([typ, tytul, autor, rok_str, sygnatura]):
            flash('Wypełnij wszystkie wymagane pola.', 'danger')
            return redirect(url_for('add_material'))

        try:
            rok = int(rok_str)
        except ValueError:
            flash('Rok musi być liczbą.', 'danger')
            return redirect(url_for('add_material'))

        dane = {
            'tytul': tytul,
            'autor': autor,
            'rok': rok,
            'sygnatura': sygnatura,
        }

        if typ == 'ksiazka':
            liczba_stron_str = request.form.get('liczba_stron', '0').strip()
            try:
                dane['liczba_stron'] = int(liczba_stron_str) if liczba_stron_str else 0
            except ValueError:
                flash('Liczba stron musi być liczbą.', 'danger')
                return redirect(url_for('add_material'))
        elif typ == 'czasopismo':
            numer_wydania_str = request.form.get('numer_wydania', '1').strip()
            try:
                dane['numer_wydania'] = int(numer_wydania_str) if numer_wydania_str else 1
            except ValueError:
                flash('Numer wydania musi być liczbą.', 'danger')
                return redirect(url_for('add_material'))
        elif typ == 'multimedia':
            czas_trwania_str = request.form.get('czas_trwania', '0').strip()
            try:
                dane['czas_trwania'] = int(czas_trwania_str) if czas_trwania_str else 0
            except ValueError:
                flash('Czas trwania musi być liczbą.', 'danger')
                return redirect(url_for('add_material'))
        else:
            flash('Nieznany typ materiału.', 'danger')
            return redirect(url_for('add_material'))

        try:
            material = FabrykaMaterialow.utworz(typ, **dane)
            biblioteka.dodaj_material(material)
            biblioteka.zapisz_do_pliku()
            flash(f'Dodano materiał: {material.wyswietl_info()}', 'success')
        except ValueError as e:
            flash(str(e), 'danger')

        return redirect(url_for('index'))

    return render_template('add_material.html')


@app.route('/add_reader', methods=['GET', 'POST'])
def add_reader():
    if request.method == 'POST':
        imie = request.form.get('imie', '').strip()
        nazwisko = request.form.get('nazwisko', '').strip()

        if not imie or not nazwisko:
            flash('Wypełnij wszystkie pola.', 'danger')
            return redirect(url_for('add_reader'))

        czytelnik = Czytelnik(imie, nazwisko)
        biblioteka.dodaj_czytelnika(czytelnik)
        biblioteka.zapisz_do_pliku()
        flash(f'Dodano czytelnika: {czytelnik}', 'success')
        return redirect(url_for('index'))

    return render_template('add_reader.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
