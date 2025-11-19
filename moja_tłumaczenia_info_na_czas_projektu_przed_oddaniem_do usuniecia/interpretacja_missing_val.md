# Interpretacja Missing Values Report

Poniżej znajduje się kompletna, spójna i uporządkowana interpretacja raportu braków danych (`Missing Values Report`) 
wygenerowanego w kroku **05_missing_values_check.py**. Jest to wyjaśniona analiza: skąd się biorą braki, czy 
są normalne, czy są problemem, co oznaczają w kontekście fizyki Słońca i pipeline’u ML oraz co dokładnie robimy dalej 
w projekcie.

---

# 1. Co pokazuje raport Missing Values?

Raport informuje, ile wartości brakuje w każdej kolumnie po scaleniu danych SHARP (SDO), etykiet flar (LABEL) i informacji GOES. Wynik:

- **Rows:** 46 134  
- **Columns:** 55  
- **Global missing:** 15.863%  
- **Ogromne braki dotyczą prawie wyłącznie kolumn GOES**, a nie SDO.

To jest normalne i oczekiwane w danych astrofizycznych.

---

# 2. Severe missing (>80%) — dlaczego tak jest?

Najcięższe braki:

| Kolumna      | % braków | Źródło |
|--------------|----------|--------|
| GWILL        | 100%     | SDO    |
| latitude     | 87%      | GOES   |
| longtitude   | 87%      | GOES   |

## GWILL (SDO) — 100% braków (normalne)
NASA w dokumentacji NLFFF podaje, że `GWILL` jest kolumną *placeholder*, niewykorzystywaną fizycznie.  
Dlatego zawsze ma 100% braków.

→ **Usuwamy ją całkowicie.**

## latitude / longtitude (GOES) — 87% braków
Większość flar w bazie NOAA GOES nie ma przypisanych współrzędnych, bo GOES obserwuje całe Słońce i nie lokalizuje regionów na powierzchni tak precyzyjnie jak SDO/HMI.

→ **Nie używamy jako cech ML.**

---

# 3. High missing (30–80%) — przyczyna i interpretacja

Kolumny z ~65–80% braków:

- `peak_datetime`  
- `xray_intensity`, `xray_class`
- `start_datetime`, `end_datetime`
- `delta_hours`
- `noaa_ar`
- `source`
- `deeps_flare_id`

## Skąd te braki?

### 🔹 Powód 1: GOES rejestruje tylko nieliczne flary  
SDO/HMI zbiera dane *ciągle*, co 12 min, ale flary są:

- rzadkie,
- krótkotrwałe,
- trudne do dopasowania czasowo,
- nie zawsze w pełni opisane.

Dlatego większość pomiarów SHARP **nie ma dopasowanej flary**.

### 🔹 Powód 2: merge_asof dopasuje tylko flary:
- które wystąpiły po pomiarze,
- w tolerancji 2 godzin,
- z prawidłowym timestampem.

### 🔹 Powód 3: braki metadanych w NOAA  
NOAA w wielu przypadkach nie podaje regionu (`noaa_ar`), intensywności (`xray_intensity`) ani pozycji (`latitude`, `longtitude`).

## Czy to problem?

**Nie.**

Te kolumny GOES:
- nie są feature’ami do modeli ML,
- służą jedynie do walidacji czasowej,
- w żadnym wypadku nie mogą być używane jako wejście modelu.

Dlatego ich braki **nie wpływają negatywnie na uczenie maszynowe**.

---

# 4. Moderate missing (5–30%) — brak takich przypadków

Raport pokazuje:

✔ **Brak kolumn o umiarkowanych brakach.**

To dobra wiadomość i oznacza czyste dane wejściowe.

---

# 5. Light missing (<5%) — to cechy SHARP, czyli świetna jakość danych ML

Braki ~0.011% dotyczą wyłącznie cech SHARP (np. `MEANSHR`, `MEANGAM`, `MEANPOT`).  
Wszystkie mają dokładnie **5 braków na 46 134 rekordy**.

To kompletnie zaniedbywalne.

## Jak z tym postąpić?

→ **Imputacja medianą w kroku 07_feature_engineering jest idealna i w pełni bezpieczna.**

---

# 6. Co to oznacza dla modeli ML?

### ✔ Feature’y ML będą pochodzić niemal wyłącznie z SDO  
To dokładnie tak, jak w literaturze NASA i Stanforda:

- SHARP = cechy wejściowe (X)
- GOES = target (y)
- GOES metadane ≠ feature’y

### ✔ Duże braki w GOES nie są problemem  
Dlaczego?

Bo GOES **nie jest źródłem cech**, tylko źródłem etykiet i informacji o flarach.

### ✔ Dane SHARP są niemal kompletne  
To ogromna zaleta tego datasetu — idealnego do ML.

---

# 7. Co robimy dalej? Plan kolejnych kroków

## 7.1. Do usunięcia w kroku 06 EDA
Kolumny:
- `GWILL`
- `latitude`, `longtitude`
- `source`
- `noaa_ar`
- `deeps_flare_id`
- `xray_class`, `xray_intensity`
- `peak_datetime`, `start_datetime`, `end_datetime`
- `delta_hours`

Są z GOES, niepotrzebne jako feature.

## 7.2. Kolumny techniczne do usunięcia
- `valid_now`, `valid_6h`, `valid_12h`, `valid_24h`, `valid_48h`
- `temporal_valid`
- `harpnum_trec`, `t_rec_str`

Użyte tylko do walidacji temporalnej.

## 7.3. Cechy SHARP — zostają jako feature’y ML
- USFLUX  
- MEANGAM  
- MEANGBT  
- MEANGBZ  
- MEANGBH  
- MEANJZD  
- MEANALP  
- MEANJZH  
- TOTUSJZ  
- TOTUSJH  
- ABSNJZH  
- SAVNCPP  
- MEANPOT  
- TOTPOT  
- MEANSHR  
- SHRGT45  
- R_VALUE  

## 7.4. Kolumny LABEL — zostają jako target ML
- now/h6/h12/h24/h48 poziomy flar  
- h24_posmx, h24_poscmx  
- h48_posmx, h48_poscmx  
- h24_delta05, h48_delta05  

---

# 8. Podsumowanie

- Braki w danych **są w pełni normalne** dla misji SDO/GOES.  
- Dane SHARP (cechy ML) są prawie kompletne.  
- Dane GOES (etykiety i metadane) mają duże braki, lecz **nie są feature’ami**, więc nie przeszkadzają.  


---
