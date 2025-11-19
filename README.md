# Solar Flare Forecasting using NASA SDO (HMI) & NOAA GOES Data

Machine Learning project aimed at predicting the occurrence and intensity level of solar flares based on physical magnetic field parameters of solar active regions obtained from the HMI instrument on the NASA SDO satellite, combined with flare label data from NOAA GOES observations.

---

## Project Objective

The goal of this analysis is to develop predictive models capable of:

- forecasting the occurrence of a solar flare,
- predicting the intensity class level (B, C, M, X),
- analyzing forecasting time horizons: **0h, 6h, 12h, 24h, 48h**, 
- assessing the importance of physical magnetic features related to solar activity.

The project includes a **complete Data Science / ML pipeline** — from dataset acquisition, preprocessing, feature selection, model training, hyperparameter tuning (Optuna), up to model evaluation and interpretation.

---

## Data Sources

All datasets used in this project were obtained from official scientific institutions:

- https://nlfff.dataset.deepsolar.space/en/download/
- https://sdo.gsfc.nasa.gov
- https://www.swpc.noaa.gov/products/goes-x-ray-flux

Full dataset documentation can be found in:  
`docs/data_description.md`

---
## Important note on raw dataset exploration

The raw dataset (`nlfff_raw.csv`) contains 276 columns, including metadata, 
processing flags, geometric information and pipeline diagnostic values. 
Based on findings from space weather research (Bobra & Couvidat 2015; 
Nishizuka et al. 2018; Park et al. 2020), only physically meaningful 
magnetic SHARP features are relevant for solar flare prediction.

Therefore:
- We do NOT perform `.head()` / `.info()` / `.describe()` on the full raw dataset
- We first remove non-physical and non-causal features based on domain knowledge
- EDA is performed only on the **reduced**, scientifically relevant feature set

---

## Note on large data files !!!

The downloaded raw dataset files are very large (some exceed 100 MB).  
Do **not** commit them to GitHub at this stage.  
They will be added only after preprocessing and removing unnecessary columns  
to keep the repository lightweight and compatible with GitHub’s file size limits.

---
## Repository Structure

```text
project/
│
├── data/
│ ├── raw/ # Original downloaded CSV files (not committed to GitHub)
│ ├── interim/ # Cleaned & partially transformed datasets (temporary stage)
│ └── processed/ # Final modeling-ready datasets (features + target)
│
├── src/ AKTUALIZOWANY W TRAKCIE PISANIA PROJEKTU !!!
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

Feature selection and dataset merging were performed based on domain-relevant publications
(Bobra & Couvidat 2015; Nishizuka et al. 2018; Park et al. 2020) and supported by
interactive reasoning and code-generation assistance using ChatGPT (OpenAI) in a
co-pilot role. The final decisions regarding selected features, preprocessing
and merging logic were manually evaluated and validated by the author.