# Description of Selected Features Used in the Project (After Cleaning)

The following table lists all **retained variables** from the three main source data files:  
`nlfff_raw.csv`, `nlfff_flare_label.csv`, and `flare_info.csv`.

The selected features meet the following criteria:  
- physically meaningful and relevant to solar flare prediction,  
- supported by space weather research (SDO/HMI + SHARP),  
- no risk of data leakage,  
- useful for machine learning modeling.

---

## 1. Magnetic Field Physical Features (**X**)  
**File:** `nlfff_raw.csv`  
**Role:** model input features

| Name | Meaning |
|------|---------|
| **HARP_NUM** | Unique identifier of the active solar region (AR) – used only for merging, not included as a model feature. |
| **T_REC_DATETIME** | Timestamp of the physical observation (SDO/HMI record time) – used for synchronization only. |
| **USFLUX** | Total unsigned magnetic flux – describes the energy scale and size of the AR. |
| **MEANGAM** | Mean inclination angle of the magnetic field vector relative to the solar surface. |
| **MEANGBT** | Mean gradient of the total magnetic field strength – a measure of magnetic field variability. |
| **MEANGBZ** | Mean gradient of the vertical magnetic field component (Bz). |
| **MEANGBH** | Mean gradient of the horizontal magnetic field component. |
| **MEANJZD** | Mean vertical electric current density – linked to magnetohydrodynamic activity. |
| **TOTUSJZ** | Total unsigned vertical current within the active region. |
| **MEANALP** | Force-free alpha parameter (magnetic twist) – correlates with free magnetic energy. |
| **MEANJZH** | Mean current helicity – associated with magnetic instability. |
| **TOTUSJH** | Total unsigned current helicity – measures total stored helical energy. |
| **ABSNJZH** | Normalized current helicity – scaled variation suitable for AR comparisons. |
| **SAVNCPP** | Sum of net current per polarity – reflects current imbalance and instability. |
| **MEANPOT** | Mean free magnetic energy density. |
| **TOTPOT** | Total free magnetic energy of the AR. |
| **MEANSHR** | Mean magnetic shear angle – indicator of non-potential magnetic configuration. |
| **SHRGT45** | Percentage of pixels where magnetic shear exceeds 45° – strong indicator of M/X flares. |
| **R_VALUE** | Schrijver’s magnetic neutral line activity index – known strong flare precursor. |
| **GWILL** | Gradient-weighted integral length measure – alternative magnetic instability metric. |

---

## 2. Target Variables (Classification) (**y_class**)  
**File:** `nlfff_flare_label.csv`

| Name | Meaning |
|------|---------|
| **harp_num** | AR identifier used for merging – not a model feature. |
| **t_rec_datetime** | Observation timestamp – used only for time alignment. |
| **now_flare_level** | Current flare strength class associated with the observation time. |
| **h6_flare_level** | Forecast class for a 6-hour prediction window. |
| **h12_flare_level** | Forecast class for a 12-hour prediction window. |
| **h24_flare_level** | Forecast class for a 24-hour prediction window – **main classification target**. |
| **h48_flare_level** | Forecast class for a 48-hour prediction window. |
| **h24_posmx** | Binary indicator: M or X flare within 24 hours (0/1). |
| **h24_poscmx** | Binary indicator: C, M, or X flare within 24 hours (0/1). |
| **h48_posmx** | Same as above, but within 48 hours (M/X). |
| **h48_poscmx** | Same as above, but within 48 hours (C/M/X). |
| **h24_delta05** | Alternative binary target for 24-hour prediction. |
| **h48_delta05** | Alternative binary target for 48-hour prediction. |

---

## 3. Target Variables (Regression & Validation) (**y_reg**)  
**File:** `flare_info.csv`

| Name | Meaning |
|------|---------|
| **deeps_flare_id** | Flare identifier from the DeepSolar database – used for matching only. |
| **xray_intensity** | Peak X-ray flux value – used as the regression target. |
| **xray_class** | Official GOES flare class (A/B/C/M/X) – used for reporting and cross-validation. |
| **start_datetime** | Flare start time – not used as a feature. |
| **peak_datetime** | Flare peak time – used for validation only. |
| **end_datetime** | Flare end time – not used as a feature. |
| **latitude** | Heliographic flare latitude – optional for experimental modeling. |
| **longtitude** | Heliographic flare longitude – optional for experimental modeling. |

---

## Summary Logic

- Only **physical magnetic field features** from `nlfff_raw.csv` are used as inputs for modeling.  
- Classification and regression targets are taken from **separate** datasets.  
- Time fields and identifiers are **not** used as model features.  
- Joined dataset must preserve **temporal causality**.

```markdown
ML Model = f(USFLUX, MEANJZD, MEANSHR, ...) → {h24_flare_level, log10(xray_intensity)}
