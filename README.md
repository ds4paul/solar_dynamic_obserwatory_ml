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

## Repository Structure

```text
project/
│
├── data/
│   ├── raw/            # original .csv files / SQL export
│   ├── interim/        # partially processed data
│   └── processed/      # data prepared for modeling
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
