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

# BAZA MECZÓW (Zaktualizowana: historyczne zachowane, nowe dodane)
mecze = [
    # --- MECZE ZAKOŃCZONE (Zachowane, aby nie usunąć danych z bazy) ---
    {"id": 0, "data": "Czwartek 21:00", "sys_data": "2026-06-11 21:00", "gospodarz": "Meksyk", "gosc": "RPA", "wynik_g": "2", "wynik_b": "0"},
    {"id": 1, "data": "Piątek 04:00", "sys_data": "2026-06-12 04:00", "gospodarz": "Korea Południowa", "gosc": "Czechy", "wynik_g": "2", "wynik_b": "1"},
    {"id": 2, "data": "Piątek 21:00", "sys_data": "2026-06-12 21:00", "gospodarz": "Kanada", "gosc": "Bośnia i Hercegowina", "wynik_g": "", "wynik_b": ""},
    {"id": 3, "data": "Sobota 03:00", "sys_data": "2026-06-13 03:00", "gospodarz": "USA", "gosc": "Paragwaj", "wynik_g": "", "wynik_b": ""},
    {"id": 4, "data": "Sobota 21:00", "sys_data": "2026-06-13 21:00", "gospodarz": "Katar", "gosc": "Szwajcaria", "wynik_g": "", "wynik_b": ""},
    {"id": 5, "data": "Niedziela 00:00", "sys_data": "2026-06-14 00:00", "gospodarz": "Brazylia", "gosc": "Maroko", "wynik_g": "", "wynik_b": ""},
    {"id": 6, "data": "Niedziela 03:00", "sys_data": "2026-06-14 03:00", "gospodarz": "Haiti", "gosc": "Szkocja", "wynik_g": "", "wynik_b": ""},
    {"id": 15, "data": "Niedziela 06:00", "sys_data": "2026-06-14 06:00", "gospodarz": "Australia", "gosc": "Turcja", "wynik_g": "", "wynik_b": ""},
    
    # --- NOWY TERMINARZ (od 14 czerwca 19:00 do 18 czerwca) ---
    
    # 14 czerwca
    {"id": 16, "data": "Niedziela 19:00", "sys_data": "2026-06-14 19:00", "gospodarz": "Niemcy", "gosc": "Curaçao", "wynik_g": "", "wynik_b": ""},
    {"id": 17, "data": "Niedziela 22:00", "sys_data": "2026-06-14 22:00", "gospodarz": "Holandia", "gosc": "Japonia", "wynik_g": "", "wynik_b": ""},
    
    # 15 czerwca
    {"id": 18, "data": "Poniedziałek 01:00", "sys_data": "2026-06-15 01:00", "gospodarz": "Wybrzeże Kości Słoniowej", "gosc": "Ekwador", "wynik_g": "", "wynik_b": ""},
    {"id": 19, "data": "Poniedziałek 04:00", "sys_data": "2026-06-15 04:00", "gospodarz": "Szwecja", "gosc": "Tunezja", "wynik_g": "", "wynik_b": ""},
    {"id": 7, "data": "Poniedziałek 18:00", "sys_data": "2026-06-15 18:00", "gospodarz": "Hiszpania", "gosc": "Republika Zielonego Przylądka", "wynik_g": "", "wynik_b": ""},
    {"id": 8, "data": "Poniedziałek 21:00", "sys_data": "2026-06-15 21:00", "gospodarz": "Belgia", "gosc": "Egipt", "wynik_g": "", "wynik_b": ""},
    
    # 16 czerwca
    {"id": 20, "data": "Wtorek 00:00", "sys_data": "2026-06-16 00:00", "gospodarz": "Arabia Saudyjska", "gosc": "Urugwaj", "wynik_g": "", "wynik_b": ""},
    {"id": 21, "data": "Wtorek 03:00", "sys_data": "2026-06-16 03:00", "gospodarz": "Iran", "gosc": "Nowa Zelandia", "wynik_g": "", "wynik_b": ""},
    {"id": 9, "data": "Wtorek 21:00", "sys_data": "2026-06-16 21:00", "gospodarz": "Francja", "gosc": "Senegal", "wynik_g": "", "wynik_b": ""},
    
    # 17 czerwca
    {"id": 22, "data": "Środa 00:00", "sys_data": "2026-06-17 00:00", "gospodarz": "Irak", "gosc": "Norwegia", "wynik_g": "", "wynik_b": ""},
    {"id": 23, "data": "Środa 03:00", "sys_data": "2026-06-17 03:00", "gospodarz": "Argentyna", "gosc": "Algieria", "wynik_g": "", "wynik_b": ""},
    {"id": 24, "data": "Środa 06:00", "sys_data": "2026-06-17 06:00", "gospodarz": "Austria", "gosc": "Jordania", "wynik_g": "", "wynik_b": ""},
    {"id": 10, "data": "Środa 19:00", "sys_data": "2026-06-17 19:00", "gospodarz": "Portugalia", "gosc": "DR Konga", "wynik_g": "", "wynik_b": ""},
    {"id": 11, "data": "Środa 22:00", "sys_data": "2026-06-17 22:00", "gospodarz": "Anglia", "gosc": "Chorwacja", "wynik_g": "", "wynik_b": ""},
    
    # 18 czerwca
    {"id": 12, "data": "Czwartek 01:00", "sys_data": "2026-06-18 01:00", "gospodarz": "Ghana", "gosc": "Panama", "wynik_g": "", "wynik_b": ""},
    {"id": 25, "data": "Czwartek 04:00", "sys_data": "2026-06-18 04:00", "gospodarz": "Uzbekistan", "gosc": "Kolumbia", "wynik_g": "", "wynik_b": ""},
    {"id": 13, "data": "Czwartek 18:00", "sys_data": "2026-06-18 18:00", "gospodarz": "Czechy", "gosc": "RPA", "wynik_g": "", "wynik_b": ""},
    {"id": 14, "data": "Czwartek 21:00", "sys_data": "2026-06-18 21:00", "gospodarz": "Szwajcaria", "gosc": "Bośnia i Hercegowina", "wynik_g": "", "wynik_b": ""}
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
        if m_id in typy[gracz]:  # Zabezpieczenie na wypadek
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
    mecze_do_zapisu = {str(m["id"]): {"wynik_g": m["wynik_g"], "wynik_b": m["wynik_b"]}
