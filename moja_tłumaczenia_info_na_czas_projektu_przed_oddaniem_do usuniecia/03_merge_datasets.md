# Co robią te cztery linie usuwające braki dat i sortujące dane?

```python
# Remove missing datetime entries
df_xy = df_xy.dropna(subset=["T_REC_DATETIME"])
df_info = df_info.dropna(subset=["peak_datetime"])

# Sorting is required for merge_asof
df_xy = df_xy.sort_values("T_REC_DATETIME")
df_info = df_info.sort_values("peak_datetime")
```

## 1. Usuwanie rekordów z brakującymi datami

Instrukcje `dropna(subset=...)` usuwają wszystkie wiersze, w których brakuje wartości w kluczowych kolumnach czasowych:

- **T_REC_DATETIME** — czas pomiaru parametrów magnetycznych SHARP (SDO/HMI),
- **peak_datetime** — czas maksimum flary GOES.

Wiersz bez jednej z tych dat jest bezużyteczny, ponieważ:

- nie można policzyć różnicy czasu `delta_hours`,
- nie można dopasować zdarzeń SHARP ↔ GOES (`merge_asof`),
- nie można ocenić poprawności czasowej (czy pomiar wystąpił przed flarą).

Dlatego takie rekordy są natychmiast usuwane z analizy.

---

## 2. Sortowanie danych przed `merge_asof`

`merge_asof` wymaga, aby dane były posortowane **rosnąco** po kolumnie czasu.  
Dlatego wykonujemy:

```python
df_xy = df_xy.sort_values("T_REC_DATETIME")
df_info = df_info.sort_values("peak_datetime")
```

Sortowanie jest absolutnie konieczne, ponieważ `merge_asof`:

- przeszukuje dane chronologicznie,
- znajduje najbliższe późniejsze zdarzenie (`direction="forward"`),
- nie działa poprawnie, jeśli dane nie są uporządkowane.

---

## **Podsumowanie**

- `dropna()` usuwa rekordy bez dat — bo nie nadają się do walidacji czasowej.  
- `sort_values()` przygotowuje dane do `merge_asof`.  
- Te cztery linie przygotowują zbiór do dopasowania SDO ↔ GOES oraz do obliczeń czasowych.


# Wyjaśnienie działania łączenia czasowego `merge_asof` z 2-godzinną tolerancją oraz zapisu wyniku

```python
# Perform tolerance-based merge (2-hour window)
df_final = pd.merge_asof(
    df_xy,
    df_info,
    left_on="T_REC_DATETIME",
    right_on="peak_datetime",
    direction="forward",
    tolerance=pd.Timedelta("2h")
)

print(f"[OK] Final merged dataset shape (X + y + GOES): {df_final.shape}")

# Calculate time-match percentage
match_rate = df_final["peak_datetime"].notna().mean() * 100
print(f"[INFO] GOES timestamp match rate: {match_rate:.2f}%")

# 4 SAVE TEMPORARY MERGED OUTPUT

OUT_PATH = INTERIM_DIR / "merged_xy_goes_test.csv"
df_final.to_csv(OUT_PATH, index=False)

print(f"\n[SAVED] Test merged dataset saved to:\n{OUT_PATH}")
print("[NOTE] This output is TEMPORARY — final dataset will be validated and cleaned later.")
```

## 1. Łączenie czasowe za pomocą `merge_asof`

`merge_asof` dopasowuje rekordy **na podstawie osi czasu**, a nie na podstawie identycznych timestampów.  
Podczas gdy zwykły `merge` działa tylko wtedy, gdy wartości klucza są identyczne,  
`merge_asof` znajduje **najbliższe późniejsze zdarzenie**.

Pozwala to połączyć:

- pomiar SHARP (SDO/HMI),  
- z odpowiadającą mu flarą GOES,  

nawet gdy timestampy nie są identyczne.

### Parametry:

- **left_on="T_REC_DATETIME"** — czas pomiaru SHARP  
- **right_on="peak_datetime"** — czas maksimum flary  
- **direction="forward"** — znajdź pierwsze zdarzenie *po* pomiarze  
- **tolerance="2h"** — łącz tylko wtedy, gdy flara wystąpiła w ciągu 2 godzin

To odzwierciedla fizyczny porządek zdarzeń:  
**najpierw zmiana pola magnetycznego → potem flara.**

---

## 2. Obliczanie procentu dopasowanych rekordów

```python
match_rate = df_final["peak_datetime"].notna().mean() * 100
```

Ten wskaźnik pokazuje, jaka część pomiarów SHARP miała dopasowaną flarę GOES.  
`NaT` oznacza, że w ciągu 2 godzin od pomiaru nie wystąpiła żadna flara.

---

## 3. Zapis wyniku tymczasowego

```python
df_final.to_csv(OUT_PATH, index=False)
```

Tworzony jest plik:

**`merged_xy_goes_test.csv`**

To **tymczasowy** wynik, którego używamy do:

- sprawdzenia poprawności merge,  
- oceny jakości dopasowań,  
- przygotowania do walidacji czasowej.

Ostateczny dataset powstanie dopiero później.

---

## **Podsumowanie**

- `merge_asof` dopasowuje rekordy na podstawie czasu, nie identycznych kluczy.  
- `direction="forward"` wymusza poprawną chronologię: pomiar → flara.  
- `tolerance="2h"` zapobiega łączeniu z przypadkowymi, odległymi zdarzeniami.  
- Wynik to testowy merge SHARP ↔ GOES, używany przed walidacją czasową.

