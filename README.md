# Car_Rent_Project
# 🚗 CAR RENTAL SERVICE

## Opis projektu
Car Rental Service to konsolowa aplikacja napisana w języku Python, służąca do zarządzania procesami w wypożyczalni samochodów. System działa w pełni w pamięci RAM (in-memory) i umożliwia kompleksową obsługę floty pojazdów, bazy klientów, procesu wypożyczeń i zwrotów, a także automatyczne naliczanie zniżek w ramach programu lojalnościowego.

## Struktura projektu
Zgodnie z systemem importów, projekt opiera się na następującej strukturze plików:

* main.py - główny punkt wejścia aplikacji zawierający interaktywne menu w terminalu.
* src/models.py - plik z definicjami modeli danych (`CarStatus`, Car, `Customer`).
* src/services.py - plik zawierający logikę biznesową i serwisy (`FleetManager`, CustomerRegistry, Invoice, Rental, RentalService, `LoyaltyProgram`).

## Funkcjonalności

System został podzielony na kilka niezależnych modułów (serwisów), które odpowiadają za poszczególne zadania:

### 1. Zarządzanie flotą (`FleetManager` i `Car`)
* Przechowywanie informacji o samochodach (marka, model, rocznik, stawka dzienna).
* Śledzenie statusu pojazdów (`available`, rented, `maintenance`).
* Możliwość dodawania i usuwania aut z floty.
* Wyszukiwanie aut dostępnych, w serwisie oraz filtrowanie po marce.

### 2. Baza klientów (`CustomerRegistry` i `Customer`)
* Rejestrowanie nowych klientów z przypisaniem ich danych (imię, nazwisko, email, telefon).
* Unikalny identyfikator klienta oparty na numerze prawa jazdy.
* Zabezpieczenie przed ponowną rejestracją klienta z tym samym numerem prawa jazdy.

### 3. Obsługa wypożyczeń (`RentalService`, Rental, `Invoice`)
* Wypożyczanie: Powiązanie dostępnego pojazdu z klientem na określoną liczbę dni, zmiana statusu auta na rented oraz zablokowanie go dla innych.
* Zwroty: Odblokowanie pojazdu (zmiana statusu na `available`), usunięcie transakcji z aktywnych wypożyczeń oraz wygenerowanie dokumentu finansowego (`Invoice`).
* Obliczanie całkowitego kosztu na podstawie stawki dziennej pojazdu oraz liczby dni.

### 4. Program lojalnościowy (`LoyaltyProgram`)
* Automatyczne śledzenie liczby pomyślnie zakończonych wypożyczeń każdego klienta.
* Naliczanie zniżek przy zwrocie pojazdu:
  * 3 do 4 wypożyczeń: 10% zniżki.
  * 5 i więcej wypożyczeń: 20% zniżki.

## Instrukcja uruchomienia

Ponieważ aplikacja wykorzystuje wyłącznie standardowe biblioteki języka Python (`sys`, `datetime`), nie wymaga instalacji żadnych zewnętrznych pakietów. 

1. Upewnij się, że masz zainstalowanego Pythona w wersji 3.10 lub nowszej (kod używa typowania, np. list[Car] oraz operatora | dla typów opcjonalnych).
2. Pobierz pliki projektu, zachowując powyższą strukturę katalogów (`main.py` w głównym folderze oraz models.py i services.py w folderze `src/`).
3. Otwórz terminal w głównym katalogu projektu i uruchom komendę:
   ```bash
   python main.py
   
## Instrukcja obsługi (Menu Główne)

Aplikacja po uruchomieniu automatycznie ładuje dane testowe (3 samochody: Toyota Corolla, BMW X5, Ford Focus oraz 1 klienta: Jana Kowalskiego).

Dostępne opcje w menu głównym:

[1] Pokaż dostępne samochody: Wyświetla listę pojazdów gotowych do wypożyczenia wraz z ich stawką dzienną.
[2] Zarejestruj nowego klienta: Przeprowadza przez proces dodawania nowej osoby do bazy (wymaga podania m.in. unikalnego numeru prawa jazdy).
[3] Wypożycz samochód: Wymaga podania numeru prawa jazdy zarejestrowanego klienta, wybrania auta z listy dostępnych i zadeklarowania liczby dni.
[4] Zwróć samochód: Pozwala wybrać aktywne wypożyczenie do zakończenia. System automatycznie odblokuje auto, wygeneruje fakturę, zastosuje zniżki lojalnościowe i zaktualizuje historię klienta.
[5] Wyjdź: Zamyka aplikację. Uwaga: ponieważ dane są przechowywane w pamięci operacyjnej, zamknięcie aplikacji skutkuje usunięciem historii wypożyczeń i nowo dodanych klientów.

## Skład grupy

* Nazar Humeniuk * GitHub profile - "nazikmazik007"
* Anastasiya Vasenda * GitHub profile - "anastiavasenda-cell"
* Aliaksandr Tsylindz * GitHub profile - "TwetnyFirst"
* Oleksandr Pysmennyi * GitHub profile - "OleksandrPysmennyi"

