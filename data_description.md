# Data Description (NLFFF Dataset – Solar Active Regions + Flare Labels)

## Official Data Sources

https://nlfff.dataset.deepsolar.space/en/download/  
https://sdo.gsfc.nasa.gov  
https://www.swpc.noaa.gov/products/goes-x-ray-flux  

---

## 0. Dataset Download Source

Source:  
https://nlfff.dataset.deepsolar.space/en/download/#3-database-archive-files  

Original archive: **NLFFF Dataset and Flare Label Database Archive**

---

## 1. SQL Data Exported to CSV

The working data, exported from SQLite to `.csv` format, is available at:  
https://drive.google.com/drive/folders/1JJhNI2VePSgYyD1sM7Lv63ajUMJ-iElY?usp=sharing

---

## 2. Dataset Overview and File Structure

### 2.1 Contents of Individual Files

#### 1.1 `flare_info.csv`

Contains information on solar flares observed by **NOAA/GOES** satellites.  
This file represents the **outcome** (observational effect) dataset.  
It includes:  
- flare classes: **A, B, C, M, X**  
- start time  
- peak time  
- end time  
- peak X-ray radiation intensity (peak flux)

This file **remains in the project**, but is used **only** for:  
- validation  
- qualitative interpretation  
- sanity-check  
- *not* as ML model input features  

---

#### 1.2 `nlfff_flare_label.csv`

Contains flare labels time-aligned with **HARP/SHARP** observations from NASA SDO  
for multiple forecast windows, e.g.:

`now_flare_level, h6_flare_level, h12_flare_level, h24_flare_level, h48_flare_level`

Labels are based on:  
- flare strength  
- flare occurrence time  

This file remains in the project and forms the **core target variable (y)**  
for machine learning models.

---

#### 1.3 `nlfff_raw.csv`

Contains **physical magnetic field parameters** of solar active regions (*SHARP features*)  
retrieved from the **HMI instrument** on the **SDO satellite**.

This file serves as the **main source of input features (X)**.

It remains in the project **after feature selection** — only physically meaningful,  
magnetically relevant parameters are retained, while all fields that are:  
- technical  
- descriptive  
- file-related  
- geometric  
- quality-related  
are **removed**.

---

#### 1.4 `nlfff_archive.csv`

Contains archival records, metadata, intermediate values, and duplicated data  
overlapping with `nlfff_raw.csv`.  

This file **is removed** from the project and must **not** be used at any stage  
of ML modeling due to risk of:  
- **data leakage**  
- **false correlations**

---

## 3. Removed Fields and Justification

The following types of fields are removed:  
- technical  
- file-related  
- geometric  
- statistical  
- qualitative  
- metadata  

because they **do not carry physical predictive value** for flare forecasting.

Examples of excluded fields:  
`FILE_NAME, CONTENT, ORIGIN, CTYPE*, CRPIX*, CRVAL*, CDELT*, CROTA2, QUALITY, QUAL_S, QUALLEV*, FITS paths, BUNIT*, DATA*, MISSVAL*, DATAMIN*, DATAMAX*, DATAMEAN*, DATARMS*, comments, pipeline version fields, documentation-related fields.`

Time-based fields such as `T_REC`, and identifiers such as `HARP_NUM`,  
are kept **only for merging tables**,  
but **not** included as ML features.

---

## 4. Final File Usage Summary

| File | Project Role |
|------|--------------|
| **nlfff_raw.csv** | Main input features (X) |
| **nlfff_flare_label.csv** | Target variables (y) |
| **flare_info.csv** | Validation and auxiliary analysis (not features) |
| **nlfff_archive.csv** | Removed / archived (leakage risk) |

---

## 5. Table Joining Rules

- Tables are joined using a **composite key**:  
  **`HARP_NUM` + `T_REC`**

- Input features (X) must originate **before** the target (y) timestamp.

- It is strictly forbidden to use any variable **created after the flare event**  
  as an input feature, due to **data leakage risk**.

---

## 6. Final Logical Dataset Pipeline

- `nlfff_raw.csv` → physical feature selection → preprocessing & scaling  
- `nlfff_flare_label.csv` → target extraction + optional encoding  
- optional `flare_info.csv` → validation and result interpretation  
- `X + y` → ML models (classification, regression, ordinal classification, multi-horizon forecasting)

---

## 7. Full Variable Meaning Reference (Data Dictionary)

### 7.1 Key Variables (Not Used as Features)

- **HARP_NUM** – numerical identifier of the solar active region (SHARP/HARP)  
- **T_REC** – observation timestamp in TAI time format  

---

### 7.2 Physical Magnetic Parameters Used as Input Features (X)

`USFLUX` – total unsigned magnetic flux  
`MEANGAM` – mean magnetic field inclination angle  
`MEANGBT` – mean gradient of total magnetic field  
`MEANGBZ` – mean vertical gradient of Bz magnetic field component  
`MEANGBH` – mean gradient of horizontal magnetic field component  
`MEANJZD` – mean vertical electric current density  
`TOTUSJZ` – total unsigned vertical electric current  
`MEANALP` – mean alpha parameter (magnetic twist)  
`MEANJZH` – mean current helicity  
`TOTUSJH` – total unsigned current helicity  
`ABSNJZH` – normalized helicity parameter  
`SAVNCPP` – sum of net current per polarity  
`MEANPOT` – mean free magnetic energy density  
`TOTPOT` – total free magnetic energy  
`MEANSHR` – mean shear angle between observed and potential field  
`SHRGT45` – percentage of pixels where shear angle > 45°  
`R_VALUE` – Schrijver coronal neutral line activity index (PIL)  
`GWILL` – alternative magnetic gradient index  

---

### 7.3 Target Variables in `nlfff_flare_label.csv`

- `now_flare_level`
- `h6_flare_level`
- `h12_flare_level`
- `h24_flare_level`
- `h48_flare_level`

Class interpretation:  
`0 = no flare`  
`1 = B`  
`2 = C`  
`3 = M`  
`4 = X`  

---

### 7.4 Auxiliary Variables in `flare_info.csv` (Validation Only)

`start_time` – flare start timestamp  
`peak_time` – peak time  
`end_time` – end timestamp  
`peak_flux` – peak X-ray intensity  
`class` – official NOAA flare class (A, B, C, M, X)  
`noaa_region` – NOAA active region identifier  

---

## 8. Final Feature Selection Decision

Only **physical magnetic features** from `nlfff_raw.csv` are kept as input (X),  
and only **flare horizon labels** from `nlfff_flare_label.csv` are used as targets (y).  

Time variables and unique identifiers are used **solely for joining** tables,  
while all other variables including:  

- technical  
- imaging  
- descriptive  
- geometric  
- metadata  
- full `nlfff_archive.csv`  

are removed due to **lack of predictive value**  
and **high data leakage risk**.

