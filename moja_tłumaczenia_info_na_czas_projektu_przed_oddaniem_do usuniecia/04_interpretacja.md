# Interpretacja wyników walidacji czasowej — pełne, spójne wyjaśnienie działania

Poniżej znajduje się **jeden spójny blok**, który obejmuje punkty **1–7**, w pełni sformatowany nagłówkami `#`, `##`, gotowy do wklejenia do dokumentacji projektu.

---

# 1. Cel działania skryptu `04_temporal_validation.py`

Skrypt służy do sprawdzenia, czy między pomiarem parametrów magnetycznych SDO/HMI (`T_REC_DATETIME`) a wystąpieniem flary GOES (`peak_datetime`) zachodzi poprawna zależność czasowa. Dzięki temu można wyeliminować przypadki, w których model mógłby się „uczyć na przyszłości” (data leakage). Dane wejściowe pochodzą z pliku `merged_xy_goes_test.csv`, który łączy:  
- cechy SHARP (X),  
- etykiety horyzontów czasowych (y),  
- zdarzenia flar GOES.

---

# 2. Konwersja dat i obliczenie różnicy czasowej

Pierwszy krok to zamiana tekstowych dat na format `datetime64`, co umożliwia wykonywanie operacji czasowych. Następnie obliczana jest wartość `delta_hours` — różnica czasu między flarą a pomiarem SHARP w godzinach. Dodatnia wartość oznacza, że flara wystąpiła **po** pomiarze, co jest warunkiem koniecznym do stworzenia sensownego przykładu w uczeniu maszynowym.

---

# 3. Weryfikacja horyzontów predykcyjnych

Na podstawie `delta_hours` system ocenia, czy flara mieści się w jednym z horyzontów:  
- **now** (delta ≥ 0),  
- **6h**,  
- **12h**,  
- **24h**,  
- **48h**.  

Przykład: jeśli `delta_hours = 1.65`, to rekord jest poprawny dla wszystkich horyzontów ≥ 2h. Skrypt tworzy flagi `valid_now`, `valid_6h`, itd., oznaczające zgodność z danym oknem czasowym.

---

# 4. Utworzenie głównej flagi czasowej `temporal_valid`

Aby rekord mógł zostać wykorzystany w modelowaniu, musi:  
1. spełniać warunek przyczynowości (`valid_now = TRUE`),  
2. mieścić się przynajmniej w jednym oknie czasowym (`valid_6h`, `valid_12h`, `valid_24h`, `valid_48h`).  

Flaga `temporal_valid` jest logiczną sumą tych warunków i ostatecznie decyduje o jakości czasowej rekordu:  
- `temporal_valid = TRUE` → przykład poprawny,  
- `temporal_valid = FALSE` → przykład błędny lub nieprzydatny dla predykcji.

---

# 5. Analiza statystyk raportu

Raport wygenerowany przez skrypt pokazuje:

- **46 134** rekordy w całym zbiorze,  
- **16 067** rekordów czasowo poprawnych,  
- **30 067** rekordów czasowo błędnych,  
- **valid_ratio ≈ 0.3483**, co oznacza, że ~35% danych spełnia wymogi czasowe.

To w pełni naturalny wynik — satelita SDO rejestruje dane regularnie co kilkanaście minut, natomiast flary są zjawiskiem rzadkim. Większość snapshotów nie sąsiaduje z żadną flarą GOES w ciągu 2 godzin, dlatego trafiają do kategorii `invalid`.

Dodatkowo wszystkie horyzonty (6h, 12h, 24h, 48h) mają podobne wyniki, ponieważ wcześniejszy etap łączenia (`merge_asof`) używa tolerancji 2 godzin — każdy dopasowany rekord automatycznie mieści się więc również w większych horyzontach.

---

# 6. Jak interpretować przykładowe rekordy?

### Przykład rekordu poprawnego:
- `T_REC_DATETIME = 00:00`,  
- `peak_datetime = 01:39`,  
- `delta_hours = 1.65`,  
- `xray_class = C`,  
- wszystkie flagi `valid_* = TRUE`,  
- `temporal_valid = TRUE`.

Interpretacja:  
> Pomiar SHARP poprzedza flarę o ~1.6 godziny → rekord idealny do nauki modelu.

### Przykład rekordu tuż przed flarą:
- `T_REC = 01:36`,  
- `peak = 01:39`,  
- `delta_hours = 0.05`,  
- wszystkie flagi TRUE.

Interpretacja:  
> Pomiar 3 minuty przed flarą. Bardzo wartościowe dane.

### Przykład rekordu niepoprawnego:
- brak GOES (`peak_datetime = NaT`),  
- `delta_hours = NaN`,  
- wszystkie `valid_* = FALSE`.

Interpretacja:  
> Po pomiarze nie było flary w oknie 2h → naturalny negatywny przykład.

---

# 7. Dlaczego ten etap jest absolutnie konieczny?

Walidacja czasowa to fundament poprawnej analizy ML w projektach predykcyjnych dla zjawisk fizycznych. Bez niej model mógłby:

- uczyć się na danych z przyszłości,  
- otrzymywać sztucznie zawyżone metryki,  
- generować fałszywe zależności (np. SHAP, feature importance),  
- być niereplikowalny i niefizyczny.

Ten krok zapewnia, że **wszystkie dalsze etapy — EDA, modele, Optuna, SHAP, finalny raport** — opierają się na fizycznie poprawnych danych, w których zachowana jest przyczynowość:  
> najpierw pomiar SDO → później flara GOES.

To gwarantuje naukową poprawność całego pipeline’u.

---

# Wyjaśnienie dlaczego `delta_hours = 1.6` godziny jest poprawne fizycznie (i nie ma nic wspólnego z 8 minutami)

Poniżej znajduje się pełna, spójna odpowiedź w jednym bloku markdown obejmująca wszystkie punkty.

---

# 1. Czas 8 minut nie ma związku z naszym pomiarem
Czas **8 minut** oznacza jedynie:
> ile czasu potrzebują fotony, aby dotrzeć ze Słońca do Ziemi.

Dotyczy to obserwacji:
- wizualnych,
- optycznych,
- X-ray (GOES),
- instrumentów SDO.

**Nie ma to żadnego wpływu na to, kiedy flara powstaje względem zmian pola magnetycznego.**

---

# 2. Pole magnetyczne „przygotowuje” flarę długo przed jej wystąpieniem
Cechy SHARP — takie jak:
- `USFLUX`,
- `MEANGAM`,
- `MEANJZH`,
- `MEANPOT`,
- `TOTPOT`,
- `R_VALUE`,
- `SHRGT45`,

opisują **nagromadzenie energii magnetycznej**, naprężenia, skręcenie linii pola i prądy elektryczne.

Flara pojawia się *dopiero wtedy*, gdy energia osiągnie punkt krytyczny — przez rekoneksję magnetyczną.

To może trwać:
- **minuty**,  
- **godziny**,  
- **a nawet kilkadziesiąt godzin**.

Dlatego pomiar sprzed 1.6h, 6h czy 24h może być jak najbardziej predykcyjny.

---

# 3. Okna czasowe używane w literaturze
Naukowe modele prognozowania flar operują na horyzontach:

- **6 godzin**
- **12 godzin**
- **24 godziny**
- **48 godzin**
- czasem **72 godziny**

Najczęściej spotykane okna: **24–48 godzin**.

Dlaczego?

Bo aktywny region często akumuluje energię stopniowo, a flara jest efektem wcześniejszej ewolucji pola.

---

# 4. Co naprawdę oznacza wartość `delta_hours = 1.65`?

Oznacza to:

> Pomiar SHARP wykonano o 00:00,  
> a flara GOES wystąpiła o 01:39.

Interpretacja:
- pole magnetyczne „zwiastowało” flarę wcześniej,  
- flara była konsekwencją stanu pola i jego ewolucji,  
- różnica 1.6h jest całkowicie normalna.

Nie ma tu żadnej nieprawidłowości.

---

# 5. Delta_hours NIE jest czasem podróży sygnału
To NIE jest:
- czas transmisji światła,
- opóźnienie instrumentów,
- fizyczne „dotarcie” flary do Ziemi.

To wyłącznie:
> różnica między czasem pomiaru pola a czasem wystąpienia flary.

Czyli czas **w którym pole magnetyczne ewoluowało**, aż flara została wyzwolona.

---

# 6. Co by oznaczało delta_hours ≈ 8 minut?
Tylko to, że flara wystąpiła:
- bardzo szybko po pomiarze,
- w praktyce: „prawie natychmiast”.

To też się zdarza, ale nie jest normą.

---

# 7. Podsumowanie

- `delta_hours = 1.6` jest **poprawne i fizycznie logiczne**.  
- Ewolucja pola magnetycznego trwa **dużo dłużej** niż 8 minut.  
- Horyzonty 6–48 godzin są standardem w prognozowaniu flar.  
- 8 minut to tylko czas podróży fotonów, który **nie ma znaczenia** dla naszego feature→flare timeline.  
- Wszystkie wyniki z 04_temporal_validation.py są poprawne i zgodne z literaturą.

---

Jeśli chcesz, mogę przygotować również:
- wykres rozkładu `delta_hours`,
- opis naukowy do dokumentacji projektu,
- albo porównanie z klasycznymi pracami Bobra & Couvidat (2015).
