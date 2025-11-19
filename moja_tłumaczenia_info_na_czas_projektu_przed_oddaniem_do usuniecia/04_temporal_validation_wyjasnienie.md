# Wyjaśnienie działania skryptu `04_temporal_validation.py`

```python
import pandas as pd
from pathlib import Path
from src.config import INTERIM_DIR, PROCESSED_DIR

# === 1. Paths ===
INPUT_FILE = INTERIM_DIR / "merged_xy_goes_test.csv"
OUTPUT_FILE = PROCESSED_DIR / "merged_xy_temporally_valid.csv"
REPORT_FILE = PROCESSED_DIR / "temporal_validation_report.md"
```

Skrypt zaczyna od zdefiniowania ścieżek do plików:  
- wejściowy → tymczasowy merge SHARP + labels + GOES,  
- wyjściowy → dataset po walidacji czasowej,  
- raport → plik markdown z podsumowaniem.

---

```python
# === 2. Load data ===
print("[INFO] Loading merged dataset...")
df = pd.read_csv(INPUT_FILE)

print("[INFO] Converting datetimes...")
df["T_REC_DATETIME"] = pd.to_datetime(df["T_REC_DATETIME"], utc=True, errors="coerce")
df["peak_datetime"] = pd.to_datetime(df["peak_datetime"], utc=True, errors="coerce")
```

Wczytujemy scalone dane i konwertujemy timestampy na obiekty `datetime64`.  
`errors="coerce"` zamienia błędne daty na `NaT`, co zapobiega awariom.

---

```python
# === 3. Compute time difference ===
print("[INFO] Computing delta_hours...")
df["delta_hours"] = (df["peak_datetime"] - df["T_REC_DATETIME"]) \
                        .dt.total_seconds() / 3600.0
```

Obliczamy różnicę czasu pomiędzy:

- **czasem wystąpienia flary GOES**,  
- **czasem pomiaru SHARP**,

w godzinach.  
`delta_hours` to kluczowa zmienna opisująca opóźnienie pomiędzy pomiarem a flarą.

---

```python
# === 4. Horizon validation logic ===
def valid_window(delta, hours):
    return (delta > 0) & (delta <= hours)

print("[INFO] Checking horizon correctness...")

df["valid_now"]  = df["delta_hours"] >= 0
df["valid_6h"]   = valid_window(df["delta_hours"], 6)
df["valid_12h"]  = valid_window(df["delta_hours"], 12)
df["valid_24h"]  = valid_window(df["delta_hours"], 24)
df["valid_48h"]  = valid_window(df["delta_hours"], 48)
```

Każdy rekord sprawdzamy pod kątem tego, czy flara mieści się w horyzoncie przewidywania:

- `valid_now` → dowolna flara po czasie pomiaru,  
- `valid_6h` → flara ≤ 6h po pomiarze,  
- `valid_12h` → flara ≤ 12h,  
- `valid_24h` → flara ≤ 24h,  
- `valid_48h` → flara ≤ 48h.

Pomiar jest **poprawny**, jeżeli znalazła się flara po czasie pomiaru (valid_now) **i** mieści się w którymkolwiek horyzoncie.

---

```python
# === 5. Final temporal validity flag ===
df["temporal_valid"] = (
    df["valid_now"] &
    (
        df["valid_6h"] |
        df["valid_12h"] |
        df["valid_24h"] |
        df["valid_48h"]
    )
)
```

Tworzymy jeden główny wskaźnik jakości czasowej:

- TRUE → rekord czasowo poprawny  
- FALSE → rekord błędny (flara wystąpiła zbyt późno lub przed pomiarem)

---

```python
# === 6. Stats ===
summary = {
    "total_rows": len(df),
    "valid_rows": int(df["temporal_valid"].sum()),
    "invalid_rows": int((~df["temporal_valid"]).sum()),
    "valid_ratio": round(df["temporal_valid"].mean(), 4),
}
```

Tworzymy podsumowanie:

- liczba wierszy,  
- ile przechodzi walidację,  
- ile odpada,  
- stosunek poprawnych do wszystkich.

Dodatkowo generujemy tabelę skuteczności dla każdego horyzontu:

```python
horizon_stats = pd.DataFrame({
    "valid_ratio": [
        df["valid_now"].mean(),
        df["valid_6h"].mean(),
        df["valid_12h"].mean(),
        df["valid_24h"].mean(),
        df["valid_48h"].mean(),
    ]
}, index=["now", "6h", "12h", "24h", "48h"]).round(4)
```

---

```python
# === 7. Save output ===
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)
print(f"[SAVED] Temporally validated dataset saved to: {OUTPUT_FILE}")
```

Zapisujemy dataset z oznaczeniami czasowymi jako:

**`merged_xy_temporally_valid.csv`**

To jest wejście do kolejnych kroków:

- handling missing values,  
- outlier detection,  
- feature engineering,  
- modelowania.

---

```python
# === 8. Save report ===
with open(REPORT_FILE, "w") as f:
    f.write("# Temporal Validation Report\n\n")
    f.write("## Summary\n")
    for k, v in summary.items():
        f.write(f"- **{k}**: {v}\n")

    f.write("\n## Horizon Validity\n")
    f.write(horizon_stats.to_string())
    f.write("\n\n---\nGenerated automatically by 04_temporal_validation.py\n")
```

Skrypt generuje raport **Markdown** z wynikami walidacji:

- sekcja Summary  
- sekcja dla horyzontów czasowych  
- tabela wyników  

Raport pozwala łatwo przejrzeć efekty walidacji i włączyć go do dokumentacji projektu.

---

```python
# === 9. Done ===
print("[DONE] Temporal validation complete.\n")
print(summary)
print("\nHorizon stats:\n", horizon_stats)
```

Na koniec wypisywane są podsumowania do konsoli.

---

# Podsumowanie działania skryptu

Skrypt:

1. Wczytuje połączone dane SHARP + GOES  
2. Konwertuje daty  
3. Oblicza opóźnienie czasowe `delta_hours`  
4. Waliduje każdy horyzont (0h–48h)  
5. Tworzy flagę `temporal_valid`  
6. Oblicza statystyki  
7. Zapisuje dataset i raport  
8. Kończy pełną walidację temporalną  

To fundament pipeline’u — usuwa wszystkie przypadki czasowo błędne,  
zapobiegając **data leakage z przyszłości**.
