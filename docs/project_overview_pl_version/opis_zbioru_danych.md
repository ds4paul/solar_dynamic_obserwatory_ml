# Data Description (NLFFF Dataset – Solar Active Regions + Flare Labels)

## Oficjalne źródła danych
https://nlfff.dataset.deepsolar.space/en/download/  
https://sdo.gsfc.nasa.gov  
https://www.swpc.noaa.gov/products/goes-x-ray-flux  


---

## 0. Zbiór pobrany ze strony

Źródło:  
https://nlfff.dataset.deepsolar.space/en/download/#3-database-archive-files  

Plik źródłowy: **NLFFF Dataset and Flare Label Database Archive**


---

## 1. Dane eksportowane z SQL do CSV

Dane robocze zapisane w formacie `.csv` dostępne są pod adresem:  
https://drive.google.com/drive/folders/1JJhNI2VePSgYyD1sM7Lv63ajUMJ-iElY?usp=sharing

 - `flare_info.csv` https://drive.google.com/file/d/1LU4Js4fyA0Hl1fmAKjH7rSDzpfxD90r1/view?usp=share_link
 - `nlfff_archive.csv` https://drive.google.com/file/d/1Y8oVZ9SM0S6JAKCBOsmFRjlJAN3F8yvg/view?usp=share_link
 - `nlfff_flare_label.csv` https://drive.google.com/file/d/1MRRVrNkP0UIONW9aGk1LUoeN2OcxlCKG/view?usp=share_link
 - `nlfff_raw.csv` https://drive.google.com/file/d/19uYRjL3k-hy6aIV4g4QsHVcwyvcDyx0-/view?usp=share_link

---

## 2. Dataset — informacje i struktura

### 2.1 Zawartość poszczególnych plików

#### 1.1 flare_info.csv
Zawiera informacje o rozbłyskach słonecznych według obserwacji satelitów **NOAA/GOES**.  
Jest to zbiór opisujący **skutek** (wynik obserwacyjny).  
Dane zawierają m.in.:  
- klasy flar: **A, B, C, M, X**,  
- czas rozpoczęcia,  
- czas maksimum,  
- czas zakończenia,  
- wartość szczytowego natężenia promieniowania rentgenowskiego (**peak flux**).  

Plik **pozostaje** w projekcie, ale jest wykorzystywany **wyłącznie** do:  
- walidacji,  
- interpretacji jakościowej,  
- sanity-check,  
- *nie* jako wejście do modelu ML.


#### 1.2 nlfff_flare_label.csv
Zawiera etykiety flar powiązane czasowo z obserwacjami **HARP/SHARP** z NASA SDO  
dla różnych horyzontów prognozy, np.:  
`now_flare_level, h6_flare_level, h12_flare_level, h24_flare_level, h48_flare_level`.

Oznaczenia oparte są na:  
- sile rozbłysku,  
- czasie jego wystąpienia.

Plik pozostaje w projekcie i stanowi **podstawę do tworzenia zmiennej celu (target y).**


#### 1.3 nlfff_raw.csv
Zawiera rzeczywiste **fizyczne parametry magnetyczne aktywnych regionów Słońca** (*SHARP features*)  
pochodzące z instrumentu **HMI** satelity **SDO**.

Jest to **główne źródło cech wejściowych (features X)**.

Plik pozostaje w projekcie **po selekcji zmiennych**, pozostają tylko cechy fizyczne istotne  
dla modelowania, natomiast wszystkie pola:  
- techniczne,  
- opisowe,  
- plikowe,  
- geometryczne,  
- jakościowe  
są **usuwane**.


#### 1.4 nlfff_archive.csv
Zawiera dane archiwalne, metadane, pola pośrednie oraz dane duplikujące zawartość `nlfff_raw.csv`.  
Ten plik **jest usuwany** z projektu i nie powinien być używany na żadnym etapie modelowania ML,  
ponieważ może prowadzić do:  
- **data leakage**,  
- **błędnych korelacji**.


---

## 3. Co usuwamy i dlaczego

Usuwamy wszystkie pola o charakterze:  
- technicznym,  
- plikowym,  
- geometrycznym,  
- statystycznym,  
- jakościowym,  
- metadokumentacyjnym,  

ponieważ **nie mają fizycznego znaczenia w predykcji flar**.

Odrzucamy m.in.:  
`FILE_NAME, CONTENT, ORIGIN, CTYPE*, CRPIX*, CRVAL*, CDELT*, CROTA2, QUALITY, QUAL_S, QUALLEV*, ścieżki do FITS, BUNIT*, DATA*, MISSVAL*, DATAMIN*, DATAMAX*, DATAMEAN*, DATARMS*, komentarze, pola wersji pipeline, pola dokumentacyjne.`

Pola czasowe, np. `T_REC`, oraz identyfikator aktywnego regionu `HARP_NUM`,  
pozostawiamy **wyłącznie w celu łączenia tabel**,  
jednak **nie są** one cechami modelowymi (features).


---

## 4. Zestaw plików i ich ostateczna rola

| Plik | Rola w projekcie |
|------|------------------|
| **nlfff_raw.csv** | Główne cechy wejściowe (features X) |
| **nlfff_flare_label.csv** | Zmienne celu (targets y) |
| **flare_info.csv** | Walidacja i analiza pomocnicza (nie features) |
| **nlfff_archive.csv** | Usuwamy / archiwizujemy (ryzyko leakage) |


---

## 5. Zasady łączenia tabel

- Łączenie wykonujemy poprzez **klucz złożony**:  
  **`HARP_NUM` + `T_REC`**
- Dane wejściowe (X) muszą pochodzić **z czasu wcześniejszego niż target (y)**.
- Niedopuszczalne jest użycie zmiennych **pochodzących po wystąpieniu flary**  
  jako cech wejściowych (ryzyko **data leakage**).


---

## 6. Finalny logiczny pipeline danych

- `nlfff_raw.csv` → selekcja fizycznych cech → preprocessing & scaling  
- `nlfff_flare_label.csv` → wybór targetu + opcjonalny encoding  
- opcjonalnie `flare_info.csv` → walidacja i analiza wyników  
- `X + y` → modele ML (klasyfikacja, regresja, ordinal classification, multi-horizon forecasting)

---

## 7. Full Variable Meaning Reference (Data Dictionary)

### 7.1 Zmienne kluczowe (nie są cechami modelowymi)

- **HARP_NUM** – numeryczny identyfikator aktywnego regionu Słońca (SHARP/HARP)  
- **T_REC** – timestamp obserwacji w formacie TAI (czas rekordu)


### 7.2 Fizyczne parametry magnetyczne używane jako cechy wejściowe (features X)

`USFLUX` – całkowity bezwzględny strumień magnetyczny  
`MEANGAM` – średni kąt nachylenia pola magnetycznego  
`MEANGBT` – średni gradient modułu całkowitego pola magnetycznego  
`MEANGBZ` – średni pionowy gradient składowej pola magnetycznego Bz  
`MEANGBH` – średni gradient poziomej składowej pola magnetycznego  
`MEANJZD` – średnia gęstość pionowego prądu elektrycznego  
`TOTUSJZ` – całkowity bezwzględny pionowy prąd elektryczny  
`MEANALP` – średnia wartość parametru alfa (twist)  
`MEANJZH` – średnia helicity prądowej  
`TOTUSJH` – całkowita helicity prądowa (unsigned)  
`ABSNJZH` – znormalizowana helicity prądowa  
`SAVNCPP` – suma bezwzględnych wartości prądów netto  
`MEANPOT` – średnia gęstość wolnej energii pola magnetycznego  
`TOTPOT` – całkowita wolna energia pola magnetycznego  
`MEANSHR` – średni kąt ścinania pola  
`SHRGT45` – odsetek pikseli o kącie ścinania > 45°  
`R_VALUE` – wskaźnik Schrijvera linii neutralnej pola (PIL)  
`GWILL` – alternatywny wskaźnik gradientowy pola magnetycznego  


### 7.3 Zmienne etykiet w nlfff_flare_label.csv (targets y)

- `now_flare_level`
- `h6_flare_level`
- `h12_flare_level`
- `h24_flare_level`
- `h48_flare_level`

Interpretacja klas:  
`0 = brak flary`  
`1 = B`  
`2 = C`  
`3 = M`  
`4 = X`  


### 7.4 Zmienne pomocnicze w flare_info.csv (walidacja, nie features)

`start_time` – czas rozpoczęcia flary  
`peak_time` – czas szczytowy  
`end_time` – czas zakończenia  
`peak_flux` – wartość szczytowa X-ray  
`class` – oficjalna klasa flary (A, B, C, M, X)  
`noaa_region` – identyfikator regionu NOAA powiązanego z flarą  


---

## 8. Ostateczna decyzja dotycząca cech modelowych

Zachowujemy wyłącznie fizyczne cechy magnetyczne z `nlfff_raw.csv` jako wejście (X)  
oraz etykiety z `nlfff_flare_label.csv` jako wyjście (y).  

Dane czasowe oraz klucz identyfikacyjny pełnią funkcję **łączącą**,  
natomiast wszystkie cechy:  
- techniczne,  
- obrazowe,  
- opisowe,  
- geometryczne,  
- metadane,  
- cały plik `nlfff_archive.csv`  

są usuwane ze względu na **brak wartości predykcyjnej** oraz **ryzyko data leakage**.
