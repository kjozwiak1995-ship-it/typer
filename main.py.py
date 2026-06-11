from flask import Flask, render_template_string, request, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = "mundial_secret_key_2026" # Potrzebne do logowania

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

lista_graczy = [
    "Andrzej", "Jakub", "Daniel", "Klaudia T", "Agnieszka",
    "Patrycja A", "Julia", "Marzena", "Malina", "Patrycja W",
    "Agata", "Marek", "Kamil O", "Kamil K", "Michał"
]

# STARTOWE TYPY, KTÓRE JUŻ ZEBRAŁEŚ
typy = {gracz: {m["id"]: {"typ_g": "", "typ_b": "", "punkty": 0, "kolor": "white"} for m in mecze} for gracz in lista_graczy}
startowe_typy = {
    "Andrzej": {0: (3, 1), 1: (2, 1)}, "Jakub": {0: (1, 1), 1: (1, 1)}, "Daniel": {0: (2, 0), 1: (2, 1)},
    "Klaudia T": {0: (2, 1), 1: (1, 0)}, "Agnieszka": {0: (2, 0), 1: (1, 1)}, "Patrycja A": {0: (2, 0), 1: (1, 1)},
    "Julia": {0: (2, 1), 1: (0, 1)}, "Marzena": {0: (3, 1), 1: (0, 3)}, "Malina": {0: (3, 1), 1: (1, 2)},
    "Patrycja W": {0: (4, 0), 1: (1, 3)}, "Agata": {0: (3, 0), 1: (0, 2)}, "Marek": {0: (1, 0), 1: (2, 1)},
    "Kamil O": {0: (3, 0), 1: (1, 1)}, "Kamil K": {0: (3, 0), 1: (0, 2)}, "Michał": {0: (2, 1), 1: (1, 0)}
}

for gracz, m_typy in startowe_typy.items():
    for m_id, (tg, tb) in m_typy.items():
        typy[gracz][m_id]["typ_g"] = tg
        typy[gracz][m_id]["typ_b"] = tb

totale = {gracz: 0 for gracz in lista_graczy}

def przelicz_wszystko():
    for g in lista_graczy: totale[g] = 0
    for m in mecze:
        wg_raw, wb_raw = m["wynik_g"], m["wynik_b"]
        if wg_raw == "" or wb_raw == "":
            for g in lista_graczy:
                typy[g][m["id"]]["punkty"] = 0
                typy[g][m["id"]]["kolor"] = "white" if typy[g][m["id"]]["typ_g"] != "" else "#f3f4f6"
            continue
        wg, wb = int(wg_raw), int(wb_raw)
        for g in lista_graczy:
            tg_raw, tb_raw = typy[g][m["id"]]["typ_g"], typy[g][m["id"]]["typ_b"]
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
        input[type="number"] { width: 35px; padding: 4px; text-align: center; font-size: 14px; border: 1px solid #ccc; border-radius: 4px; }
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
                Zalogowany jako: <span style="color:#1F497D;">{{ session['user'] }}</span> | <a href="/logout">Wyloguj</a>
            {% else %}
                <form action="/login" method="POST" style="display:inline;">
                    Zaloguj się: 
                    <select name="user_name">
                        <option value="Admin">--- ADMIN (Ty) ---</option>
                        {% for g in lista_graczy %}<option value="{{ g }}">{{ g }}</option>{%