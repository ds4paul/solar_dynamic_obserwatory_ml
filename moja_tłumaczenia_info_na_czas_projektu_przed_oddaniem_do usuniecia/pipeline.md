# Kompletny pipeline projektu Solar Flare Forecasting (SDO + GOES)

Poniżej przedstawiony jest uporządkowany workflow projekt.

---

## 1. Wczytanie danych (Data Loading)

**Źródła danych:**

- `selected_features.csv` — cechy fizyczne (X)
- `nlfff_flare_label.csv` — klasyfikacyjne etykiety flar (y_class)
- `flare_info.csv` — informacje o flarach GOES (y_reg)
- `merged_xy_temporally_valid.csv` — finalne wyniki po walidacji czasowej

**Czynności:**
- wczytanie datasetów
- konwersja kolumn datetime
- podstawowa sanity-check: liczba rekordów, brakujące dane, zakres dat
- analiza spójności kluczy (`HARP_NUM`, `T_REC_DATETIME`)

---

## 2. Exploratory Data Analysis (EDA)

### 2.1. Statystyki podstawowe
- `df.describe()`
- rozkłady cech fizycznych (histogramy)
- rozkład klas dla horyzontów 6h/12h/24h/48h

### 2.2. Korelacje i współliniowość
- macierz korelacji Pearson/Spearman
- heatmapa
- wyszukiwanie cech z wysoką korelacją (|r| > 0.9)

### 2.3. Analiza ekstremów i anomalii
- wykres pudełkowy (boxplot)
- IQR
- **Isolation Forest** (rekomendowane do dużych zbiorów)

### 2.4. PCA (Principal Component Analysis)
- obliczenie PCA dla standaryzowanych cech
- procent wyjaśnionej wariancji
- wykres komponentów PCA 1 vs PCA 2

---

## 3. Feature Engineering (FE)

### 3.1. Przygotowanie X
- skalowanie (`StandardScaler`, `MinMaxScaler`)
- opcjonalne transformacje log (np. log USFLUX)
- redukcja wymiaru (PCA opcjonalne)

### 3.2. Przygotowanie y (klasyfikacja)
Dla każdego horyzontu czasowego tworzymy:
- `y_now`
- `y_6h`
- `y_12h`
- `y_24h`
- `y_48h`

### 3.3. Przygotowanie y (regresja)
- `xray_intensity`  
- `log10_xray_intensity` *(najczęściej używane)*

---

## 4. Usuwanie outlierów (Isolation Forest)

- trenujemy model `IsolationForest(contamination=0.01–0.05)`
- odrzucamy punkty oznaczone jako anomalia
- powtórnie sprawdzamy rozkłady cech

---

## 5. Podział danych (Train/Test split)

**Zachowujemy walidację czasową**:
- dane są sortowane po czasie
- test zawiera najnowszy fragment danych, np. 20–30%

---

## 6. Model Benchmark (Baseline)

Przed zaawansowanymi modelami robimy prosty benchmark:

### 6.1. Baseline dla klasyfikacji:
- model przewidujący najczęstszą klasę
- model przewidujący rozkład proporcji

### 6.2. Baseline dla regresji:
- przewidywanie średniej intensywności flary
- RMSE baseline

---

## 7. Trenowanie modeli (Classification & Regression)

### 7.1. Modele klasyfikacyjne:
- Logistic Regression
- RandomForestClassifier
- XGBoostClassifier
- SVC (opcjonalnie)
- LightGBMClassifier

### 7.2. Modele regresyjne:
- Linear Regression
- Ridge Regression
- RandomForestRegressor
- XGBoostRegressor
- LightGBMRegressor

---

## 8. Optymalizacja hiperparametrów (OPTUNA)

### 8.1. Używamy Optuna:
- wybór modelu
- przestrzeń hiperparametrów
- optymalizacja F1-score (klasyfikacja)
- optymalizacja RMSE / MAE (regresja)

### 8.2. Wyniki Optuny:
- najlepsze hiperparametry
- najlepsze parametry modelu
- porównanie z baseline

---

## 9. Wyjaśnialność modeli (Explainability)

### 9.1. SHAP (ważność cech i kierunek wpływu)
- summary plot
- beeswarm plot
- decision plot dla pojedynczej obserwacji
- SHAP przez model klasyfikacyjny i regresyjny

### 9.2. Partial Dependence Plot (PDP)
- PDP dla wybranych cech fizycznych (np. USFLUX, TOTUSJZ)
- ICE curves (opcjonalnie)

---

## 10. Interpretacja rezultatów (Model Interpretation)

- które cechy magnetyczne najbardziej wpływają na predykcję flar?
- porównanie klasyfikacji vs regresji
- wnioski fizyczne (np. rola TOTUSJZ, USFLUX, R_VALUE)
- wnioski operacyjne (przydatność dla prognoz)

---

# Podsumowanie końcowe (zaliczenie)

Zgodnie z wymaganiami zaliczenia projekt musi zawierać:

1. **Wczytanie danych**
2. **Feature Engineering**
3. **Model**
4. **Optymalizacja (Optuna)**
5. **SHAP**
6. **Interpretacja wyników**
7. **PDP (Partial Dependence Plot)**
8. **Outliers – Isolation Forest**
9. **Benchmark model**
10. **Raport + wnioski**