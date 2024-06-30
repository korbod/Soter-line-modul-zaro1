from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd

app = Flask(__name__)

# Globális változó a DataFrame tárolására
db = None

def load_data():
    global db
    db = pd.read_excel('film_adatok.xlsx')

# Adatbázis betöltése indításkor
load_data()

# Új film hozzáadása
@app.route('/add_film', methods=['POST'])
def add_film():
    global db
    cim = request.form['cim']
    gyartasi_ev = int(request.form['gyartasi_ev'])
    megtekintes_ev = int(request.form['megtekintes_ev'])
    ertekeles = int(request.form['ertekeles'])

    # Ellenőrzés, hogy létezik-e már a film
    if any(db['Cím'] == cim):
        return 'A film már létezik az adatbázisban!'
    
    # Új sor hozzáadása az adatbázishoz
    new_film = pd.DataFrame({'Cím': [cim], 'Gyártási év': [gyartasi_ev], 'Megtekintés éve': [megtekintes_ev], 'Értékelés': [ertekeles]})
    db = db._append(new_film, ignore_index=True)
    
    # Frissített adatok mentése az Excel fájlba
    db.to_excel('film_adatok.xlsx', index=False)
    
    return redirect('/')

# Filmek listázása
@app.route('/')
def index():
    global db
    filmek = db.to_dict(orient='records')
    return render_template('index.html', filmek=filmek)

# Film törlése
@app.route('/delete/<cim>')
def delete_film(cim):
    global db
    db = db[db['Cím'] != cim]
    db.to_excel('film_adatok.xlsx', index=False)
    return redirect('/')

@app.route('/statistics_year', methods=['GET'])
def statistics_film_year():
    global db
    evszam = request.args.get('evszam', type=int)
    results = db.loc[db['Gyártási év'] == evszam].to_dict(orient='records')
    return jsonify(results)


# Statisztika készítése értékelés alapján
@app.route('/statistics_rating', methods=['GET'])
def statistics_film_rating():
    global db
    ertekeles = request.args.get('ertekeles', type=int)
    results = db.loc[db['Értékelés'] == ertekeles].to_dict(orient='records')
    return jsonify(results)

#test github


if __name__ == '__main__':
    app.run(debug=True)
