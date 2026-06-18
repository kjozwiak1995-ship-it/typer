@app.route("/", methods=["GET", "POST"])
def index():
    wiadomosc = None
    
    # 1. NAJPIERW WCZYTUJEMY NAJŚWIEŻSZE DANE Z BAZY
    wczytaj_dane()
    
    # 2. NAJPIERW USTALAMY BLOKADY CZASOWE
    teraz = datetime.now()
    for m in mecze:
        try:
            m_data = datetime.strptime(m["sys_data"], "%Y-%m-%d %H:%M")
            # Blokada na 15 minut przed meczem
            m["zablokowany"] = teraz >= (m_data - timedelta(minutes=15))
        except:
            m["zablokowany"] = False

    # 3. DOPIERO TERAZ PRZETWARZAMY ZAPIS
    if request.method == "POST":
        user = session.get("user")
        if user:
            for m in mecze:
                m_id = m["id"]
                if user == "Admin":
                    wg = request.form.get(f"wynik_g_{m_id}", "")
                    wb = request.form.get(f"wynik_b_{m_id}", "")
                    m["wynik_g"] = wg
                    m["wynik_b"] = wb
                
                # Zapis typów - teraz m["zablokowany"] ma poprawną, świeżą wartość!
                if user == "Admin" or not m.get("zablokowany", False):
                    tg = request.form.get(f"typ_g_{user}_{m_id}")
                    tb = request.form.get(f"typ_b_{user}_{m_id}")
                    if tg is not None and tb is not None:
                        typy[user][m_id]["typ_g"] = tg
                        typy[user][m_id]["typ_b"] = tb
            
            zapisz_dane()
            wiadomosc = "Dane zostały pomyślnie zapisane!"

    # 4. PRZELICZAMY RANKING NA BAZIE ŚWIEŻYCH DANYCH
    przelicz_wszystko()
    
    # Sortowanie rankingu
    posortowani = sorted(totale.items(), key=lambda x: x[1], reverse=True)
    
    ranking = []
    miejsce = 1
    for i, (g, pkt) in enumerate(posortowani):
        if i > 0 and posortowani[i][1] < posortowani[i-1][1]:
            miejsce = i + 1
        ranking.append((miejsce, g, pkt))
        
    podium = [(posortowani[0] if len(posortowani) > 0 else ("", 0)),
              (posortowani[1] if len(posortowani) > 1 else ("", 0)),
              (posortowani[2] if len(posortowani) > 2 else ("", 0))]

    return render_template_string(HTML_TEMPLATE, mecze=mecze, lista_graczy=lista_graczy, typy=typy, ranking=ranking, podium=podium, wiadomosc=wiadomosc)
