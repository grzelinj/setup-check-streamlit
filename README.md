# Setup Check Generator (Streamlit)

Prosta aplikacja webowa stworzona w **Streamlit**, która umożliwia:
- upload pliku Excel
- automatyczne wygenerowanie zestawu zapytań SQL
- pobranie wyniku jako plik `.txt`

Aplikacja jest przeznaczona do szybkiego przygotowania **setup checków** na podstawie danych z Excela.

---

## 🚀 Demo / Użycie

1. Otwórz aplikację w przeglądarce
2. Wgraj plik Excel (`.xlsx` lub `.xls`)
3. Aplikacja:
   - wyciąga unikalne wartości z kolumn
   - generuje gotowe template’y SQL
4. Skopiuj wynik lub pobierz go jako plik tekstowy

---

## 📂 Wymagana struktura Excela

Plik Excel **musi zawierać poniższe kolumny**:

- `PLAN`
- `FMV RULE ID`
- `PARTICIPATION ID`
- `UNDERLYING VEHICLE`
- `VEHICLE`
- `DISTRIBUTION RULE ID`

---

## 🛠 Technologie

- Python
- Streamlit
- Pandas
- openpyxl

---

## ▶️ Uruchamianie lokalnie

```bash
pip install -r requirements.txt
streamlit run app.py
