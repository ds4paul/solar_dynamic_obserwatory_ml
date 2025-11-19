# Czym są fizyczne parametry SHARP (SHARP features)?

**SHARP = Spaceweather HMI Active Region Patches**

To specjalny zestaw parametrów fizycznych, wyliczanych przez zespół NASA
dla każdego aktywnego regionu (Active Region, AR) obserwowanego przez
instrument **HMI** na satelicie **SDO (Solar Dynamics Observatory)**.

Celem SHARP jest:
- opisywać **pole magnetyczne** aktywnych regionów Słońca,
- monitorować ich **aktywność**,
- przewidywać **rozbłyski słoneczne (solar flares)**,
- dostarczać fizyczne cechy wejściowe dla modeli prognozowania pogody kosmicznej.

---

# Co mierzą SHARP features?

Są to ilościowe parametry związane z:
- **natężeniem pola magnetycznego**,
- **gradientami pola**,
- **prądem elektrycznym w plazmie**,
- **skręceniem pola (helicity)**,
- **shear** (odchyleniem od potencjalnego pola),
- **złożonością magnetyczną**.

Są to fizyczne wielkości opisujące aktywny region, które w literaturze
są skorelowane z prawdopodobieństwem wystąpienia flary.

---

## Przykłady głównych SHARP features (które masz w projekcie)

### 1. USFLUX  
Całkowity strumień pola magnetycznego poziomego.

### 2. MEANGAM  
Średnie pochylenie pola magnetycznego (gamma angle).

### 3. MEANGBT / MEANGBZ / MEANGBH  
Średnie gradienty pola magnetycznego:  
- BT = transversal (poziomy)  
- BZ = vertical (pionowy)  
- BH = total horizontal

### 4. MEANJZD  
Średnia gęstość prądu pionowego (current density).

### 5. TOTUSJZ  
Całkowita pionowa gęstość prądu.

### 6. MEANALP  
Parametr α (alfa), który opisuje skręcenie pola magnetycznego.

### 7. MEANJZH / TOTPOT  
Parametry związane z energią wolną i helicity.

### 8. R_VALUE  
Parametr Schrijvera – miara złożoności aktywnego regionu (bardzo silny predyktor flar).

### 9. SHRGT45  
Udział pola o shear >45°.

Te cechy pochodzą z rekonstrukcji wektorowego pola magnetycznego na powierzchni.

---

# Dlaczego SHARP features są tak ważne?

1. **Najważniejsze znane predyktory flar słonecznych** na podstawie
   fizyki pola magnetycznego.
2. Używane we wszystkich ważnych publikacjach:
   - Bobra & Couvidat (2015)
   - Nishizuka et al. (2017, 2018)
   - Jonas et al. (2021)
   - NASA/NOAA space weather forecasting
3. Są obliczone z instrumentu **HMI** co 12 minut.
4. Właśnie na ich podstawie buduje się najbardziej skuteczne modele ML.

---

# W projekcie Solar Flare ML

To właśnie **SHARP features** stanowią zbiór X  
(w pliku `selected_features.csv`).

To są:
- dane wejściowe do klasyfikacji,
- dane wejściowe do regresji,
- dane do PCA,
- dane do SHAP i interpretacji modeli.

Modele uczą się zależności między **strukturą pola magnetycznego**,  
a tym, czy region wywoła **flare**, oraz jak **silny** rozbłysk powstanie.

