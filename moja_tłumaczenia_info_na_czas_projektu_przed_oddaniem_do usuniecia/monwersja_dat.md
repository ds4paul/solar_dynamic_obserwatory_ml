# Co robią te dwie linie konwersji dat?

```python
df_xy["T_REC_DATETIME"] = pd.to_datetime(df_xy["T_REC_DATETIME"])
df_info["peak_datetime"] = pd.to_datetime(df_info["peak_datetime"], errors="coerce")
```

## 1. Zamiana tekstu na obiekty `datetime64`

Po wczytaniu pliku CSV daty są zwykłymi stringami.  
Funkcja `pd.to_datetime()` zamienia je na prawdziwe obiekty typu `datetime64`,  
co pozwala wykonywać operacje czasowe takie jak:

- obliczanie różnic czasowych (np. godzin),
- sortowanie po czasie,
- filtrowanie zakresów czasowych,
- łączenie rekordów po czasie (`merge_asof`).

Bez konwersji te operacje byłyby niemożliwe.

---

## 2. Konwersja `T_REC_DATETIME`

Kolumna `T_REC_DATETIME` pochodzi z danych NASA SDO/HMI i ma **stały, poprawny format**.  
Dlatego wystarcza zwykła konwersja:

```python
pd.to_datetime(df_xy["T_REC_DATETIME"])
```

Nie potrzebujemy dodatkowych zabezpieczeń.

---

## 3. Konwersja `peak_datetime` z `errors="coerce"`

Dane `peak_datetime` z GOES mogą mieć:

- puste pola,
- błędne wartości,
- niejednolity format daty.

Dlatego stosujemy:

```python
errors="coerce"
```

Co to oznacza?

- poprawne daty → zostaną skonwertowane,
- błędne daty → zostaną zamienione na `NaT` (Not a Time).

Dzięki temu skrypt działa stabilnie, a błędne daty są oznaczone jako brakujące.

---

## 4. Dlaczego konwersja jest konieczna?

Po konwersji możemy:

- obliczyć `delta_hours`,
- sortować wiersze po czasie,
- filtrować obserwacje według daty,
- poprawnie wykonać `merge_asof`.

To absolutnie kluczowy krok przed walidacją czasową.

---

## **Podsumowanie**

- `pd.to_datetime()` zamienia tekst na prawdziwe daty.  
- `T_REC_DATETIME` konwertujemy normalnie (dane są czyste).  
- `peak_datetime` konwertujemy z `errors="coerce"` (dane GOES mogą mieć błędy).  
- Dzięki temu operacje czasowe działają poprawnie w dalszym pipeline.
