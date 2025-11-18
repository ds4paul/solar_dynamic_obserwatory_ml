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

## Ważna uwaga dotycząca eksploracji danych surowych

Zbiór `nlfff_raw.csv` zawiera 276 kolumn, w tym metadane, znaczniki jakości, 
informacje geometryczne oraz wartości diagnostyczne wynikające z pipeline’u 
przetwarzania danych. Zgodnie z literaturą naukową dotyczącą prognozowania 
rozbłysków słonecznych (Bobra & Couvidat 2015; Nishizuka et al. 2018; Park et al. 2020) 
do modelowania wykorzystuje się wyłącznie **fizyczne i przyczynowe parametry 
magnetyczne SHARP**, powiązane z energią i niestabilnością pól magnetycznych 
w aktywnych regionach Słońca.

W związku z tym:
- **nie** wykonujemy `.head()` / `.info()` / `.describe()` na pełnym surowym zbiorze danych,
- **najpierw** usuwamy zmienne nie-fizyczne oraz nie-przyczynowe na podstawie wiedzy domenowej,
- EDA wykonujemy **dopiero po** selekcji cech, dla zbioru **zredukowanego i naukowo uzasadnionego**.

---

## Uwaga dotycząca dużych plików danych

Pobrane surowe pliki danych są bardzo duże (niektóre przekraczają 100 MB).  
Na tym etapie **nie należy** dodawać ich do repozytorium GitHub.  
Będą dodane dopiero po przeprowadzeniu selekcji zmiennych oraz redukcji rozmiaru,  
tak aby repozytorium pozostało lekkie oraz zgodne z ograniczeniami GitHub 
(dotyczy plików przekraczających 100 MB).

## Struktura repozytorium

```text
project/
│
├── data/
│ ├── raw/ # Original downloaded CSV files (not committed to GitHub)
│ ├── interim/ # Cleaned & partially transformed datasets (temporary stage)
│ └── processed/ # Final modeling-ready datasets (features + target)
│
├── src/
│ ├── config.py # Central configuration (paths, globals)
│ ├── 00_download_data.py # Downloading raw data from Google Drive
│ ├── 01_load_data.py # Loading CSV files into DataFrames
│ ├── 02_select_features.py # Selecting physical & causal SHARP feature set
│ ├── 03_feature_engineering.py # Encoding, scaling, transformations
│ ├── 04_model_training.py # Baseline & final model training
│ ├── 05_optuna_tuning.py # Hyperparameter optimization using Optuna
│ ├── 06_evaluation.py # Evaluation metrics, reports & visualizations
│ │
│ └── utils/ # Helper module with reusable functions
│   ├── plotting.py # Visualization utilities (EDA, metrics, SHAP)
│   ├── dimensionality.py # PCA, t-SNE, feature reduction tools
│   ├── model_helpers.py # Model registry, pipelines, wrappers
│   ├── explainability.py # SHAP, feature importance, PDP/ICE plots
│   └── metrics.py # Custom evaluation metrics
│
└── docs/
    ├── data_description.md # Full dataset and feature documentation
    └── model_notes.md # Notes, observations, and experiment logs

