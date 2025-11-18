# Opis wybranych cech wykorzystanych w projekcie (po czyszczeniu)

Poniżej znajduje się lista wszystkich **pozostawionych** zmiennych z trzech głównych plików źródłowych danych:  
`nlfff_raw.csv`, `nlfff_flare_label.csv`, `flare_info.csv`.

Cechy zostały wybrane pod kątem:  
- fizycznej interpretowalności,  
- zgodności z literaturą naukową (SDO/HMI + SHARP),  
- braku ryzyka data leakage,  
- użyteczności w predykcji rozbłysków słonecznych.

---

## 1. Cechy fizyczne pola magnetycznego (**X**)  
**Plik:** `nlfff_raw.csv`  
**Rola:** cechy wejściowe modelu (features)

| Nazwa | Znaczenie |
|-------|-----------|
| **HARP_NUM** | Numer identyfikacyjny aktywnego regionu Słońca (AR) – używany wyłącznie do dopasowania rekordów, nie jako cecha w modelu. |
| **T_REC_DATETIME** | Czas wykonania obserwacji fizycznych parametrów (timestamp SDO/HMI) – używany do synchronizacji, nie jako cecha. |
| **USFLUX** | Całkowity bezwzględny strumień pola magnetycznego – określa skalę i siłę energetyczną aktywnego regionu. |
| **MEANGAM** | Średni kąt nachylenia wektora pola magnetycznego względem powierzchni Słońca. |
| **MEANGBT** | Średni gradient wielkości całkowitego pola magnetycznego – miara zmienności pola. |
| **MEANGBZ** | Średni gradient pionowej składowej pola magnetycznego Bz (w kierunku radialnym). |
| **MEANGBH** | Średni gradient poziomej składowej pola magnetycznego (wzdłuż powierzchni fotosfery). |
| **MEANJZD** | Średnia gęstość pionowego prądu elektrycznego – wskaźnik aktywności magnetohydrodynamicznej. |
| **TOTUSJZ** | Całkowity bezwzględny pionowy prąd w obrębie aktywnego regionu. |
| **MEANALP** | Parametr α opisujący stopień skręcenia (twist) pola magnetycznego – im wyższy, tym większa energia wolna. |
| **MEANJZH** | Średnia helicity prądowej – powiązana z niestabilnościami magnetycznymi. |
| **TOTUSJH** | Całkowita helicity prądowa – pokazuje akumulację energii magnetycznej w AR. |
| **ABSNJZH** | Znormalizowana helicity prądowa – wersja skalowalna i porównywalna między AR. |
| **SAVNCPP** | Suma przepływów prądów netto pomiędzy biegunami magnetycznymi – związana z niestabilnością pola. |
| **MEANPOT** | Średnia gęstość energii wolnej pola magnetycznego – energia możliwa do uwolnienia. |
| **TOTPOT** | Całkowita energia wolna pola magnetycznego – jeden z kluczowych predyktorów flar. |
| **MEANSHR** | Średni kąt ścinania pola magnetycznego – im większy, tym większa niestabilność geometryczna. |
| **SHRGT45** | Procent pikseli, w których kąt ścinania przekracza 45° – silny predyktor rozbłysków klasy M/X. |
| **R_VALUE** | Indeks aktywności linii neutralnych pola (wg Schrijvera) – wskaźnik zagrożenia dużymi flarami. |
| **GWILL** | Miara gradientu pola magnetycznego oparta na metodzie Willa – alternatywny wskaźnik niestabilności. |

---

## 2. Zmienne celu (klasyfikacja) (**y_class**)  
**Plik:** `nlfff_flare_label.csv`

| Nazwa | Znaczenie |
|-------|-----------|
| **harp_num** | Identyfikator AR do dopasowania rekordów – nie jest cechą modelową. |
| **t_rec_datetime** | Czas obserwacji – używany do synchronizacji, nie jako cecha modelowa. |
| **now_flare_level** | Aktualna klasa flary przypisana do czasu obserwacji. |
| **h6_flare_level** | Prognozowana klasa flary w horyzoncie 6 godzin. |
| **h12_flare_level** | Prognozowana klasa flary w horyzoncie 12 godzin. |
| **h24_flare_level** | Prognozowana klasa flary w horyzoncie 24 godzin – **główny target klasyfikacji**. |
| **h48_flare_level** | Prognozowana klasa flary w horyzoncie 48 godzin. |
| **h24_posmx** | Czy w ciągu 24 godzin wystąpi flara klasy M lub X (0/1). |
| **h24_poscmx** | Czy w ciągu 24 godzin wystąpi flara klasy C, M lub X (0/1). |
| **h48_posmx** | Jak wyżej, ale w horyzoncie 48 godzin (M/X). |
| **h48_poscmx** | Jak wyżej, ale w horyzoncie 48 godzin (C/M/X). |
| **h24_delta05** | Binary target: M/X w 24h, wg dodatkowego kryterium probabilistycznego. |
| **h48_delta05** | Binary target: M/X w 48h. |

---

## 3. Zmienne celu (regresja + walidacja) (**y_reg**)  
**Plik:** `flare_info.csv`

| Nazwa | Znaczenie |
|-------|-----------|
| **deeps_flare_id** | Id flary w bazie – używany do dopasowania, nie jako cecha modelowa. |
| **xray_intensity** | Wartość szczytowa emisji promieniowania X-ray (używana jako target regresji). |
| **xray_class** | Oficjalna klasa flary NOAA – używana do walidacji porównawczej. |
| **start_datetime** | Czas rozpoczęcia flary – do analizy i sanity-check, nie cecha. |
| **peak_datetime** | Czas maksimum flary – pomoc kontrolna, nie cecha. |
| **end_datetime** | Czas zakończenia flary – nie cecha, tylko do raportów. |
| **latitude** | Pozycja heliograficzna flary – opcjonalnie do analizy. |
| **longtitude** | Pozycja heliograficzna flary – opcjonalnie do analizy. |

---

## Podsumowanie logiki
- **Model używa tylko cech fizycznych** z `nlfff_raw.csv`  
- **Etykiety klasyfikacyjne i regresyjne pochodzą z dwóch niezależnych tabel**  
- **Dane czasowe i identyfikatory służą tylko do łączenia rekordów i kontroli jakości, nie trafiają do modelu**

```markdown
Model ML = f(USFLUX, MEANJZD, MEANSHR, ... ) → (h24_flare_level, log10(xray_intensity))
