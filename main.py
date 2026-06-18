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

# BAZA MECZÓW (Zaktualizowana: historyczne zachowane, nowe z 19-26 czerwca dodane)
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
    
    # 14 czerwca
    {"id": 16, "data": "Niedziela 19:00", "sys
