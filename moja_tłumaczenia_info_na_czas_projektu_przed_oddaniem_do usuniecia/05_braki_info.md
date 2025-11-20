# Interpretacja wyników Missing Values (po kroku 05)

Otrzymałem wynik:

- GWILL = 100% braków  
- większość kolumn GOES (xray_intensity, xray_class, peak_datetime itd.) = 64.8% braków  
- latitude / longitude ~87% braków  
- noaa_ar ~80% braków  
- fizyczne cechy SHARP mają praktycznie **brak braków** (tylko minimalne 0.01%)

To jest **dokładnie to, czego spodziewamy się** po merge SDO → GOES.

---

# 1. Dlaczego niektóre kolumny mają tak dużo braków?

## ✔ GWILL – 100% braków  
Kolumna GWILL (gradient-weighted integral length scale) **prawie zawsze** ma braki w NLFFF datasetach.  
Możemy ją **usunąć całkowicie**.  
Jest nieużywana w literaturze.

---

## ✔ GOES: xray_intensity / class / peak_datetime → 64.8% braków  
To jest **normalne**, bo:

- większość obserwacji SDO **nie ma flary** (flary są rzadkie),  
- merge_asof dopasowuje tylko przypadki, gdzie flara wystąpiła blisko w czasie,  
- nawet jeśli jest AR, to flara może nie rozwinąć się z tego AR,  
- tylko ~1/3 rekordów ma dopasowanie GOES (co pokrywa się z temporal_valid = 34.8%).

**Wniosek:**

- dla **klasyfikacji** → brak GOES **nie jest problemem**,  
- dla **regresji** → musimy wybrać tylko próbki z GOES (bez braków).

---

## ✔ latitude / longitude / noaa_ar → bardzo dużo braków  
To są metadane GOES.  
Nie są cechami fizycznymi SHARP.  
Możemy:

- zostawić je *opcjonalnie* do analizy opisowej,  
- ale do modelu ML raczej je **usuwamy**.

---

## ✔ Fizyczne cechy magnetyczne SHARP → prawie brak braków  
To fantastyczna wiadomość — jakość danych SHARP jest wysoka.

Minimalne braki (<0.02%) można:

- uzupełnić medianą, albo
- po prostu usunąć kilka wierszy.

---

# 2. Co z tym robię w projekcie?

## ✔ KROK 1 – usuwam całkowicie kolumny bezużyteczne
- `GWILL`
- `noaa_ar`
- `source` (jeśli niepotrzebne)
- latitude / longitude (opcjonalnie)

## ✔ KROK 2 – decydujem o regresji i klasyfikacji

### **A) Klasyfikacja (y from nlfff_flare_label.csv)**
Brak GOES **nie wpływa** na klasyfikację.
Można używać pełny zbiór z `temporal_valid==True`.

### **B) Regresja (xray_intensity, log10)**  
Regresji **nie możemy zrobić** na rekordach bez GOES.  
Więc:

```python
df_reg = df.dropna(subset=["xray_intensity"])
