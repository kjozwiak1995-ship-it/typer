from flask import Flask, render_template_string, request, session, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "mundial_2026_ekipa"

# BAZA MECZÓW (Z WPROWADZONYMI OFICJALNYMI WYNIKAMI DLA MECZU 0 i 1)
mecze = [
    {"id": 0, "data": "Czwartek 21:00", "sys_data": "2026-06-11 21:00", "gospodarz": "Meksyk 🇲🇽", "gosc": "RPA 🇿🇦", "wynik_g": "2", "wynik_b": "0"},
    {"id": 1, "data": "Piątek 04:00", "sys_data": "2026-06-12 04:00", "gospodarz": "Korea Południowa 🇰🇷", "gosc": "Czechy 🇨🇿", "wynik_g": "2", "wynik_b": "1"},
    {"id": 2, "data": "Piątek 21:00", "sys_data": "2026-06-12 21:00", "gospodarz": "Kanada 🇨🇦", "gosc": "Bośnia i Hercegowina 🇧🇦", "wynik_g": "", "wynik_b": ""},
    {"id": 3, "data": "Sobota 03:00", "sys_data": "2026-06-13 03:00", "gospodarz": "USA 🇺🇸", "gosc": "Paragwaj 🇵🇾", "wynik_g": "", "wynik_b": ""},
    {"id": 4, "data": "Sobota 21:00", "sys_data": "2026-06-13 21:00", "gospodarz": "Katar 🇶🇦", "gosc": "Szwajcaria 🇨🇭", "wynik_g": "", "wynik_b": ""},
    {"id": 5, "data": "Niedziela 00:00", "sys_data": "2026-06-14 00:00", "gospodarz": "Brazylia 🇧🇷", "gosc": "Maroko 🇲🇦", "wynik_g": "", "wynik_b": ""},
    {"id": 6, "data": "Niedziela 03:00", "sys_data": "2026-06-14 03:00", "gospodarz": "Haiti 🇭🇹", "gosc": "Szkocja 🏴\u200d☠️", "wynik_g": "", "wynik_b": ""},
]

# LISTA UCZESTNIKÓW
lista_graczy = [
    "Andrzej", "Jakub", "Daniel", "Klaudia T", "Agnieszka",
    "Patrycja A", "Julia", "Marzena", "Malina", "Patrycja W",
    "Agata", "Marek", "Kamil O", "Kamil K", "Michał", "Tomek"
]

# STARTOWE TYPY
startowe_typy = {
    "Andrzej": {0: (3, 1), 1: (2, 1)}, "Jakub": {0: (1, 1), 1: (1, 1)}, "Daniel": {0: (2, 0), 1: (2, 1)},
    "Klaudia T": {0: (2, 1), 1: (1, 0)}, "Agnieszka": {0: (2, 0), 1: (1, 1)}, "Patrycja A": {0: (2, 0), 1: (1, 1)},
    "Julia": {0: (2, 1), 1: (0, 1)}, "Marzena": {0: (3, 1), 1: (0, 3)}, "Malina": {0: (3, 1), 1: (1, 2)},
    "Patrycja W": {0: (4, 0), 1: (1, 3)}, "Agata": {0: (3, 0), 1: (0, 2)}, "Marek": {0: (1, 0), 1: (2, 1)},
    "Kamil O": {0: (3, 0), 1: (1, 1)}, "Kamil K": {0: (3, 0), 1: (0, 2)}, "Michał": {0: (2, 1), 1: (1, 0)},
    "Tomek": {0: (2, 1), 1: (1, 2)}
}

# INICJALIZACJA BAZY
typy = {gracz: {m["id"]: {"typ_g": "", "typ_b": "", "punkty": 0, "kolor": "white"} for m in mecze} for gracz in lista_graczy}
for gracz, m_typy in startowe_typy.items():
    for m_id, (tg, tb) in m_typy.items():
        typy[gracz][m_id]["typ_g"] = str(tg)
        typy[gracz][m_id]["typ_b"] = str(tb)

totale = {gracz: 0 for gracz in lista_graczy}

# PANCERNE PRZELICZANIE
def przelicz_wszystko():
    for g in lista_graczy: totale[g] = 0
    for m in mecze:
        wg_raw, wb_raw = str(m["wynik_g"]).strip(), str(m["wynik_b"]).strip()
        
        if not wg_raw.isdigit() or not wb_raw.isdigit():
            for g in lista_graczy:
                typy[g][m["id"]]["punkty"] = 0
                typy[g][m["id"]]["kolor"] = "white" if str(typy[g][m["id"]]["typ_g"]).strip() != "" else "#f3f4f6"
            continue
            
        wg, wb = int(wg_raw), int(wb_raw)
        
        for g in lista_graczy:
            tg_raw, tb_raw = str(typy[g][m["id"]]["typ_g"]).strip(), str(typy[g][m["id"]]["typ_b"]).strip()
            
            if not tg_raw.isdigit() or not tb_raw.isdigit():
                typy[g][m["id"]]["punkty"] = 0
                typy[g][m["id"]]["kolor"] = "#FFC7CE" if (tg_raw != "" or tb_raw != "") else "#f3f4f6"
                continue
                
            tg, tb = int(tg_raw), int(tb_raw)
            if tg == wg and tb == wb: pkt, kol = 3, "#C6EFCE"
            elif (tg > tb and wg > wb) or (tg < tb and wg < wb) or (tg == tb and wg == wb): pkt, kol = 1, "#FFEB9C"
            else: pkt, kol = 0, "#FFC7CE"
            
            typy[g][m["id"]]["punkty"] = pkt
            typy[g][m["id"]]["kolor"] = kol
            totale[g] += pkt

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Decathlon Typer MŚ 2026</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #f4f7f6; margin: 10px; color: #333; }
        .container { max-width: 1000px; background: white; padding: 20px; border-radius: 16px; box-shadow: 0 4px 25px rgba(0,0,0,0.06); margin: 0 auto; }
        .logo-wrapper { text-align: center; margin-bottom: 25px; padding-top: 10px; }
        h1 { color: #002244; text-align: center; font-size: 24px; margin-top: 5px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase; }
        .alert-success { background-color: #d4edda; color: #155724; padding: 12px; text-align: center; border-radius: 8px; margin-bottom: 20px; border: 1px solid #c3e6cb; font-weight: bold; font-size: 16px; box-shadow: 0 2px 10px rgba(40,167,69,0.1); }
        .login-bar { background: #002244; color: white; padding: 12px; border-radius: 8px; margin-bottom: 20px; text-align: center; font-weight: bold; }
        .login-bar a { color: #00EDFF; text-decoration: none; margin-left: 10px; }
        .login-bar select, .login-bar input, .login-bar button { padding: 4px 8px; border-radius: 4px; border: none; margin: 2px; font-size: 14px; }
        .login-bar button { background: #007D8F; color: white; font-weight: bold; cursor: pointer; transition: 0.2s; }
        .legend-box { background: #e6f2f4; border-left: 5px solid #007D8F; padding: 12px 15px; border-radius: 8px; margin-bottom: 25px; font-size: 14px; color: #002244; }
        .legend-box ul { margin: 8px 0 0 20px; padding: 0; }
        .legend-box li { margin-bottom: 6px; }
        .badge { display: inline-block; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; margin-right: 5px; }
        .badge-3 { background: #C6EFCE; color: #006100; border: 1px solid #a3d9a5; }
        .badge-1 { background: #FFEB9C; color: #9C6500; border: 1px solid #e0c870; }
        .badge-0 { background: #FFC7CE; color: #9C0006; border: 1px solid #e0a4aa; }
        
        /* STYLIZACJA PODIUM DLA TOP 3 */
        .podium-wrap { display: flex; justify-content: center; align-items: flex-end; gap: 10px; margin-bottom: 25px; text-align: center; color: white; font-weight: bold; }
        .podium-block { width: 31%; border-radius: 12px 12px 0 0; border: 1px solid rgba(255,255,255,0.1); padding: 15px 5px; position: relative; }
        .p-name { font-size: 14px; margin: 5px 0; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .p-pts { color: #00EDFF; font-size: 18px; font-weight: 800; display: block; }
        
        .p-1 { height: 140px; background: linear-gradient(180deg, #FFD700, #007D8F); border-top: 5px solid #FFD700; box-shadow: 0 -4px 15px rgba(255,215,0,0.3); order: 2;}
        .p-1 .p-rank { font-size: 30px; position: absolute; top: -20px; left: 50%; transform: translateX(-50%); }
        
        .p-2 { height: 110px; background: linear-gradient(180deg, #C0C0C0, #002244); border-top: 5px solid #C0C0C0; order: 1;}
        .p-2 .p-rank { font-size: 24px; color: #C0C0C0; }
        
        .p-3 { height: 90px; background: linear-gradient(180deg, #CD7F32, #002244); border-top: 5px solid #CD7F32; order: 3;}
        .p-3 .p-rank { font-size: 22px; color: #CD7F32; }

        .ranking-sidebar { background: #002244; color: white; padding: 15px; border-radius: 12px; margin-bottom: 25px; }
        .ranking-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(145px, 1fr)); gap: 8px; margin-top: 12px; font-size: 13px; }
        .ranking-item { background: rgba(255,255,255,0.07); padding: 8px; border-radius: 8px; text-align: center; border: 1px solid rgba(255,255,255,0.05); }
        
        .mecz-row { background: #ffffff; border: 1px solid #e0e6ed; padding: 15px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }
        .mecz-header { font-weight: bold; color: #007D8F; background: #e6f2f4; padding: 6px 12px; border-radius: 6px; font-size: 14px; display: inline-block; }
        .grid-typy { display: grid; grid-template-columns: repeat(auto-fill, minmax(210px, 1fr)); gap: 8px; margin-top: 15px; }
        .gracz-card { border: 1px solid #e2e8f0; padding: 8px 12px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; font-size: 14px; font-weight: 600; }
        input[type="text"] { width: 35px; padding: 5px; text-align: center; font-size: 14px; border: 2px solid #cbd5e1; border-radius: 6px; font-weight: bold; }
        .btn { background: #007D8F; color: white; padding: 14px 30px; border: none; border-radius: 10px; cursor: pointer; font-size: 16px; font-weight: bold; width: 100%; transition: 0.2s; box-shadow: 0 4px 12px rgba(0,125,143,0.25); }
        .admin-backup-box { background: #fff3cd; border: 2px dashed #ffc107; padding: 15px; border-radius: 12px; margin-top: 30px; color: #856404; font-size: 12px; }
        .admin-backup-box pre { background: #f8f9fa; padding: 10px; border-radius: 6px; border: 1px solid #ced4da; overflow-x: auto; color: #333; font-family: monospace; max-height: 150px; }
    </style>
</head>
<body>
    <div class="container">
        
        <div class="logo-wrapper">
            <h1>🏆 TYPER EKIPY 🏆</h1>
        </div>

        {% if wiadomosc %}
        <div class="alert-success">
            {{ wiadomosc }}
        </div>
        {% endif %}
        
        <div class="login-bar">
            {% if session.get('user') %}
                Zalogowany: <span style="color:#00EDFF; font-size:18px;">{{ session['user'] }}</span> | <a href="/logout">Wyloguj się</a>
            {% else %}
                <form action="/login" method="POST" style="display:inline;">
                    Gracz: 
                    <select name="user_name">
                        <option value="Admin">--- ADMIN ---</option>
                        {% for g in lista_graczy %}<option value="{{ g }}">{{ g }}</option>{% endfor %}
                    </select>
                    Kod: <input type="password" name="pass" placeholder="****" style="width:50px;">
                    <button type="submit">Wejdź</button>
                </form>
            {% endif %}
        </div>

        <div class="legend-box">
            <b>Zasady punktacji:</b>
            <ul>
                <li><span class="badge badge-3">3 pkt</span> Idealnie trafiony wynik</li>
                <li><span class="badge badge-1">1 pkt</span> Trafiony zwycięzca lub remis</li>
                <li><span class="badge badge-0">0 pkt</span> Całkowity błąd</li>
            </ul>
        </div>

        <div class="ranking-sidebar">
            <div style="font-weight: bold; text-align: center; letter-spacing: 1px;">📊 OFICJALNY RANKING</div>
            
            <div class="podium-wrap">
                <div class="podium-block p-2">
                    <div class="p-rank">2</div>
                    <span class="p-name">{{ podium[1][0] }}</span>
                    <span class="p-pts">{{ podium[1][1] }} pkt</span>
                </div>
                <div class="podium-block p-1">
                    <div class="p-rank">👑</div>
                    <span class="p-name">{{ podium[0][0] }}</span>
                    <span class="p-pts">{{ podium[0][1] }} pkt</span>
                </div>
                <div class="podium-block p-3">
                    <div class="p-rank">3</div>
                    <span class="p-name">{{ podium[2][0] }}</span>
                    <span class="p-pts">{{ podium[2][1] }} pkt</span>
                </div>
            </div>

            <div class="ranking-grid">
                {% for gracz, pkt in totale_sorted %}
                <div class="ranking-item"><b>{{ loop.index }}. {{ gracz }}</b><br><span style="color:#00EDFF; font-size:16px;">{{ pkt }} pkt</span></div>
                {% endfor %}
            </div>
        </div>

        <form method="POST">
            {% for m in mecze %}
            <div class="mecz-row">
                <div class="mecz-header">
                    ⏰ {{ m.data }} 
                    {% if m.zablokowany %}<span style="color: #dc3545; margin-left: 10px;">🔒 ZABLOKOWANY</span>{% endif %}
                </div>
                <div style="margin: 15px 0; font-size: 18px; font-weight: bold; color: #002244;">
                    {{ m.gospodarz }} 
                    <input type="text" name="wynik_g_{{ m['id'] }}" value="{{ m.wynik_g }}" {% if session.get('user') != 'Admin' %}readonly style="background:#eee; color:#666;"{% endif %} style="border: 2px solid #002244; width: 40px;">
                    :
                    <input type="text" name="wynik_b_{{ m['id'] }}" value="{{ m.wynik_b }}" {% if session.get('user') != 'Admin' %}readonly style="background:#eee; color:#666;"{% endif %} style="border: 2px solid #002244; width: 40px;">
                    {{ m.gosc }}
                </div>
                
                <div class="grid-typy">
                    {% for gracz in lista_graczy %}
                    {% set g_typ = typy[gracz][m['id']] %}
                    {% set blokada_dla_gracza = m.zablokowany and session.get('user') != 'Admin' %}
                    <div class="gracz-card" style="background-color: {{ g_typ.kolor }};">
                        <span>{{ gracz }}</span>
                        <div>
                            <input type="text" name="typ_g_{{ gracz }}_{{ m['id'] }}" value="{{ g_typ.typ_g }}" {% if blokada_dla_gracza or (session.get('user') != gracz and session.get('user') != 'Admin') %}readonly style="background:rgba(0,0,0,0.05); border:none;"{% endif %}>
                            :
                            <input type="text" name="typ_b_{{ gracz }}_{{ m['id'] }}" value="{{ g_typ.typ_b }}" {% if blokada_dla_gracza or (session.get('user') != gracz and session.get('user') != 'Admin') %}readonly style="background:rgba(0,0,0,0.05); border:none;"{% endif %}>
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

        {% if session.get('user') == 'Admin' %}
        <div class="admin-backup-box">
            <h3>🔑 PANEL ADMINA: Kopia Zapasowa (Ochrona przed resetem serwera)</h3>
            <p>Skopiuj ten kod i wklej go do pliku <b>main.py</b> na GitHubie, aby zamrozić wyniki na stałe.</p>
            <pre>{{ backup_code }}</pre>
        </div>
        {% endif %}

    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    wiadomosc = ""
    
    # 1. Kłódki czasowe
    now_pl = datetime.utcnow() + timedelta(hours=2)
    for m in mecze:
        if "sys_data" in m:
            m_time = datetime.strptime(m["sys_data"], "%Y-%m-%d %H:%M")
            m["zablokowany"] = now_pl >= m_time
        else:
            m["zablokowany"] = False

    # 2. Zapisywanie
    if request.method == "POST":
        current_user = session.get("user")
        if current_user == "Admin":
            for m in mecze:
                m["wynik_g"] = request.form.get(f"wynik_g_{m['id']}", m["wynik_g"])
                m["wynik_b"] = request.form.get(f"wynik_b_{m['id']}", m["wynik_b"])
        
        if current_user:
            for m in mecze:
                if current_user != "Admin" and m["zablokowany"]:
                    continue
                for gracz in lista_graczy:
                    if current_user == "Admin" or current_user == gracz:
                        tg = request.form.get(f"typ_g_{gracz}_{m['id']}")
                        tb = request.form.get(f"typ_b_{gracz}_{m['id']}")
                        if tg is not None: typy[gracz][m["id"]]["typ_g"] = tg
                        if tb is not None: typy[gracz][m["id"]]["typ_b"] = tb
            wiadomosc = "✅ Pomyślnie zapisano wyniki!"

    przelicz_wszystko()
            
    totale_sorted = sorted(totale.items(), key=lambda x: x[1], reverse=True)
    
    # Przygotowanie danych dla podium (pobierz top 3)
    # Jeśli turniej startuje, a wszyscy mają 0 pkt, podium też się wyświetli z pustymi nazwami
    default_p = [("", 0), ("", 0), ("", 0)]
    podium_data = default_p
    if totale_sorted:
        podium_data = totale_sorted[:3]
        while len(podium_data) < 3: # Obsługa sytuacji, gdyby grało mniej niż 3 osoby
            podium_data.append(("", 0))
    
    backup_lines = ["startowe_typy = {"]
    for g in lista_graczy:
        m_list = []
        for m in mecze:
            tg = typy[g][m["id"]]["typ_g"]
            tb = typy[g][m["id"]]["typ_b"]
            if str(tg).strip() != "" and str(tb).strip() != "":
                m_list.append(f"{m['id']}: ({tg}, {tb})")
        m_str = ", ".join(m_list)
        backup_lines.append(f"    \"{g}\": {{{m_str}}},")
    backup_lines.append("}")
    backup_code = "\n".join(backup_lines)

    return render_template_string(HTML_TEMPLATE, mecze=mecze, lista_graczy=lista_graczy, typy=typy, totale_sorted=totale_sorted, podium=podium_data, backup_code=backup_code, wiadomosc=wiadomosc)

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
