from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "mundial_2026_ekipa"

# BAZA MECZÓW
mecze = [
    {"id": 0, "data": "Czwartek 21:00", "gospodarz": "Meksyk 🇲🇽", "gosc": "RPA 🇿🇦", "wynik_g": "", "wynik_b": ""},
    {"id": 1, "data": "Piątek 04:00", "gospodarz": "Korea Południowa 🇰🇷", "gosc": "Czechy 🇨🇿", "wynik_g": "", "wynik_b": ""},
    {"id": 2, "data": "Piątek 21:00", "gospodarz": "Kanada 🇨🇦", "gosc": "Bośnia i Hercegowina 🇧🇦", "wynik_g": "", "wynik_b": ""},
    {"id": 3, "data": "Sobota 03:00", "gospodarz": "USA 🇺🇸", "gosc": "Paragwaj 🇵🇾", "wynik_g": "", "wynik_b": ""},
    {"id": 4, "data": "Sobota 21:00", "gospodarz": "Katar 🇶🇦", "gosc": "Szwajcaria 🇨🇭", "wynik_g": "", "wynik_b": ""},
    {"id": 5, "data": "Niedziela 00:00", "gospodarz": "Brazylia 🇧🇷", "gosc": "Maroko 🇲🇦", "wynik_g": "", "wynik_b": ""},
    {"id": 6, "data": "Niedziela 03:00", "gospodarz": "Haiti 🇭🇹", "gosc": "Szkocja 🏴\u200d☠️", "wynik_g": "", "wynik_b": ""},
]

# LISTA UCZESTNIKÓW (16 OSOB)
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
    "Tomek": {0: (2, 1), 1: (1, 2)}
}

for gracz, m_typy in startowe_typy.items():
    for m_id, (tg, tb) in m_typy.items():
        typy[gracz][m_id]["typ_g"] = str(tg)
        typy[gracz][m_id]["typ_b"] = str(tb)

totale = {gracz: 0 for gracz in lista_graczy}

def przelicz_wszystko():
    for g in lista_graczy: totale[g] = 0
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
                typy[g][m["id"]]["punkty"], typy[g][m["id"]]["kolor"] = 0, "#FFC7CE"
                continue
            tg, tb = int(tg_raw), int(tb_raw)
            if tg == wg and tb == wb: pkt, kol = 3, "#C6EFCE"
            elif (tg > tb and wg > wb) or (tg < tb and wg < wb) or (tg == tb and wg == wb): pkt, kol = 1, "#FFEB9C"
            else: pkt, kol = 0, "#FFC7CE"
            typy[g][m["id"]]["punkty"], typy[g][m["id"]]["kolor"] = pkt, kol
            totale[g] += pkt

przelicz_wszystko()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Decathlon Typer MŚ 2026</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #f4f7f6; margin: 10px; color: #333; }
        .container { max-width: 1000px; background: white; padding: 20px; border-radius: 16px; box-shadow: 0 4px 25px rgba(0,0,0,0.06); margin: 0 auto; }
        .logo-wrapper { text-align: center; margin-bottom: 15px; padding-top: 10px; }
        .logo-img { max-width: 280px; height: auto; }
        h1 { color: #002244; text-align: center; font-size: 20px; margin-top: 5px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase; }
        .lider-box { background: linear-gradient(135deg, #007D8F, #005662); color: white; padding: 12px; border-radius: 10px; text-align: center; font-size: 18px; font-weight: bold; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,125,143,0.2); }
        .login-bar { background: #002244; color: white; padding: 12px; border-radius: 8px; margin-bottom: 20px; text-align: center; font-weight: bold; }
        .login-bar a { color: #00EDFF; text-decoration: none; margin-left: 10px; }
        .login-bar select, .login-bar input, .login-bar button { padding: 4px 8px; border-radius: 4px; border: none; margin: 2px; font-size: 14px; }
        .login-bar button { background: #007D8F; color: white; font-weight: bold; cursor: pointer; transition: 0.2s; }
        .login-bar button:hover { background: #005662; }
        .legend-box { background: #e6f2f4; border-left: 5px solid #007D8F; padding: 12px 15px; border-radius: 8px; margin-bottom: 25px; font-size: 14px; color: #002244; }
        .legend-box ul { margin: 8px 0 0 20px; padding: 0; }
        .legend-box li { margin-bottom: 6px; }
        .badge { display: inline-block; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; margin-right: 5px; }
        .badge-3 { background: #C6EFCE; color: #006100; border: 1px solid #a3d9a5; }
        .badge-1 { background: #FFEB9C; color: #9C6500; border: 1px solid #e0c870; }
        .badge-0 { background: #FFC7CE; color: #9C0006; border: 1px solid #e0a4aa; }
        .mecz-row { background: #ffffff; border: 1px solid #e0e6ed; padding: 15px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }
        .mecz-header { font-weight: bold; color: #007D8F; background: #e6f2f4; padding: 6px 12px; border-radius: 6px; font-size: 14px; display: inline-block; }
        .mecz-wynik-container { margin: 15px 0; font-size: 18px; font-weight: bold; display: flex; align-items: center; gap: 10px; color: #002244; }
        .grid-typy { display: grid; grid-template-columns: repeat(auto-fill, minmax(210px, 1fr)); gap: 8px; margin-top: 15px; }
        .gracz-card { border: 1px solid #e2e8f0; padding: 8px 12px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; font-size: 14px; font-weight: 600; }
        input[type="text"] { width: 35px; padding: 5px; text-align: center; font-size: 14px; border: 2px solid #cbd5e1; border-radius: 6px; font-weight: bold; }
        .btn { background: #007D8F; color: white; padding: 14px 30px; border: none; border-radius: 10px; cursor: pointer; font-size: 16px; font-weight: bold; width: 100%; transition: 0.2s; box-shadow: 0 4px 12px rgba(0,125,143,0.25); }
        .btn:hover { background: #005662; }
        .ranking-sidebar { background: #002244; color: white; padding: 15px; border-radius: 12px; margin-bottom: 25px; }
        .ranking-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(145px, 1fr)); gap: 8px; margin-top: 12px; font-size: 13px; }
        .ranking-item { background: rgba(255,255,255,0.07); padding: 8px; border-radius: 8px; text-align: center; border: 1px solid rgba(255,255,255,0.05); }
    </style>
</head>
<body>
    <div class="container">
        
        <div class="logo-wrapper">
            <svg class="logo-img" viewBox="0 0 350 45" xmlns="http://www.w3.org/2000/svg">
                <path d="M0 0h55.2c16.1 0 26.6 9.4 26.6 22.1s-10.5 22.1-26.6 22.1H0V0zm53.4 34.6c8.5 0 13.5-4.7 13.5-12.5s-5-12.5-13.5-12.5H14.6v25H53.4zM92.3 0h47.2v9.6h-32.6v7.7h29.8v9.5h-29.8v7.7h33.2v10H92.3V0zm94 22.7c0-13.5-10.4-23.4-24.8-23.4-15 0-25 10.3-25 22.8 0 13 10.2 22.4 25.6 22.4 9.9 0 17.2-3.7 21.8-9.4l-7.7-5.5c-3.1 3.8-7.7 5.6-13.6 5.6-8.8 0-14.7-5-15.3-12.5h43.7c.2-.7.3-1.4.3-2.7zm-39.2-4.1c.9-6 6.1-9.9 13.8-9.9 7.3 0 12.6 3.8 13.5 9.9h-27.3zM232.5 44.5l-6.8-10h-23.2v10h-14.6V0h36.7c13.7 0 22.4 7.4 22.4 17.5 0 7.3-4.6 13.1-12.3 15.6l8.8 11.4h-11zm-5.1-27c0-5-3.8-8-9.7-8h-22.1v16h22.1c5.9 0 9.7-3 9.7-8zM263.8 9.6V44.5h-14.6V9.6h-15.3V0h45.2v9.6h-15.3zM302.3 0v44.5H287.7V25.2h-21.7v19.3h-14.6V0h14.6v15.7h21.7V0h14.6zm14.1 0h14.6v34.9h27.4v9.6h-42V0zm51.4 22.2c0 13-10.3 22.8-25.2 22.8-15 0-25.2-9.8-25.2-22.8C317.4 9.3 327.6-.5 342.6-.5c15 0 25.2 9.8 25.2 22.7zm-35.4.1c0 7.9 4.6 13.2 10.2 13.2 5.6 0 10.2-5.3 10.2-13.2 0-7.8-4.6-13.1-10.2-13.1-5.6 0-10.2 5.3-10.2 13.1z" fill="#002244"/>
                <path d="M407.3 22.2c0-11-7-19.6-18.7-21.7-1.3-.2-2.7-.3-4.1-.3-14.7 0-25.1 11.2-25.1 22.5 0 10.3 7 19.3 18.2 21.5 1.5.3 3 .4 4.5.4 15.1 0 25.2-11.2 25.2-22.4zm-22.8 13.2c-5.7 0-9.8-5.3-9.8-13.1 0-7.5 3.9-13.2 10-13.2 5.5 0 9.6 5.4 9.6 13.1a11.2 11.2 0 0 1-.7 3.9c-1.3 3.6-4.5 9.3-9.1 9.3z" fill="#00EDFF"/>
            </svg>
            <h1>🏆 OFICJALNY TYPER EKIPY 🏆</h1>
        </div>
        
        <div class="login-bar">
            {% if session.get('user') %}
                Zalogowany: <span style="color:#00EDFF; font-size:18px;">{{ session['user'] }}</span> | <a href="/logout">Wyloguj się</a>
            {% else %}
                <form action="/login" method="POST" style="display:inline;">
                    Strefa Gracza: 
                    <select name="user_name">
                        <option value="Admin">Panel Admina</option>
                        {% for g in lista_graczy %}<option value="{{ g }}">{{ g }}</option>{% endfor %}
                    </select>
                    Kod dostępu: <input type="password" name="pass" placeholder="****" style="width:70px;">
                    <button type="submit">Wejdź</button>
                </form>
            {% endif %}
        </div>

        <div class="lider-box">👑 AKTUALNY LIDER: {{ lider }}</div>

        <div class="legend-box">
            <b>Zasady punktacji:</b>
            <ul>
                <li><span class="badge badge-3">3 pkt</span> Idealnie trafiony wynik <i>(np. obstawiasz 2:1, mecz kończy się 2:1)</i></li>
                <li><span class="badge badge-1">1 pkt</span> Trafiony zwycięzca lub remis <i>(np. obstawiasz wygraną 2:0, ale mecz kończy się 1:0)</i></li>
                <li><span class="badge badge-0">0 pkt</span> Całkowity błąd <i>(np. obstawiasz wygraną gospodarzy, a wygrywają goście)</i></li>
            </ul>
        </div>

        <div class="ranking-sidebar">
            <div style="font-weight: bold; text-align: center; letter-spacing: 1px;">📊 OFICJALNA TABELA GENERALNA</div>
            <div class="ranking-grid">
                {% for gracz, pkt in totale_sorted %}
                <div class="ranking-item"><b>{{ loop.index }}. {{ gracz }}</b><br><span style="color:#00EDFF; font-size:16px;">{{ pkt }} pkt</span></div>
                {% endfor %}
            </div>
        </div>

        <form method="POST">
            {% for m in mecze %}
            <div class="mecz-row">
                <div class="mecz-header">⏰ {{ m.data }}</div>
                <div style="margin: 15px 0; font-size: 18px; font-weight: bold; color: #002244;">
                    {{ m.gospodarz }} 
                    <input type="text" name="wynik_g_{{ m.id }}" value="{{ m.wynik_g }}" {% if session.get('user') != 'Admin' %}readonly style="background:#eee;"{% endif %} style="border: 2px solid #002244; width: 40px;">
                    :
                    <input type="text" name="wynik_b_{{ m.id }}" value="{{ m.wynik_b }}" {% if session.get('user') != 'Admin' %}readonly style="background:#eee;"{% endif %} style="border: 2px solid #002244; width: 40px;">
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
    lider = f"{totale_sorted[0][0]} ({totale_sorted[0][1]} pkt)" if totale_sorted[0][1] > 0 else "Czekamy na wyniki!"
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
