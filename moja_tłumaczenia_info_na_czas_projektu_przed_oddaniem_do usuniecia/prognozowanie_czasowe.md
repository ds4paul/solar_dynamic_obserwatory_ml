# Dlaczego w prognozowaniu czasowym konieczna jest walidacja temporalna?

W klasycznych problemach Machine Learning często zakłada się, że jeżeli poprawnie wybierzemy cechy wejściowe (features) oraz wykonamy prawidłowy podział danych na train/test, to ryzyko *data leakage* praktycznie znika. Jednak w zadaniach, w których kluczowym elementem jest **czas wystąpienia zdarzenia**, takie założenie nie jest wystarczające. Modele predykcyjne oparte na danych szeregów czasowych (time-based forecasting) mogą nieświadomie wykorzystać informacje pochodzące z przyszłości, nawet jeśli programista nie widzi w kodzie żadnych jawnych przyszłych wartości.

---

## Na czym polega problem?

W naszych danych każdy rekord reprezentuje pojedynczy pomiar fizycznych parametrów aktywnego regionu Słońca (SDO/HMI). Jednakże sam fakt, że rekord istnieje w tabeli, **nie gwarantuje**, że został wykonany **przed** rozbłyskiem, który próbujemy przewidzieć. Może się zdarzyć, że niektóre rekordy zawierają pomiary wykonane **po fakcie**, czyli po wystąpieniu rozbłysku związanego z tą samą aktywną strukturą. W efekcie model ma dostęp do informacji, które w praktyce operacyjnej nigdy nie byłyby dostępne w momencie podjęcia decyzji prognozowej.

---

## Przykład intuicyjny

Załóżmy, że flara klasy M rozpoczęła się o **12:00 UTC**.  
W zbiorze danych mogą istnieć dwie obserwacje dotyczące tego samego regionu AR:

| Czas pomiaru SDO | Kontekst | Poprawność dla modelowania |
|------------------|----------|-----------------------------|
| 11:48 UTC        | pomiar przed flarą | ✔ poprawny |
| 12:15 UTC        | pomiar po flarze | ✖ niedozwolony |

Oba rekordy mają takie same kolumny wejściowe i wyglądają prawidłowo z punktu widzenia struktury danych, ale ich **znaczenie czasowe jest zupełnie inne**. Tylko pierwszy z nich mógłby być realistycznie użyty do prognozy.

---

## Dlaczego zwykły train/test split nie wystarcza?

Standardowy podział danych (train/test split) nie bierze pod uwagę czasu powstania rekordów. 
Może więc wystąpić sytuacja, w której dane treningowe zawierają obserwacje **po** flarze, 
natomiast dane testowe zawierają obserwacje **sprzed** flary. W takiej konfiguracji model 
uczy się i generalizuje na podstawie informacji, które w rzeczywistości były dostępne dopiero 
po wystąpieniu zdarzenia, co oznacza, że operuje wiedzą z przyszłości. Skutkuje to sztucznie 
zawyżonymi wynikami metryk jakości (np. accuracy, recall, F1, ROC-AUC), które nie odzwierciedlają 
realnej skuteczności modelu w systemie operacyjnym lub środowisku badawczym. W praktyce rzeczywisty 
wynik byłby znacznie gorszy.

| Problem | Efekt |
|---------|--------|
| Nieświadome uczenie się na danych z przyszłości | Fałszywie wysokie metryki |
| Zniekształcenie interpretacji cech (SHAP, feature importance) | Błędne wnioski fizyczne |
| Brak możliwości przeniesienia rozwiązania do praktyki | Model nie działa na prawdziwych danych |
| Ryzyko niewłaściwych publikacji | Replikowalność = 0 |

**Wniosek końcowy:** walidacja temporalna nie jest dodatkiem ani opcją, lecz absolutnym wymogiem w projektach predykcyjnych opartych na czasie. W naszym pipeline etap `04_temporal_validation.py` odpowiada za oznaczanie lub odfiltrowywanie rekordów, tak aby do trenowania modeli trafiały wyłącznie dane, które faktycznie mogły istnieć przed wystąpieniem rozbłysku i mogły być dostępne dla analityka, systemu satelitarnego lub modelu predykcyjnego.


