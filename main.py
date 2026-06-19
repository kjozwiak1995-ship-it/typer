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

# BAZA MECZÓW
mecze = [
    # --- MECZE ZAKOŃCZONE / DOTYCHCZASOWE ---
    {"id": 0, "data": "Czwartek 21:00", "sys_data": "2026-06-11 21:00", "gospodarz": "Meksyk", "gosc": "RPA", "wynik_g": "2", "wynik_b": "0"},
    {"id": 1, "data": "Piątek 04:00", "sys_data": "2026-06-12 04:00", "gospodarz": "Korea Południowa", "gosc": "Czechy", "wynik_g": "2", "wynik_b": "1"},
    {"id": 2, "data": "Piątek 21:00", "sys_data": "2026-06-12 21:00", "gospodarz": "Kanada", "gosc": "Bośnia i Hercegowina", "wynik_g": "", "wynik_b": ""},
    {"id": 3, "data": "Sobota 03:00", "sys_data": "2026-06-13 03:00", "gospodarz": "USA", "gosc": "Paragwaj", "wynik_g": "", "wynik_b": ""},
    {"id": 4, "data": "Sobota 21:00", "sys_data": "2026-06-13 21:00", "gospodarz": "Katar", "gosc": "Szwajcaria", "wynik_g": "", "wynik_b": ""},
    {"id": 5, "data": "Niedziela 00:00", "sys_data": "2026-06-14 00:00", "gospodarz": "Brazylia", "gosc": "Maroko", "wynik_g": "", "wynik_b": ""},
    {"id": 6, "data": "Niedziela 03:00", "sys_data": "2026-06-14 03:00", "gospodarz": "Haiti", "gosc": "Szkocja", "wynik_g": "", "wynik_b": ""},
    {"id": 15, "data": "Niedziela 06:00", "sys_data": "2026-06-14 06:00", "gospodarz": "Australia", "gosc": "Turcja", "wynik_g": "", "wynik_b": ""},
    
    # --- KOLEJNA PORCJA TERMINARZA ---
    {"id": 16, "data": "Niedziela 19:00", "sys_data": "2026-06-14 19:00", "gospodarz": "Niemcy", "gosc": "Curaçao", "wynik_g": "", "wynik_b": ""},
    {"id": 17, "data": "Niedziela 22:00", "sys_data": "2026-06-14 22:00", "gospodarz": "Holandia", "gosc": "Japonia", "wynik_g": "", "wynik_b": ""},
    {"id": 18, "data": "Poniedziałek 01:00", "sys_data": "2026-06-15 01:00", "gospodarz": "Wybrzeże Kości Słoniowej", "gosc": "Ekwador", "wynik_g": "", "wynik_b": ""},
    {"id": 19, "data": "Poniedziałek 04:00", "sys_data": "2026-06-15 04:00", "gospodarz": "Szwecja", "gosc": "Tunezja", "wynik_g": "", "wynik_b": ""},
    {"id": 7, "data": "Poniedziałek 18:00", "sys_data": "2026-06-15 18:00", "gospodarz": "Hiszpania", "gosc": "Republika Zielonego Przylądka", "wynik_g": "", "wynik_b": ""},
    {"id": 8, "data": "Poniedziałek 21:00", "sys_data": "2026-06-15 21:00", "gospodarz": "Belgia", "gosc": "Egipt", "wynik_g": "", "wynik_b": ""},
    {"id": 20, "data": "Wtorek 00:00", "sys_data": "2026-06-16 00:00", "gospodarz": "Arabia Saudyjska", "gosc": "Urugwaj", "wynik_g": "", "wynik_b": ""},
    {"id": 21, "data": "Wtorek 03:00", "sys_data": "2026-06-16 03:00", "gospodarz": "Iran", "gosc": "Nowa Zelandia", "wynik_g": "", "wynik_b": ""},
    {"id": 9, "data": "Wtorek 21:00", "sys_data": "2026-06-16 21:00", "gospodarz": "Francja", "gosc": "Senegal", "wynik_g": "", "wynik_b": ""},
    {"id": 22, "data": "Środa 00:00", "sys_data": "2026-06-17 00:00", "gospodarz": "Irak", "gosc": "Norwegia", "wynik_g": "", "wynik_b": ""},
    {"id": 23, "data": "Środa 03:00", "sys_data": "2026-06-17 03:00", "gospodarz": "Argentyna", "gosc": "Algieria", "wynik_g": "", "wynik_b": ""},
    {"id": 24, "data": "Środa 06:00", "sys_data": "2026-06-17 06:00", "gospodarz": "Austria", "gosc": "Jordania", "wynik_g": "", "wynik_b": ""},
    {"id": 10, "data": "Środa 19:00", "sys_data": "2026-06-17 19:00", "gospodarz": "Portugalia", "gosc": "DR Konga", "wynik_g": "", "wynik_b": ""},
    {"id": 11, "data": "Środa 22:00", "sys_data": "2026-06-17 22:00", "gospodarz": "Anglia", "gosc": "Chorwacja", "wynik_g": "", "wynik_b": ""},
    {"id": 12, "data": "Czwartek 01:00", "sys_data": "2026-06-18 01:00", "gospodarz": "Ghana", "gosc": "Panama", "wynik_g": "", "wynik_b": ""},
    {"id": 25, "data": "Czwartek 04:00", "sys_data": "2026-06-18 04:00", "gospodarz": "Uzbekistan", "gosc": "Kolumbia", "wynik_g": "", "wynik_b": ""},
    {"id": 13, "data": "Czwartek 18:00", "sys_data": "2026-06-18 18:00", "gospodarz": "Czechy", "gosc": "RPA", "wynik_g": "", "wynik_b": ""},
    {"id": 14, "data": "Czwartek 21:00", "sys_data": "2026-06-18 21:00", "gospodarz": "Szwajcaria", "gosc": "Bośnia i Hercegowina", "wynik_g": "", "wynik_b": ""},
    
    # --- NOWE MECZE OD 19 CZERWCA DO 28 CZERWCA ---
    {"id": 26, "data": "Piątek 00:00", "sys_data": "2026-06-19 00:00", "gospodarz": "Kanada", "gosc": "Katar", "wynik_g": "", "wynik_b": ""},
    {"id": 27, "data": "Piątek 03:00", "sys_data": "2026-06-19 03:00", "gospodarz": "Meksyk", "gosc": "Korea Południowa", "wynik_g": "", "wynik_b": ""},
    {"id": 28, "data": "Piątek 21:00", "sys_data": "2026-06-19 21:00", "gospodarz": "USA", "gosc": "Australia", "wynik_g": "", "wynik_b": ""},
    {"id": 29, "data": "Sobota 00:00", "sys_data": "2026-06-20 00:00", "gospodarz": "Szkocja", "gosc": "Maroko", "wynik_g": "", "wynik_b": ""},
    {"id": 30, "data": "Sobota 03:00", "sys_data": "2026-06-20 03:00", "gospodarz": "Brazylia", "gosc": "Haiti", "wynik_g": "", "wynik_b": ""},
    {"id": 31, "data": "Sobota 05:00", "sys_data": "2026-06-20 05:00", "gospodarz": "Turcja", "gosc": "Paragwaj", "wynik_g": "", "wynik_b": ""},
    {"id": 32, "data": "Sobota 19:00", "sys_data": "2026-06-20 19:00", "gospodarz": "Holandia", "gosc": "Szwecja", "wynik_g": "", "wynik_b": ""},
    {"id": 33, "data": "Sobota 22:00", "sys_data": "2026-06-20 22:00", "gospodarz": "Niemcy", "gosc": "Wybrzeże Kości Słoniowej", "wynik_g": "", "wynik_b": ""},
    {"id": 34, "data": "Niedziela 02:00", "sys_data": "2026-06-21 02:00", "gospodarz": "Ekwador", "gosc": "Curaçao", "wynik_g": "", "wynik_b": ""},
    {"id": 35, "data": "Niedziela 06:00", "sys_data": "2026-06-21 06:00", "gospodarz": "Tunezja", "gosc": "Japonia", "wynik_g": "", "wynik_b": ""},
    {"id": 36, "data": "Niedziela 18:00", "sys_data": "2026-06-21 18:00", "gospodarz": "Hiszpania", "gosc": "Arabia Saudyjska", "wynik_g": "", "wynik_b": ""},
    {"id": 37, "data": "Niedziela 21:00", "sys_data": "2026-06-21 21:00", "gospodarz": "Belgia", "gosc": "Iran", "wynik_g": "", "wynik_b": ""},
    {"id": 38, "data": "Poniedziałek 00:00", "sys_data": "2026-06-22 00:00", "gospodarz": "Urugwaj", "gosc": "Republika Zielonego Przylądka", "wynik_g": "", "wynik_b": ""},
    {"id": 39, "data": "Poniedziałek 03:00", "sys_data": "2026-06-22 03:00", "gospodarz": "Nowa Zelandia", "gosc": "Egipt", "wynik_g": "", "wynik_b": ""},
    {"id": 40, "data": "Poniedziałek 19:00", "sys_data": "2026-06-22 19:00", "gospodarz": "Argentyna", "gosc": "Austria", "wynik_g": "", "wynik_b": ""},
    {"id": 41, "data": "Poniedziałek 23:00", "sys_data": "2026-06-22 23:00", "gospodarz": "Francja", "gosc": "Irak", "wynik_g": "", "wynik_b": ""},
    {"id": 42, "data": "Wtorek 02:00", "sys_data": "2026-06-23 02:00", "gospodarz": "Norwegia", "gosc": "Senegal", "wynik_g": "", "wynik_b": ""},
    {"id": 43, "data": "Wtorek 05:00", "sys_data": "2026-06-23 05:00", "gospodarz": "Jordania", "gosc": "Algieria", "wynik_g": "", "wynik_b": ""},
    {"id": 44, "data": "Wtorek 19:00", "sys_data": "2026-06-23 19:00", "gospodarz": "Portugalia", "gosc": "Uzbekistan", "wynik_g": "", "wynik_b": ""},
    {"id": 45, "data": "Wtorek 22:00", "sys_data": "2026-06-23 22:00", "gospodarz": "Anglia", "gosc": "Ghana", "wynik_g": "", "wynik_b": ""},
    {"id": 46, "data": "Środa 01:00", "sys_data": "2026-06-24 01:00", "gospodarz": "Panama", "gosc": "Chorwacja", "wynik_g": "", "wynik_b": ""},
    {"id": 47, "data": "Środa 04:00", "sys_data": "2026-06-24 04:00", "gospodarz": "Kolumbia", "gosc": "DR Konga", "wynik_g": "", "wynik_b": ""},
    {"id": 48, "data": "Środa 21:00", "sys_data": "2026-06-24 21:00", "gospodarz": "Szwajcaria", "gosc": "Kanada", "wynik_g": "", "wynik_b": ""},
    {"id": 49, "data": "Środa 21:00", "sys_data": "2026-06-24 21:00", "gospodarz": "Bośnia i Hercegowina", "gosc": "Katar", "wynik_g": "", "wynik_b": ""},
    {"id": 50, "data": "Czwartek 00:00", "sys_data": "2026-06-25 00:00", "gospodarz": "Maroko", "gosc": "Haiti", "wynik_g": "", "wynik_b": ""},
    {"id": 51, "data": "Czwartek 00:00", "sys_data": "2026-06-25 00:00", "gospodarz": "Szkocja", "gosc": "Brazylia", "wynik_g": "", "wynik_b": ""},
    {"id": 52, "data": "Czwartek 03:00", "sys_data": "2026-06-25 03:00", "gospodarz": "RPA", "gosc": "Korea Południowa", "wynik_g": "", "wynik_b": ""},
    {"id": 53, "data": "Czwartek 03:00", "sys_data": "2026-06-25 03:00", "gospodarz": "Czechy", "gosc": "Meksyk", "wynik_g": "", "wynik_b": ""},
    {"id": 54, "data": "Czwartek 22:00", "sys_data": "2026-06-25 22:00", "gospodarz": "Curaçao", "gosc": "Wybrzeże Kości Słoniowej", "wynik_g": "", "wynik_b": ""},
    {"id": 55, "data": "Czwartek 22:00", "sys_data": "2026-06-25 22:00", "gospodarz": "Ekwador", "gosc": "Niemcy", "wynik_g": "", "wynik_b": ""},
    {"id": 56, "data": "Piątek 01:00", "sys_data": "2026-06-26 01:00", "gospodarz": "Japonia", "gosc": "Szwecja", "wynik_g": "", "wynik_b": ""},
    {"id": 57, "data": "Piątek 01:00", "sys_data": "2026-06-26 01:00", "gospodarz": "Tunezja", "gosc": "Holandia", "wynik_g": "", "wynik_b": ""},
    {"id": 58, "data": "Piątek 04:00", "sys_data": "2026-06-26 04:00", "gospodarz": "Paragwaj", "gosc": "Australia", "wynik_g": "", "wynik_b": ""},
    {"id": 59, "data": "Piątek 04:00", "sys_data": "2026-06-26 04:00", "gospodarz": "Turcja", "gosc": "USA", "wynik_g": "", "wynik_b": ""},
    {"id": 60, "data": "Piątek 21:00", "sys_data": "2026-06-26 21:00", "gospodarz": "Norwegia", "gosc": "Francja", "wynik_g": "", "wynik_b": ""},
    {"id": 61, "data": "Piątek 21:00", "sys_data": "2026-06-26 21:00", "gospodarz": "Senegal", "gosc": "Irak", "wynik_g": "", "wynik_b": ""},
    {"id": 62, "data": "Sobota 02:00", "sys_data": "2026-06-27 02:00", "gospodarz": "Republika Zielonego Przylądka", "gosc": "Arabia Saudyjska", "wynik_g": "", "wynik_b": ""},
    {"id": 63, "data": "Sobota 02:00", "sys_data": "2026-06-27 02:00", "gospodarz": "Urugwaj", "gosc": "Hiszpania", "wynik_g": "", "wynik_b": ""},
    {"id": 64, "data": "Sobota 05:00", "sys_data": "2026-06-27 05:00", "gospodarz": "Egipt", "gosc": "Iran", "wynik_g": "", "wynik_b": ""},
    {"id": 65, "data": "Sobota 05:00", "sys_data": "2026-06-27 05:00", "gospodarz": "Nowa Zelandia", "gosc": "Belgia", "wynik_g": "", "wynik_b": ""},
    {"id": 66, "data": "Sobota 23:00", "sys_data": "2026-06-27 23:00", "gospodarz": "Chorwacja", "gosc": "Ghana", "wynik_g": "", "wynik_b": ""},
    {"id": 67, "data": "Sobota 23:00", "sys_data": "2026-06-27 23:00", "gospodarz": "Panama", "gosc": "Anglia", "wynik_g": "", "wynik_b": ""},
    {"id": 68, "data": "Niedziela 01:30", "sys_data": "2026-06-28 01:30", "gospodarz": "DR Konga", "gosc": "Uzbekistan", "wynik_g": "", "wynik_b": ""},
    {"id": 69, "data": "Niedziela 01:30", "sys_data": "2026-06-28 01:30", "gospodarz": "Kolumbia", "gosc": "Portugalia", "wynik_g": "", "wynik_b": ""},
    {"id": 70, "data": "Niedziela 04:00", "sys_data": "2026-06-28 04:00", "gospodarz": "Algieria", "gosc": "Austria", "wynik_g": "", "wynik_b": ""},
    {"id": 71, "data": "Niedziela 04:00", "sys_data": "2026-06-28 04:00", "gospodarz": "Jordania", "gosc": "Argentyna", "wynik_g": "", "wynik_b": ""}
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
    "Tomek": {0: (2, 1), 1: (1, 2)}, "Oliwia": {3: (2, 0)}, "Szymon": {}, "Oliwier": {}, "Patrycja C": {}
}

typy = {gracz: {m["id"]: {"typ_g": "", "typ_b": "", "punkty": 0, "kolor": "white"} for m in mecze} for gracz in lista_graczy}
totale = {gracz: 0 for gracz in lista_graczy}

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

def przelicz_wszystko():
    # Ręczna korekta punktów bonusowych
    for g in lista_graczy: 
        if g == "Julia":
            totale[g] = 3
        elif g == "Oliwier":
            totale[g] = 0
        else:
            totale[g] = 1
            
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

# TYMCZASOWY SZABLON Z BLĘDEM TECHNICZNYM
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Decathlon Typer MŚ 2026</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            font-family: 'Segoe UI', sans-serif; 
            background-color: #f4f7f6; 
            margin: 0; 
            height: 100vh; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            color: #333; 
        }
        .error-container { 
            text-align: center; 
            background: white; 
            padding: 40px; 
            border-radius: 16px; 
            box-shadow: 0 4px 25px rgba(0,0,0,0.06); 
            max-width: 90%;
            border-top: 6px solid #dc3545;
        }
        h1 { 
            color: #dc3545; 
            font-size: 28px; 
            margin-bottom: 10px; 
            font-weight: 800; 
            text-transform: uppercase; 
        }
        p { 
            color: #6c757d; 
            font-size: 16px; 
            margin: 0; 
        }
    </style>
</head>
<body>
    <div class="error-container">
        <h1>⚠️ Błąd techniczny ⚠️</h1>
        <p>Trwają prace konserwacyjne nad aplikacją. Spróbuj ponownie później.</p>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    # Zwraca tylko widok błędu, bez przetwarzania i zapisywania zmian w tle
    return render_template_string(HTML_TEMPLATE)

@app.route("/login", methods=["POST"])
def login():
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
