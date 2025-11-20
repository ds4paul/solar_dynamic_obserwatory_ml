# Co robimy z brakami danych z raportu Missing Values?

Raport pokazał bardzo ważną rzecz: **braki nie są losowe**, tylko wynikają z fizyki zjawiska i konstrukcji datasetu.  

Kluczowa zasada:
**→ Nie uzupełniamy braków w sposób klasyczny (mean/median/knn/interpolacja), bo te braki mają sens fizyczny.**

Dlatego każdy typ braków wymaga innego podejścia.

---

# 1. Braki ekstremalne (>80%) — USUWAMY KOLUMNY
To są:

- `GWILL` — **100% braków**  
- `latitude` — ~87%  
- `longtitude` — ~87%

### Dlaczego usuwamy?
- `GWILL` jest *deprecated* przez autorów NLFFF (nieużywane w modelach fizycznych).  
- `latitude`, `longtitude` — są dostępne **tylko wtedy, gdy zarejestrowano flarę**.  
  Większość próbek to „no flare → brak lokalizacji”.  
  Nie można imputować, bo to nie są dane losowe, tylko realny brak zjawiska.

→ Te kolumny **nie mają zastosowania w naszym ML**.

### Decyzja:
✔ **Usuwamy te kolumny w 06_prepare_datasets.py**.

---

# 2. Wysokie braki (30–80%) — POZOSTAWIAMY, BO TO SĄ DANE GOES, KTÓRE MAJĄ ZNIKAĆ
Dotyczy:

- `start_datetime`, `peak_datetime`, `end_datetime`
- `xray_class`, `xray_intensity`
- `noaa_ar`
- `deeps_flare_id`
- `delta_hours`
- `source`

### Dlaczego jest tyle braków?

Te wartości istnieją **tylko dla rekordów, w których GOES wykrył flarę**.  
Wszystkie „no-flare” mają:

- brak xray_class
- brak peak_datetime
- brak start/end
- brak intensywności
- brak NOAA AR ID

**I to jest poprawne**.

Braki GOES oznaczają:

> „W tym czasie NIE było flary.”

### Czy imputować?  
❌ **Nie.**  
Nie można „zgadywać”, kiedy była flara, jaki miała pik, jaka klasa.

### Co robimy?

✔ Pozostawiamy te kolumny **bez zmian**.  
✔ Użyjemy ich **tylko do modelu regresyjnego i ewaluacji**, nie do predykcji.  
✔ W datasetach do ML **usuwamy te kolumny z X**, ale trzymamy je do raportów.

---

# 3. Małe braki (<5%) — UZUPEŁNIAMY WEDŁUG FIZYKI SDO
Dotyczy:

- `MEANSHR`
- `MEANPOT`
- `SHRGT45`
- `MEANGAM`
- `MEANGBT`  
…oraz innych cech SDO z 0.01–0.1% braków.

Te braki wynikają z wyjątów podczas estymacji pól magnetycznych (gaps w SHARP).

### Jak uzupełniamy?

👉 **Najprościej i najlepiej**: medianą **grupy HARP_NUM**.

Dlaczego?

- aktywne regiony mają stałą topologię pola magnetycznego,
- mediany w obrębie tego samego AR są fizycznie sensowne,
- jest to standard w literaturze (Bobra & Couvidat 2015).

W 06_prepare_datasets zrobimy:

```python
df[col] = df.groupby("HARP_NUM")[col].transform(lambda x: x.fillna(x.median()))
```

# 4. Kolumny LABEL i TECH — co robimy?

Kolumny etykiet (`LABEL`) oraz kolumny techniczne z procesów walidacji (`TECH`) **nie są danymi wejściowymi do modeli**, lecz pełnią funkcję informacyjną i pomocniczą.  
Dlatego obowiązuje zasada:

- ❌ **Nie imputujemy tych kolumn**  
- ❌ **Nie usuwamy ich**  
- ✔ **Zostawiamy je bez zmian**, bo są potrzebne do:
  - wyliczeń horyzontów czasowych,
  - walidacji poprawności dopasowania SHARP ↔ GOES,
  - budowy targetów dla modeli ML (klasyfikacja/regresja),
  - generowania raportów.

Przykłady kolumn, których **nie zmieniamy**:
- `now_flare_level`, `h6_flare_id`, `h24_flare_level`, `h48_posmx`,
- `valid_now`, `valid_6h`, `valid_12h`, `delta_hours`,
- `temporal_valid`.

---

# 5. Konkretne działania, które wykonamy w kroku 06_prepare_datasets.py

W kroku 06 przygotujemy finalne zbiory danych dla modeli ML.  
Skrypt wykona **cztery logiczne operacje**:

### **A) Usunięcie kolumn z ekstremalnymi brakami (>80%)**
Usuwamy:
- `GWILL`,
- `latitude`,
- `longtitude`.

**Powód:** kolumny są bezużyteczne dla ML, brakujące prawie zawsze i nie mają znaczenia fizycznego.

---

### **B) Usunięcie kolumn GOES z X (zestawu cech wejściowych)**  
Kolumny GOES (czas, intensywność, lokalizacja flary) są znane **dopiero po flarze**, czyli:

- są przyczyną **nieszczelności danych** (data leakage),
- nie mogą być używane jako cechy wejściowe do przewidywania flar,
- będą używane wyłącznie jako etykiety oraz do walidacji.

**X = tylko cechy SDO/SHARP.**

---

### **C) Uzupełnienie braków (<5%) w kolumnach SHARP medianą w obrębie aktywnego regionu HARP**

Dla nielicznych braków w cechach fizycznych SDO:

- `MEANSHR`, `MEANPOT`, `MEANGAM`, `MEANGBT`, `MEANGBH`, itd.

stosujemy:

```python
df[col] = df.groupby("HARP_NUM")[col].transform(lambda x: x.fillna(x.median()))
```

## Dlaczego tak?

Dla małych braków (<5%) w danych SHARP stosujemy imputację **medianą w obrębie aktywnego regionu HARP**, ponieważ:

- **Aktywne regiony (HARP) mają spójny charakter fizyczny**  
  Pola magnetyczne w obrębie jednego AR zmieniają się stopniowo, a nie skokowo → mediany są stabilne.

- **Imputacja globalna byłaby błędem**  
  AR 11158 ≠ AR 12673 — różnią się wielkością, klasą, historią aktywności.

- **Metody zaawansowane (KNNImputer, iterative imputer) nie mają sensu fizycznego**  
  Mogłyby “wymyślać” dane, których nie było.

- **Braki GOES nie są brakami, tylko informacją „brak flary”**  
  GOES nie rejestruje danych poza zdarzeniami → nie imputujemy ich w ogóle.

Dlatego:
- SDO/SHARP (<5% braków) → imputacja medianą w HARP.  
- GOES (duże braki) → **nic nie imputujemy**.  
- LABEL/TECH → zostawiamy bez zmian.

---

## 7. Podsumowanie decyzji

| Typ braków | Kolumny | Co robimy? | Uzasadnienie |
|------------|---------|------------|--------------|
| **>80%** | `GWILL`, `latitude`, `longtitude` | ❌ usuwamy | Prawie całkowicie puste → brak wartości fizycznej |
| **30–80%** (GOES) | `start_datetime`, `peak_datetime`, `xray_class`, `xray_intensity`, `delta_hours`, `source`, itp. | ✔ zostawiamy, ❌ nie uzupełniamy | Dane GOES istnieją tylko przy flarach; brak = brak zdarzenia |
| **<5%** (SHARP) | `MEANSHR`, `MEANGAM`, `MEANPOT`, `MEANGBZ`, `MEANGBH`, itp. | ✔ imputacja medianą w obrębie `HARP_NUM` | Fizycznie poprawne, stabilne statystycznie |
| **LABEL** | `now_flare_level`, `h6_flare_id`, `h24_flare_level`, `h48_posmx`, itp. | ✔ zostawiamy bez zmian | Targety dla ML |
| **TECH** | `valid_now`, `delta_hours`, `temporal_valid`, itp. | ✔ zostawiamy bez zmian | Potrzebne dla pipeline’u i walidacji |

---

**Efekt końcowy decyzji:**  
- Dane SHARP: **czyste i kompletne po imputacji medianą HARP**  
- Dane GOES: **pozostają nieimputowane (brak = brak flary)**  
- Targety i flagi techniczne: **bez zmian**  
- Zbiór gotowy do kroku **06_prepare_datasets.py**
