import os
import requests
from flask import Flask, render_template_string, request, session, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "mundial_2026_ekipa"

# KREDENCJAŁY BAZY DANYCH JSONBIN
BIN_ID = "6a2bc4f8da38895dfeb38af7"
API_KEY = "$2a$10$VyqGJb1B1B6JJTNmndInGetz3wNmPkBpM//mfUyDdAvf3wsGhH0jW"
JSONBIN_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {
    "Content-Type": "application/json",
    "X-Master-Key": API_KEY
}

# BAZA MECZÓW (Czysta, bez flag - omija blokadę GitHuba)
mecze = [
    {"id": 0, "data": "Czwartek 21:00", "sys_data": "2026-06-11 21:00", "gospodarz": "Meksyk", "gosc": "RPA", "wynik_g": "2", "wynik_b": "0"},
    {"id": 1, "data": "Piątek 04:00", "sys_data": "2026-06-12 04:00", "gospodarz": "Korea Południowa", "gosc": "Czechy", "wynik_g": "2", "wynik_b": "1"},
    {"id": 2, "data": "Piątek 21:00", "sys_data": "2026-06-12 21:00", "gospodarz": "Kanada", "gosc": "Bośnia i Hercegowina", "wynik_g": "", "wynik_b": ""},
    {"id": 3, "data": "Sobota 03:00", "sys_data": "2026-06-13 03:00", "gospodarz": "USA", "gosc": "Paragwaj", "wynik_g": "", "wynik_b": ""},
    {"id": 4, "data": "Sobota 21:00", "sys_data": "2026-06-13 21:00", "gospodarz": "Katar", "gosc": "Szwajcaria", "wynik_g": "", "wynik_b": ""},
    {"id": 5, "data": "Niedziela 00:00", "sys_data": "2026-06-14 00:00", "gospodarz": "Brazylia", "gosc": "Maroko", "wynik_g": "", "wynik_b": ""},
    {"id": 6, "data": "Niedziela 03:00", "sys_data": "2026-06-14 03:00", "gospodarz": "Haiti", "gosc": "Szkocja", "wynik_g": "", "wynik_b": ""},
    
    # --- DODANE DZISIEJSZE MECZE (14 czerwca) ---
    {"id": 15, "data": "Niedziela 06:00", "sys_data": "2026-06-14 06:00", "gospodarz": "Australia", "gosc": "Turcja", "wynik_g": "", "wynik_b": ""},
    {"id": 16, "data": "Niedziela 19:00", "sys_data": "2026-06-14 19:00", "gospodarz": "Niemcy", "gosc": "Curaçao", "wynik_g": "", "wynik_b": ""},
    {"id": 17, "data": "Niedziela 22:00", "sys_data": "2026-06-14 22:00", "gospodarz": "Holandia", "gosc": "Japonia", "wynik_g": "", "wynik_b": ""},
    # ----------------------------------------------

    {"id": 7, "data": "Poniedziałek 15:00", "sys_data": "2026-06-15 15:00", "gospodarz": "Argentyna", "gosc": "Szwecja", "wynik_g": "", "wynik_b": ""},
    {"id": 8, "data": "Poniedziałek 21:00", "sys_data": "2026-06-15 21:00", "gospodarz": "Francja", "gosc": "Nigeria", "wynik_g": "", "wynik_b": ""},
    {"id": 9, "data": "Wtorek 15:00", "sys_data": "2026-06-16 15:00", "gospodarz": "Hiszpania", "gosc": "Japonia", "wynik_g": "", "wynik_b": ""},
    {"id": 10, "data": "Wtorek 21:00", "sys_data": "2026-06-16 21:00", "gospodarz": "Anglia", "gosc": "Kolumbia", "wynik_g": "", "wynik_b": ""},
    {"id": 11, "data": "Środa 15:00", "sys_data": "2026-06-17 15:00", "gospodarz": "Niemcy", "gosc": "Chile", "wynik_g": "", "wynik_b": ""},
    {"id": 12, "data": "Środa 21:00", "sys_data": "2026-06-17 21:00", "gospodarz": "Portugalia", "gosc": "Senegal", "wynik_g": "", "wynik_b": ""},
    {"id": 13, "data": "Czwartek 15:00", "sys_data": "2026-06-18 15:00", "gospodarz": "Włochy", "gosc": "Urugwaj", "wynik_g": "", "wynik_b": ""},
    {"id": 14, "data": "Czwartek 21:00", "sys_data": "2026-06-18 21:00", "gospodarz": "Holandia", "gosc": "Australia", "wynik_g": "", "wynik_b": ""}
]

# LISTA UCZESTNIKÓW
lista_graczy = [
    "Andrzej", "Jakub", "Daniel", "Klaudia T", "Agnieszka",
    "Patrycja A", "Julia", "Marzena", "Malina", "Patrycja W",
    "Agata", "Marek", "Kamil O", "Kamil K", "Michał", "Tomek",
    "Oliwia", "Szymon", "Oliwier", "Patrycja C"
]

# STARTOWE TYPY
startowe_typy = {
    "Andrzej": {0: (3, 1), 1: (2, 1)}, "Jakub": {0: (1, 1), 1: (1, 1)}, "Daniel": {0: (2, 0), 1: (2, 1)},
    "Klaudia T": {0: (2, 1), 1: (1, 0)}, "Agnieszka": {0: (2, 0), 1: (1, 1)}, "Patrycja A": {0: (2, 0), 1: (1, 1)},
    "Julia": {0: (2, 1), 1: (0, 1)}, "Marzena": {0: (3, 1), 1: (0, 3)}, "Malina": {0: (3, 1), 1: (1, 2)},
    "Patrycja W": {0: (4, 0), 1: (1, 3)}, "Agata": {0: (3, 0), 1: (0, 2)}, "Marek": {0: (1, 0), 1: (2, 1)},
    "Kamil O": {0: (3, 0), 1: (1, 1)}, "Kamil K": {0: (3, 0), 1: (0, 2)}, "Michał": {0: (2, 1), 1: (1, 0)},
    "Tomek": {0: (2, 1), 1: (1, 2)},
    "Oliwia": {3: (2, 0)},
    "Szymon": {},
    "Oliwier": {},
    "Patrycja C": {}
}

# INICJALIZACJA BAZY LOKALNEJ
typy = {gracz: {m["id"]: {"typ_g": "", "typ_b": "", "punkty": 0, "kolor": "white"} for m in mecze} for gracz in lista_graczy}
for gracz, m_typy in startowe_typy.items():
    for m_id, (tg, tb) in m_typy.items():
        if m_id in typy[gracz]:  # Zabezpieczenie na wypadek, gdyby ktoś wytypował usunięty mecz
            typy[gracz][m_id]["typ_g"] = str(tg)
            typy[gracz][m_id]["typ_b"] = str(tb)

totale = {gracz: 0 for gracz in lista_graczy}

# ----------------- SYSTEM BAZY DANYCH -----------------
def wczytaj_dane():
    try:
        response = requests.get(JSONBIN_URL, headers=HEADERS)
        if response.status_code == 200:
            dane = response.json().get("record", {})
            if dane.get("status") == "start":
                return
            
            if "typy" in dane:
                for gracz in lista_graczy:
                    if gracz in dane["typy"]:
                        for m in mecze:
                            m_str = str(m["id"])
                            if m_str in dane["typy"][gracz]:
                                typy[gracz][m["id"]]["typ_g"] = str(dane["typy"][gracz][m_str].get("typ_g", ""))
                                typy[gracz][m["id"]]["typ_b"] = str(dane["typy"][gracz][m_str].get("typ_b", ""))
            
            if "mecze_wyniki" in dane:
                for m in mecze:
                    m_str = str(m["id"])
                    if m_str in dane["mecze_wyniki"]:
                        m["wynik_g"] = str(dane["mecze_wyniki"][m_str].get("wynik_g", ""))
                        m["wynik_b"] = str(dane["mecze_wyniki"][m_str].get("wynik_b", ""))
    except Exception as e:
        print("Błąd pobierania danych:", e)

def zapisz_dane():
    typy_do_zapisu = {gracz: {str(m_id): data for m_id, data in m_dict.items()} for gracz, m_dict in typy.items()}
    mecze_do_zapisu = {str(m["id"]): {"wynik_g": m["wynik_g"], "wynik_b": m["wynik_b"]} for m in mecze}
    
    dane = {
        "typy": typy_do_zapisu,
        "mecze_wyniki": mecze_do_zapisu
    }
    try:
        requests.put(JSONBIN_URL, json=dane, headers=HEADERS)
    except Exception as e:
        print("Błąd zapisu danych:", e)

wczytaj_dane()
# ------------------------------------------------------

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
        
        .podium-wrap { display: flex; justify-content: center; align-items: flex-end; gap: 8px; margin-bottom: 25px; text-align: center; color: white; font-weight: bold; }
        .podium-block { width: 32%; border-radius: 12px 12px 0 0; border: 1px solid rgba(255,255,255,0.1); padding: 15px 5px; position: relative; }
        .p-name { font-size: 13px; margin: 5px 0; display: block; white-space: normal; word-wrap: break-word; line-height: 1.3; }
        .p-pts { color: #00EDFF; font-size: 18px; font-weight: 800; display: block; margin-top: 5px;}
        .p-1 { min-height: 140px; background: linear-gradient(180deg, #FFD700, #007D8F); border-top: 5px solid #FFD700; box-shadow: 0 -4px 15px rgba(255,215,0,0.3); order: 2;}
        .p-1 .p-rank { font-size: 30px; position: absolute; top: -20px; left: 50%; transform: translateX(-50%); }
        .p-2 { min-height: 110px; background: linear-gradient(180deg, #C0C0C0, #002244); border-top: 5px solid #C0C0C0; order: 1;}
        .p-2 .p-rank { font-size: 24px; color: #C0C0C0; }
        .p-3 { min-height: 90px; background: linear-gradient(180deg, #CD7F32, #002244); border-top: 5px solid #CD7F32; order: 3;}
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
        
        /* CSS DLA SZUFLADY ZAKOŃCZONYCH MECZÓW */
        .zakonczone-sekcja { background: #f8f9fa; border: 2px dashed #ced4da; border-radius: 12px; margin-bottom: 30px; }
        .zakonczone-sekcja summary { font-weight: 800; color: #6c757d; cursor: pointer; padding: 15px; text-align: center; list-style: none; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; outline: none; transition: 0.2s; user-select: none; }
        .zakonczone-sekcja summary:hover { color: #002244; background: #e9ecef; border-radius: 12px; }
        .zakonczone-sekcja summary::-webkit-details-marker { display: none; }
        .zakonczone-sekcja[open] summary { border-bottom: 2px dashed #ced4da; border-radius: 12px 12px 0 0; margin-bottom: 15px; background: transparent;}
        .naglowek-sekcji { text-align: center; color: #002244; margin: 20px 0 25px 0; font-size: 20px; font-weight: 800; letter-spacing: 1px; }
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
                    <span class="p-pts">{% if podium[1][1] > 0 %}{{ podium[1][1] }} pkt{% endif %}</span>
                </div>
                <div class="podium-block p-1">
                    <div class="p-rank">👑</div>
                    <span class="p-name">{{ podium[0][0] }}</span>
                    <span class="p-pts">{% if podium[0][1] > 0 %}{{ podium[0][1] }} pkt{% endif %}</span>
                </div>
                <div class="podium-block p-3">
                    <div class="p-rank">3</div>
                    <span class="p-name">{{ podium[2][0] }}</span>
                    <span class="p-pts">{% if podium[2][1] > 0 %}{{ podium[2][1] }} pkt{% endif %}</span>
                </div>
            </div>

            <div class="ranking-grid">
                {% for miejsce, gracz, pkt in ranking %}
                <div class="ranking-item"><b>{{ miejsce }}. {{ gracz }}</b><br><span style="color:#00EDFF; font-size:16px;">{{ pkt }} pkt</span></div>
                {% endfor %}
            </div>
        </div>

        <form method="POST">
            {% set ns = namespace(zablokowane=0, aktywne=0) %}
            {% for m in mecze %}
                {% if m.zablokowany %}
                    {% set ns.zablokowane = ns.zablokowane + 1 %}
                {% else %}
                    {% set ns.aktywne = ns.aktywne + 1 %}
                {% endif %}
            {% endfor %}

            {% if ns.zablokowane > 0 %}
            <details class="zakonczone-sekcja">
                <summary>⬇️ Rozwiń zakończone mecze ({{ ns.zablokowane }}) ⬇️</summary>
                <div style="padding: 0 10px;">
                {% for m in mecze %}
                    {% if m.zablokowany %}
                    <div class="mecz-row" style="background-color: #fcfcfc;">
                        <div class="mecz-header">
                            ⏰ {{ m.data }} <span style="color: #dc3545; margin-left: 10px;">🔒 ZABLOKOWANY</span>
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
                            <div class="gracz-card" style="background-color: {{ g_typ.kolor }}; opacity: 0.85;">
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
                    {% endif %}
                {% endfor %}
                </div>
            </details>
            {% endif %}

            {% if ns.aktywne > 0 %}
            <div class="naglowek-sekcji">🔥 MECZE DO TYPOWANIA ({{ ns.aktywne }}) 🔥</div>
            {% for m in mecze %}
                {% if not m.zablokowany %}
                <div class="mecz-row">
                    <div class="mecz-header">
                        ⏰ {{ m.data }} 
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
                {% endif %}
            {% endfor %}
            {% else %}
            <div class="naglowek-sekcji">🏁 WSZYSTKIE MECZE ZAKOŃCZONE 🏁</div>
            {% endif %}
            
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
    wiadomosc = ""
    
    # 1. Kłódki czasowe
    now_pl = datetime.utcnow() + timedelta(hours=2)
    for m in mecze:
        if "sys_data" in m:
            m_time = datetime.strptime(m["sys_data"], "%Y-%m-%d %H:%M")
            m["zablokowany"] = now_pl >= m_time
        else:
            m["zablokowany"] = False

    # 2. Zapisywanie z frontendu
    if request.method == "POST":
        current_user = session.get("user")
        zmiana = False
        
        if current_user == "Admin":
            for m in mecze:
                nowy_g = request.form.get(f"wynik_g_{m['id']}")
                nowy_b = request.form.get(f"wynik_b_{m['id']}")
                if nowy_g is not None and nowy_b is not None:
                    if m["wynik_g"] != nowy_g or m["wynik_b"] != nowy_b:
                        m["wynik_g"] = nowy_g
                        m["wynik_b"] = nowy_b
                        zmiana = True
        
        if current_user:
            for m in mecze:
                if current_user != "Admin" and m["zablokowany"]:
                    continue
                for gracz in lista_graczy:
                    if current_user == "Admin" or current_user == gracz:
                        tg = request.form.get(f"typ_g_{gracz}_{m['id']}")
                        tb = request.form.get(f"typ_b_{gracz}_{m['id']}")
                        if tg is not None and tb is not None:
                            if typy[gracz][m["id"]]["typ_g"] != tg or typy[gracz][m["id"]]["typ_b"] != tb:
                                typy[gracz][m["id"]]["typ_g"] = tg
                                typy[gracz][m["id"]]["typ_b"] = tb
                                zmiana = True
                                
        if zmiana:
            zapisz_dane()
            wiadomosc = "✅ Pomyślnie zapisano wyniki!"

    przelicz_wszystko()
            
    # SORTOWANIE
    totale_sorted = sorted(totale.items(), key=lambda x: x[1], reverse=True)
    
    # LUZACKIE NUMEROWANIE MIEJSC
    ranking_z_miejscami = []
    aktualne_miejsce = 1
    for i, (g, p) in enumerate(totale_sorted):
        if i > 0 and p < totale_sorted[i-1][1]:
            aktualne_miejsce += 1
        ranking_z_miejscami.append((aktualne_miejsce, g, p))
        
    # PODIUM
    punkty_dodatnie = sorted(list(set([p for p in totale.values() if p > 0])), reverse=True)
    podium_data = []
    for i in range(3):
        if i < len(punkty_dodatnie):
            pkt = punkty_dodatnie[i]
            gracze = [g for g, p in totale.items() if p == pkt]
            podium_data.append((", ".join(gracze), pkt))
        else:
            podium_data.append(("---", 0))

    return render_template_string(HTML_TEMPLATE, mecze=mecze, lista_graczy=lista_graczy, typy=typy, ranking=ranking_z_miejscami, podium=podium_data, wiadomosc=wiadomosc)

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
