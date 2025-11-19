# Kontrola wartości brakujących i sanity-check po `04_temporal_validation.py`

Po wykonaniu kroku `04_temporal_validation.py`, w którym dodajemy kolumnę
`temporal_valid` oraz obliczamy różnicę czasową pomiędzy obserwacją SDO a
zdarzeniem flarowym, konieczne jest przeprowadzenie dodatkowej inspekcji
datasetu, zanim przejdziemy do EDA, FE i modelowania. 

Celem tego kroku jest upewnienie się, że dane są spójne, kompletne i
bezpieczne do dalszej analizy.

---

## 1. Sprawdzenie brakujących wartości (Missing Values)

Wartości brakujące mogą wystąpić w kilku miejscach:

### **1.1. Po stronie SDO/HMI (cechy X)**
Pole magnetyczne bywa niepełne dla niektórych AR:

- `USFLUX`, `MEANJZD`, `R_VALUE`, `GWILL`
- inne cechy mogą mieć braki w pierwszych latach misji SDO (2010)

Należy wykonać:

```python
df.isna().sum().sort_values(ascending=False)
