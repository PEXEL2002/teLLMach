# teLLMach - Inteligentny Asystent Podróży i Bezpieczeństwa

**Telemach** to zaawansowany system wspomagania podróży, który łączy funkcje klasycznego planera turystycznego z dynamicznym systemem zarządzania kryzysowego. Podczas gdy inne aplikacje pokazują, gdzie zjeść obiad, Telemach dba o to, abyś miał jak wrócić do domu, gdy sytuacja na świecie ulegnie zmianie.

## 1. Opis działania i schemat logiczny

System działa jako *proaktywny agent AI*, który integruje dane z wielu zewnętrznych źródeł (API linii lotniczych, hoteli, map oraz serwisów rządowych/geopolitycznych).

### Logika działania:

1. *Profilowanie:* Użytkownik podaje preferencje, budżet i lokalizację startową.
    
2. *Planowanie:* System agreguje oferty i tworzy spersonalizowany plan podróży.
    
3. *Monitorowanie:* W tle agent śledzi statusy lotów oraz alerty bezpieczeństwa (np. dane z MSZ lub systemów monitorujących konflikty).
    
4. *Reakcja:* Jeśli poziom zagrożenia przekroczy zdefiniowany próg, system automatycznie przełącza się w "tryb ewakuacji", priorytetyzując bezpieczne korytarze lądowe lub alternatywne połączenia lotnicze z krajów sąsiednich.
    

---

## 2. Wymagania systemowe

### Wymagania Funkcjonalne 

- *Wyszukiwanie ofert:* Integracja z API (np. Skyscanner) w celu pobierania cen w czasie rzeczywistym.
    
- *Generator planu zwiedzania:* Proponowanie atrakcji na podstawie lokalizacji użytkownika.
    
- *Moduł kryzysowy:* Wykrywanie konfliktów zbrojnych w regionie na podstawie RSS/API wiadomości.
    
- *Wyznaczanie tras alternatywnych:* Obliczanie dróg powrotnych (np. pociągi, autobusy) w przypadku zamknięcia przestrzeni powietrznej.
    
- *Powiadomienia:*  Natychmiastowe alerty o zmianach w planie lub zagrożeniach.
    

### Wymagania Niefunkcjonalne (Jak system działa?)

- *Dostępność:* System działa 24/7 .
    
- *Wydajność:* Czas odpowiedzi na zapytanie o loty nie powinien przekraczać 30 sekund.
    
- *Skalowalność:* Obsługa wielu użytkowników jednocześnie bez spadku płynności.
    
- *Niezawodność danych:* Informacje o bezpieczeństwie muszą pochodzić z autoryzowanych źródeł (API rządowe).
    

---

## 3. Technologie i narzędzia

| *Warstwa*          | *Technologia*                                               |
| -------------------- | ------------------------------------------------------------- |
| *Backend*          | Python (FastAPI lub Django)                                   |
| *Frontend*         |                                                               |
| *Silnik AI*        | Gemini                                                        |
| *Integracje (API)* | skyscanner (loty), Booking.com (hotele), Google Maps (trasy). |
| *Konteneryzacja*   | Docker + Kubernetes (dla stabilności).                        |

---
## 4. Baza danych
Wektorowa baza danych (Qdrant), do semantycznego wyszukiwania polecanych atrakcji podczas wakacji.

---

## 5. Bezpieczeństwo


- *Szyfrowanie:* Wszystkie dane użytkowników (szczególnie paszporty/dowody) muszą być szyfrowane algorytmem *AES-256*.
    
- *Autoryzacja:* Standard **OAuth 2.0 
    
- *Offline Access:* Możliwość pobrania planu podróży i mapy ewakuacyjnej do pamięci urządzenia (tryb offline na wypadek braku internetu w strefie konfliktu).
    
- *Weryfikacja źródeł:* Mechanizm truth-checking dla newsów, aby uniknąć dezinformacji wywołującej panikę.
    

---
