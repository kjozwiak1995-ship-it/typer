from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "mundial_2026_ekipa"

# BAZA MECZÓW
mecze = [
    {"id": 0, "data": "Czwartek (Dzisiaj) 21:00", "gospodarz": "Meksyk 🇲🇽", "gosc": "RPA 🇿🇦", "wynik_g": "", "wynik_b": ""},
    {"id": 1, "data": "Piątek 04:00", "gospodarz": "Korea Południowa 🇰🇷", "gosc": "Czechy 🇨🇿", "wynik_g": "", "wynik_b": ""},
    {"id": 2, "data": "Piątek 21:00", "gospodarz": "Kanada 🇨🇦", "gosc": "Bośnia i Hercegowina 🇧🇦", "wynik_g": "", "wynik_b": ""},
    {"id": 3, "data": "Sobota 03:00", "gospodarz": "USA 🇺🇸", "gosc": "Paragwaj 🇵🇾", "wynik_g": "", "wynik_b": ""},
    {"id": 4, "data": "Sobota 21:00", "gospodarz": "Katar 🇶🇦", "gosc": "Szwajcaria 🇨🇭", "wynik_g": "", "wynik_b": ""},
    {"id": 5, "data": "Niedziela 00:00", "gospodarz": "Brazylia 🇧🇷", "gosc": "Maroko 🇲🇦", "wynik_g": "", "wynik_b": ""},
    {"id": 6, "data": "Niedziela 03:00", "gospodarz": "Haiti 🇭🇹", "gosc": "Szkocja 🏴\u200d☠️", "wynik_g": "", "wynik_b": ""},
]

# LISTA UCZESTNIKÓW (TERAZ JEST ICH 16 - DOPISANY TOMEK)
lista_graczy = [
    "Andrzej", "Jakub", "Daniel", "Klaudia T", "Agnieszka",
    "Patrycja A", "Julia", "Marzena", "Malina", "Patrycja W",
    "Agata", "Marek", "Kamil O", "Kamil K", "Michał", "Tomek"
]

# STARTOWE TYPY
typy = {gracz: {m["id"]: {"typ_g": "", "typ_b": "", "punkty": 0, "kolor": "white"} for m in mecze} for gracz in lista_graczy}
startowe_typy = {
    "Andrzej": {0: (3, 1), 1: (2, 1)}, "Jakub": {0: (1, 1), 1: (1, 1)}, "Daniel": {0: (2, 0), 1: (2, 1)},
    "Klaudia T": {0: (2, 1), 1: (1, 0)}, "Agnieszka": {0: (2, 0), 1: (1, 1)}, "Patrycja A": {0: (2, 0), 1: (1, 1)},
    "Julia": {0: (2, 1), 1: (0, 1)}, "Marzena": {0: (3, 1), 1: (0, 3)}, "Malina": {0: (3, 1), 1: (1, 2)},
    "Patrycja W": {0: (4, 0), 1: (1, 3)}, "Agata": {0: (3, 0), 1: (0, 2)}, "Marek": {0: (1, 0), 1: (2, 1)},
    "Kamil O": {0: (3, 0), 1: (1, 1)}, "Kamil K": {0: (3, 0), 1: (0, 2)}, "Michał": {0: (2, 1), 1: (1, 0)},
    "Tomek": {0: (2, 1), 1: (1, 2)} # Dorzucone typy Tomka!
}

for gracz, m_typy in startowe_typy.items():
    for m_id, (tg, tb) in m_typy.items():
        typy[gracz][m_id]["typ_g"] = str(tg)
        typy[gracz][m_id]["typ_b"] = str(tb)

totale = {gracz: 0 for gracz in lista_graczy}

def przelicz_wszystko():
    for g in lista_graczy: 
        totale[g] = 0
    for m in mecze:
        wg_raw, wb_raw = str(m["wynik_g"]), str(m["wynik_b"])
        if wg_raw == "" or wb_raw == "":
            for g in lista_graczy:
                typy[g][m["id"]]["punkty"] = 0
                typy[g][m["id"]]["kolor"] = "white" if str(typy[g][m["id"]]["typ_g"]) != "" else "#f3f4f6"
            continue
        wg, wb = int(wg_raw), int(wb_raw)
        for g in lista_graczy:
            tg_raw, tb_raw = str(typy[g][m["id"]]["typ_g"]), str(typy[g][m["id"]]["typ_b"])
            if tg_raw == "" or tb_raw == "":
                typy[g][m["id"]]["punkty"] = 0
                typy[g][m["id"]]["kolor"] = "#FFC7CE"
                continue
            tg, tb = int(tg_raw), int(tb_raw)
            if tg == wg and tb == wb:
                pkt, kol = 3, "#C6EFCE"
            elif (tg > tb and wg > wb) or (tg < tb and wg < wb) or (tg == tb and wg == wb):
                pkt, kol = 1, "#FFEB9C"
            else:
                pkt, kol = 0, "#FFC7CE"
            typy[g][m["id"]]["punkty"] = pkt
            typy[g][m["id"]]["kolor"] = kol
            totale[g] += pkt

przelicz_wszystko()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Oficjalny Typer MŚ 2026</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #f0f4f8; margin: 10px; color: #333; }
        .container { max-width: 1000px; background: white; padding: 20px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin: 0 auto; }
        h1 { color: #1F497D; text-align: center; font-size: 24px; }
        .lider-box { background: linear-gradient(135deg, #FFD700, #FFA500); color: white; padding: 12px; border-radius: 10px; text-align: center; font-size: 18px; font-weight: bold; margin-bottom: 20px; }
        .login-bar { background: #e2e8f0; padding: 10px; border-radius: 8px; margin-bottom: 20px; text-align: center; font-weight: bold; }
        .mecz-row { background: #f9fbfd; border: 1px solid #dbe3ec; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        .mecz-header { font-weight: bold; color: #1F497D; background: #eef3f8; padding: 5px; border-radius: 4px; font-size: 14px; }
        .grid-typy { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 8px; margin-top: 10px; }
        .gracz-card { border: 1px solid #ddd; padding: 6px 10px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; }
        input[type="text"] { width: 35px; padding: 4px; text-align: center; font-size: 14px; border: 1px solid #ccc; border-radius: 4px; }
        .btn { background: #22c55e; color: white; padding: 12px 30px; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; width: 100%; }
        .ranking-sidebar { background: #1F497D; color: white; padding: 12px; border-radius: 10px; margin-bottom: 20px; }
        .ranking-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 8px; margin-top: 10px; font-size: 13px; }
        .ranking-item { background: rgba(255,255,255,0.1); padding: 6px; border-radius: 6px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏆 TYPER MISTRZOSTW ŚWIATA 2026 🏆</h1>
        
        <div class="login-bar">
            {% if session.get('user') %}
                Zalogowany jako: <span style="color:#1F497D; font-size:18px;">{{ session['user'] }}</span> | <a href="/logout">Wyloguj</a>
            {% else %}
                <form action="/login" method="POST" style="display:inline;">
                    Zaloguj się: 
                    <select name="user_name">
                        <option value="Admin">--- ADMIN (Ty) ---</option>
                        {% for g in lista_graczy %}<option value="{{ g }}">{{ g }}</option>{% endfor %}
                    </select>
                    Hasło: <input type="password" name="pass" placeholder="Kod" style="width:70px; padding:3px;">
                    <button type="submit">Wejdź</button>
                </form>
                <span style="font-size:11px; display:block; color:#666; margin-top:5px;">(Kod gracza: 1234 | Twój kod Admina: admin2026)</span>
            {% endif %}
        </div>

        <div class="lider-box">👑 LIDER TURNIEJU: {{ lider }}</div>

        <div class="ranking-sidebar">
            <div style="font-weight: bold; text-align: center;">📊 TABELA GENERALNA</div>
            <div class="ranking-grid">
                {% for gracz, pkt in totale_sorted %}
                <div class="ranking-item"><b>{{ loop.index }}. {{ gracz }}</b><br><span style="color:#FFD700; font-size:16px;">{{ pkt }} pkt</span></div>
                {% endfor %}
            </div>
        </div>

        <form method="POST">
            {% for m in mecze %}
            <div class="mecz-row">
                <div class="mecz-header">⏰ {{ m.data }}</div>
                <div style="margin: 10px 0; font-size: 16px; font-weight: bold;">
                    {{ m.gospodarz }} 
                    <input type="text" name="wynik_g_{{ m.id }}" value="{{ m.wynik_g }}" {% if session.get('user') != 'Admin' %}readonly style="background:#eee;"{% endif %} style="border: 2px solid #1F497D;">
                    :
                    <input type="text" name="wynik_b_{{ m.id }}" value="{{ m.wynik_b }}" {% if session.get('user') != 'Admin' %}readonly style="background:#eee;"{% endif %} style="border: 2px solid #1F497D;">
                    {{ m.gosc }}
                </div>
                
                <div class="grid-typy">
                    {% for gracz in lista_graczy %}
                    {% set g_typ = typy[gracz][m.id] %}
                    <div class="gracz-card" style="background-color: {{ g_typ.kolor }};">
                        <span>{{ gracz }}</span>
                        <div>
                            <input type="text" name="typ_g_{{ gracz }}_{{ m.id }}" value="{{ g_typ.typ_g }}" {% if session.get('user') != gracz and session.get('user') != 'Admin' %}readonly style="background:rgba(0,0,0,0.05); border:none;"{% endif %}>
                            :
                            <input type="text" name="typ_b_{{ gracz }}_{{ m.id }}" value="{{ g_typ.typ_b }}" {% if session.get('user') != gracz and session.get('user') != 'Admin' %}readonly style="background:rgba(0,0,0,0.05); border:none;"{% endif %}>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endfor %}
            
            {% if session.get('user') %}
            <button type="submit" class="btn">🚀 ZAPISZ MOJE ZMIANY / WYNIKI</button>
            {% endif %}
        </form>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if session.get("user") == "Admin":
            for m in mecze:
                m["wynik_g"] = request.form.get(f"wynik_g_{m.id}", m["wynik_g"])
                m["wynik_b"] = request.form.get(f"wynik_b_{m.id}", m["wynik_b"])
        
        current_user = session.get("user")
        if current_user:
            for m in mecze:
                for gracz in lista_graczy:
                    if current_user == "Admin" or current_user == gracz:
                        tg = request.form.get(f"typ_g_{gracz}_{m.id}")
                        tb = request.form.get(f"typ_b_{gracz}_{m.id}")
                        if tg is not None: typy[gracz][m["id"]]["typ_g"] = tg
                        if tb is not None: typy[gracz][m["id"]]["typ_b"] = tb
            przelicz_wszystko()
            
    totale_sorted = sorted(totale.items(), key=lambda x: x[1], reverse=True)
    lider = f"{totale_sorted[0][0]} ({totale_sorted[0][1]} pkt)" if totale_sorted[0][1] > 0 else "Czekamy na pierwsze mecze!"
    return render_template_string(HTML_TEMPLATE, mecze=mecze, lista_graczy=lista_graczy, typy=typy, totale_sorted=totale_sorted, lider=lider)

@app.route("/login", methods=["POST"])
def login():
    user = request.form.get("user_name")
    pas = request.form.get("pass")
    if user == "Admin" and pas == "admin2026": session["user"] = "Admin"
    elif user in lista_graczy and pas == "1234": session["user"] = user
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
