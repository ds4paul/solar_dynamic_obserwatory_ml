# Jak w projekcie wykorzystujemy dane do zadań: klasyfikacji i regresji?

Po wykonaniu merge w `03_merge_datasets_test.py` oraz po walidacji czasowej
w `04_temporal_validation.py`, dataset zawiera informacje potrzebne do dwóch
różnych typów zadań uczenia maszynowego:

---

## 1. Klasyfikacja (classification)
Klasyfikacja korzysta z etykiet symbolicznych (kategoriowych) pochodzących
z pliku `nlfff_flare_label.csv`, takich jak:

- `now_flare_level`
- `h6_flare_level`
- `h12_flare_level`
- `h24_flare_level`
- `h48_flare_level`

Każda z tych zmiennych reprezentuje odpowiedź na pytanie:

**„Czy w ciągu X godzin od obserwacji wystąpi flara i jakiej klasy?”**

Przykładowe klasy:
- 0 = brak flary
- 1 = C-class
- 2 = M-class
- 3 = X-class  
(lub podobne oznaczenia w zależności od kodowania)

Te etykiety służą do trenowania modeli takich jak:
- Logistic Regression
- RandomForestClassifier
- XGBoostClassifier
- SVM
- LightGBM
- sieci neuronowe do klasyfikacji

---

## 2. Regresja (regression)
Regresja korzysta z numerycznych wartości pochodzących z katalogu GOES
(`flare_info.csv`), które zostały dopasowane czasowo w kroku 03:

- `xray_intensity` (np. wartość w jednostkach W/m²)
- `xray_class` przekształcone na wartość numeryczną,
  np. C ↦ 1e−6, M ↦ 1e−5, X ↦ 1e−4
- czas trwania flary (optional)
- log10(intensity) – najczęściej używana etykieta regresyjna w literaturze

Regresja odpowiada na pytanie:

**„Jak duża będzie intensywność rozbłysku, jeśli wystąpi?”**

Modele, które tu stosujemy:
- Linear Regression
- Ridge/Lasso Regression
- RandomForestRegressor
- XGBoostRegressor
- LightGBMRegressor
- sieci neuronowe do regresji

---

## 3. Dlaczego walidacja czasowa (krok 04) jest kluczowa dla obu zadań?

- W klasyfikacji chroni przed tym, żeby model nie widział cech zmierzonych
  **po flarze**, co prowadziłoby do fałszywie wysokich metryk.
- W regresji chroni przed sytuacją, gdy model próbowałby przewidywać
  intensywność flary na podstawie pomiarów wykonanych już *podczas* lub
  *po* rozbłysku.

Bez walidacji czasowej regresja byłaby zupełnie niewiarygodna —
intensywność flary jest zawsze wynikiem, nie wejściem.

---

## 4. Jak pipeline łączy klasyfikację i regresję?

Po kroku 04 otrzymujemy dataset z trzema grupami kolumn:

1. **X — cechy fizyczne SDO/HMI**
2. **y_class — etykiety klasyfikacyjne na horyzonty czasowe**
3. **y_reg — etykiety regresyjne z GOES (intensywność flary)**

Dalej możemy:

- trenować modele klasyfikacyjne osobno dla horyzontów 6h, 12h, 24h, 48h,
- trenować model regresyjny dla intensywności flary (log10),
- porównać oba podejścia (np. klasyfikacja ordinalna vs regresja ciągła),
- analizować SHAP i feature importance w obu przypadkach.

---

## 5. Pipeline końcowy (w kontekście regresji)

1. `02_selected_features.py` — wybór X  
2. `03_merge_datasets_test.py` — dorzucenie y_class + y_reg  
3. `04_temporal_validation.py` — sprawdzamy, czy X → Y ma sens czasowy  
4. `05_prepare_final_dataset.py` — tworzymy finalne:
   - `X_train_class`, `y_train_class`
   - `X_train_reg`, `y_train_reg`
5. `06_train_models.py` — osobne modele:
   - klasyfikacyjne
   - regresyjne
6. `07_model_evaluation.py` — pełna ewaluacja
7. `08_shap_analysis.py` — interpretacja dla klasyfikacji i regresji

To właśnie krok 03 sprawił, że **regresja stała się możliwa**,  
a krok 04 sprawi, że będzie **poprawna naukowo i czasowo**.

---

# Podsumowanie
W pipeline przewidziana jest zarówno **klasyfikacja**, jak i **regresja**.
Regresja jest możliwa dopiero po połączeniu danych z GOES (krok 03)  
i staje się *wiarygodna* dopiero po walidacji czasowej (krok 04).
