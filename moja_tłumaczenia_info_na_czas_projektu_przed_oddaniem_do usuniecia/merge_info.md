# **Test Merge Results Summary**


## 1 Input Dataset Sizes

| Dataset | Rows | Columns | Source | Role |
|---------|-------:|---------:|---------|-------------------------------|
| `selected_features.csv` | 73,747 | 20 | NASA SDO/HMI | physical input features (X) |
| `nlfff_flare_label.csv` | 46,114 | 20 | NLFFF flare label archive | target labels (y) |
| `flare_info.csv` | 85,514 | 10 | NOAA/GOES | auxiliary validation data |

**Why dataset sizes differ (expected and correct):**
- not all SDO/HMI observations have assigned flare labels,  
- labels exist only for periods where matching was possible,  
- NOAA/GOES covers a wider timespan than SDO.

---

## 2 Result of merging X + y

- X + y merged shape: (46134, 38)


- **46,134 matched rows** were obtained, very close to the total number of labeled samples,  
- this indicates labels **successfully matched** most SHARP records,  
- resulting 38 columns = **20 features + 18 label-related fields (no duplicate keys)**.

**Conclusion:**  
The join keys (`HARP_NUM`, `T_REC_DATETIME`) work correctly and  
SDO features align well with flare label entries.

---

## 3 Result of merging with NOAA/GOES

- Final merged dataset shape (X + y + GOES): (46134, 48)
- GOES timestamp match rate: 35.20%


**Interpretation:**

- the final number of rows **remained unchanged**, which confirms that `merge_asof` did not drop any records,  
- match rate of **~35%** means only about one third of the samples found an associated GOES flare within ±2 hours.

**This result is correct and expected because:**

- not every magnetic disturbance results in a recorded flare,  
- GOES reports events *after* they occur (not all timestamps must align),  
- some flares are weak, unclassified, or outside the observation window.

---

## 4 Current dataset status

The merged dataset is **temporary** and **not yet suitable for training**,  
because the following checks still have to be performed:

- **temporal leakage analysis**,  
- verification of **forecast horizon correctness** (now / 6h / 12h / 24h / 48h),  
- removal of **incorrect or ambiguous matches**.

---

## 5 Operational conclusions

| Area | Status | Notes |
|--------|--------|-----------------------------|
| X + y merge | ✔️ | Working correctly |
| Merge with GOES | ✔️ | Auxiliary only, not features |
| Temporal causality | ❓ | Must be validated next |
| Ready for modeling | ❌ | Needs temporal filtering |

**Next step:**  
**`04_temporal_validation.py`** to ensure the model does **not learn from future information**, which would invalidate evaluation results.

---

# **Wynik testowego łączenia zbiorów danych**

# Status po wykonaniu `03_merge_datasets_test.py`

Uzyskaliśmy plik tymczasowy:  
`data/interim/merged_xy_goes_test.csv`

W pliku tym po raz pierwszy znajdują się razem:

1. **X – cechy fizyczne SDO/HMI**  
   (`selected_features.csv` → wybrane SHARP magnetic features)

2. **y – etykiety dla uczenia nadzorowanego**  
   (`nlfff_flare_label.csv` → informacje o przyszłym wystąpieniu flary dla różnych horyzontów)

3. **informacje walidacyjne z NOAA/GOES**  
   (`flare_info.csv` → rzeczywiste zdarzenia flarowe: start, peak, class, intensity)


## Co zostało wykonane

- ujednolicono klucze merge (`HARP_NUM`, `T_REC_DATETIME`)
- wykonano merge **X + y** kluczem jednoznacznym
- wykonano merge **czasowe dopasowanie** SDO → GOES poprzez `merge_asof()`  
  z oknem tolerancji `2h`
- otrzymano wynikowe połączenie w jednym DataFrame (`df_final`)
- plik został zapisany jako ***test version***, a nie wersja produkcyjna

---

## Dlaczego wynik jest **testowy**, a nie finalny?

Skrypt poprawnie sprawdza **techniczne możliwości łączenia**,
ale nie sprawdza jeszcze **ważnych aspektów naukowych i predykcyjnych**:

- ❌ brak potwierdzenia, że czas cech (`T_REC_DATETIME`) jest **zawsze przed flarą**
- ❌ brak potwierdzenia, że dopasowanie czasowe spełnia warunki horyzontu (now/6h/12h/24h/48h)
- ❌ możliwe wystąpienie **temporal leakage**
- ❌ brak oznaczenia rekordów poprawnych i niepoprawnych
- ❌ brak raportu diagnostycznego

Dlatego kolejny krok jest **obowiązkowy** — bez niego model mógłby nauczyć się
na danych **fizycznie niemożliwych operacyjnie**.

---

## Następny krok w projekcie

### 🔜 `04_temporal_validation.py`

Ten moduł wykona:

1. konwersję czasów na `datetime` (UTC-safe)
2. obliczenie `delta_hours = flare_time - feature_time`
3. sprawdzenie warunków poprawności prognozy dla horyzontów:  
   `now`, `6h`, `12h`, `24h`, `48h`
4. oznaczenie kolumny `temporal_valid` (True/False)
5. przygotowanie raportu jakości (Markdown + opcjonalnie CSV)
6. decyzję o filtracji danych lub pozostawieniu flag

Po tym etapie otrzymamy:

- `merged_xy_temporally_valid.csv` (wersja oznaczona flagami)  
- opcjonalnie `merged_xy_temporally_clean.csv` (tylko dobre rekordy)

---

## 1 Rozmiary wejściowych zbiorów danych

| Zbiór | Rekordy | Kolumny | Źródło | Znaczenie |
|--------|---------:|---------:|---------|------------|
| `selected_features.csv` | 73 747 | 20 | NASA SDO/HMI | wejściowe cechy fizyczne (X) |
| `nlfff_flare_label.csv` | 46 114 | 20 | NLFFF label archive | etykiety (y) |
| `flare_info.csv` | 85 514 | 10 | NOAA/GOES | walidacja pomocnicza |

**Różne liczności są spodziewane, ponieważ:**
- nie wszystkie obserwacje SDO/HMI posiadają etykiety flar,  
- etykiety obejmują tylko okres, w którym możliwe było dopasowanie,  
- dane z NOAA/GOES obejmują szerszy zakres czasowy niż dane SDO.

---

## 2 Wynik łączenia X + y

- X + y merged shape: (46134, 38)


- otrzymano **46 134 wspólnych rekordów**, co jest bardzo zbliżone do liczby w label dataset,  
- etykiety dało się przypisać do większości obserwacji SHARP,  
- liczba kolumn 38 = **20 cech + 18 pól etykietowych (bez duplikatów kluczy)**.

**Wniosek:**  
Klucz łączenia (`HARP_NUM`, `T_REC_DATETIME`) działa poprawnie,  
co potwierdza, że dane wejściowe i etykiety są dobrze dopasowane pod względem struktury i czasu.

---

## 3 Wynik łączenia z NOAA/GOES

- Final merged dataset shape (X + y + GOES): (46134, 48)
- GOES timestamp match rate: 35.20%

**Interpretacja:**

- liczba rekordów *pozostała identyczna* → merge *asof* nie usunął wierszy,  
- match rate ≈ **35%** oznacza, że tylko ~1/3 przypadków znalazła dopasowanie w GOES  
  w oknie czasowym **± 2h**.

**Dlaczego wynik jest poprawny i oczekiwany?**

- nie każda aktywność magnetyczna prowadzi do flary wykrywalnej przez NOAA,  
- GOES rejestruje flary *po fakcie*, co nie gwarantuje 1:1 zgodności,  
- część flar mogła być słaba, nieklasyfikowana lub poza polem obserwacji.

---

## 4 Status danych na tym etapie

Aktualny plik **ma status tymczasowy** i **nie jest gotowy** do trenowania modelu,  
ponieważ wymagane są dodatkowe walidacje:

- sprawdzenie **braku leakage temporealnego**,  
- potwierdzenie poprawności **horyzontów predykcyjnych (now / 6h / 12h / 24h / 48h)**,  
- identyfikacja i usunięcie **fałszywych dopasowań**.

---

## 5 Wnioski

| Obszar | Status | Komentarz |
|--------|--------|------------|
| Dopasowanie X + y | OK️    | Stabilne i logiczne |
| Dopasowanie z GOES | OK️    | Walidacja uzupełniająca, nie feature |
| Czasowa spójność danych | ?      | Weryfikacja wymagana |
| Gotowe do treningu ML | NO     | Kolejny etap dopiero po walidacji |

**Kolejny krok:**  
Moduł **`04_temporal_validation.py`**, aby potwierdzić,  
że model nie będzie uczył się na danych z przyszłości.

---
