# Solar Flare Forecasting using NASA SDO (HMI) & NOAA GOES Data

Projekt Machine Learning służący do prognozowania wystąpienia oraz intensywności rozbłysków słonecznych (solar flares) na podstawie fizycznych parametrów magnetycznych aktywnych regionów Słońca, pozyskanych z instrumentu HMI satelity NASA SDO oraz etykiet rozbłysków NOAA GOES.

---

## Cel projektu

Celem analizy jest opracowanie modeli predykcyjnych, które umożliwią:

- przewidywanie wystąpienia rozbłysku słonecznego,
- prognozowanie poziomu jego intensywności (klasy B, C, M, X),
- analizę horyzontów czasowych: **0h, 6h, 12h, 24h, 48h**,
- ocenę znaczenia fizycznych cech magnetycznych dla aktywności słonecznej.

Projekt obejmuje **pełny pipeline Data Science / ML** — od pozyskania danych, przez ich przetwarzanie, analizę, selekcję cech, trenowanie modeli, strojenie hiperparametrów (Optuna), aż po interpretację wyników.

---

## Źródła danych

Zbiory danych wykorzystane w projekcie pochodzą z oficjalnych instytucji naukowych:

- https://nlfff.dataset.deepsolar.space/en/download/
- https://sdo.gsfc.nasa.gov
- https://www.swpc.noaa.gov/products/goes-x-ray-flux

Szczegółowa dokumentacja danych znajduje się w:  
`docs/data_description.md`

---

## Struktura repozytorium

```text
project/
│
├── data/
│   ├── raw/            # oryginalne pliki .csv / eksport z SQL
│   ├── interim/        # dane częściowo przetworzone
│   └── processed/      # dane gotowe do modelowania
│
├── src/
│   ├── 01_load_data.py
│   ├── 02_preprocessing.py
│   ├── 03_feature_engineering.py
│   ├── 04_model_training.py
│   ├── 05_hyperparameter_tuning_optuna.py
│   └── 06_evaluation_and_interpretation.py
│
└── docs/
    ├── data_description.md
    └── model_notes.md

### Uwaga dotycząca dużych plików danych !!!

Pobrane surowe pliki datasetu są bardzo duże (niektóre przekraczają 100 MB).  
Na tym etapie **nie należy** dodawać ich do GitHuba (commit/push).  
Zostaną uwzględnione dopiero po przeprowadzeniu preprocessingu  
i usunięciu zbędnych kolumn, aby repozytorium pozostało lekkie  
oraz zgodne z ograniczeniami rozmiaru plików narzucanymi przez GitHub.
