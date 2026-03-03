# teLLMach - Inteligentny Asystent Podróży i Bezpieczeństwa

**Telemach** to zaawansowany system wspomagania podróży, który łączy funkcje klasycznego planera turystycznego z dynamicznym systemem zarządzania kryzysowego. Podczas gdy inne aplikacje pokazują, gdzie zjeść obiad, Telemach dba o to, abyś miał jak wrócić do domu, gdy sytuacja na świecie ulegnie zmianie.

---

## Kluczowe Funkcje

### 1. Planowanie i Logistyka
* **Optymalizacja Tras:** Wyznaczanie najszybszych i najbezpieczniejszych połączeń (lotniczych, kolejowych, drogowych).
* **Bilety i Atrakcje:** Integracja z systemami rezerwacyjnymi oraz personalizowane rekomendacje turystyczne.
* **Travel Concierge:** Sugerowanie kierunków podróży na podstawie Twoich preferencji i aktualnego poziomu bezpieczeństwa.

### 2. Paszport do Wiedzy (Compliance)
* **Wymagania Wizowe:** Automatyczne sprawdzanie niezbędnych dokumentów wjazdowych dla obywateli RP.
* **Baza Dokumentów:** Lista kontrolna wymaganych zaświadczeń, ubezpieczeń i certyfikatów medycznych.

### 3. Moduł Bezpieczeństwa (Live GOV Integration)
Projekt aktywnie monitoruje dane z serwisów **gov.pl** (w tym systemów MSZ takich jak *Odyseusz*), dostarczając:
* **Analiza Ryzyka:** Bieżące oceny bezpieczeństwa dla poszczególnych regionów świata.
* **Alerty Kryzysowe:** Powiadomienia o nagłych zdarzeniach (konflikty zbrojne, klęski żywiołowe, niepokoje społeczne).

### 4. Zarządzanie Sytuacjami Awaryjnymi (Crisis Management)
Unikalna funkcja Telemacha, która aktywuje się w sytuacjach "Planu B":
* **Dynamiczne Omijanie Stref:** Automatyczne przeliczanie tras w przypadku zamknięcia przestrzeni powietrznej lub granic lądowych.
* **Punkty Ewakuacyjne:** Wyznaczanie drogi do najbliższych placówek dyplomatycznych i punktów zbiórki.
* **Offline First:** Dostęp do kluczowych danych kontaktowych i map nawet przy ograniczonym dostępie do sieci.

---

## Architektura Danych

System opiera się na trzech filarach informacyjnych:
1.  **Gov.pl API:** Pobieranie oficjalnych komunikatów MSZ i ostrzeżeń dla podróżujących.
2.  **Real-time Flight/Traffic Data:** Monitoring opóźnień i blokad transportowych w czasie rzeczywistym.
3.  **Global Incident Feeds:** Śledzenie globalnych doniesień o zdarzeniach losowych i pogodowych.

---

## Dlaczego Telemach?

W mitologii Telemach musiał dorosnąć i stawić czoła wyzwaniom pod nieobecność ojca. Nasz projekt realizuje tę samą misję: daje podróżnikowi narzędzia do podejmowania dojrzałych, bezpiecznych decyzji w świecie, który bywa nieprzewidywalny.

> "Nie sztuką jest wyjechać. Sztuką jest wiedzieć, jak bezpiecznie wrócić."

---

## Instalacja i Konfiguracja (Przykład)

```bash
# Sklonuj repozytorium
git clone [https://github.com/twoj-login/telemach.git](https://github.com/twoj-login/telemach.git)

# Zainstaluj zależności
pip install -r requirements.txt

# Skonfiguruj klucze API (w tym dostęp do danych gov)
cp .env.example .env
