from src.models import Car, Customer, CarStatus

class FleetManager:
    """
    Klasa odpowiedzialna za zarządzanie listą samochodów w wypożyczalni.
    Umożliwia dodawanie, usuwanie oraz zaawansowane filtrowanie aut.
    """
    def __init__(self):
        self.cars = []

    def add_car(self, car: Car):
        """Dodaje nowy samochód do floty."""
        if not isinstance(car, Car):
            raise TypeError("Można dodać tylko obiekt klasy Car")
        self.cars.append(car)

    def remove_car(self, car: Car):
        """Usuwa samochód z floty. Jeśli samochód nie istnieje, zgłasza ValueError."""
        if car in self.cars:
            self.cars.remove(car)
        else:
            raise ValueError("Podany samochód nie znajduje się we flocie")

    def get_available_cars(self):
        """Zwraca listę samochodów, które są aktualnie dostępne do wypożyczenia."""
        return [car for car in self.cars if car.status == CarStatus.AVAILABLE]

    def search_by_brand(self, brand: str):
        """Wyszukuje samochody według marki (wielkość liter nie ma znaczenia)."""
        return [car for car in self.cars if car.brand.strip().lower() == brand.strip().lower()]

    def get_cars_in_maintenance(self):
        """Zwraca listę samochodów przebywających aktualnie w serwisie/naprawie."""
        return [car for car in self.cars if car.status == CarStatus.MAINTENANCE]


class CustomerRegistry:
    """
    Klasa odpowiedzialna za zarządzanie bazą klientów wypożyczalni.
    """
    def __init__(self):
        self.customers = {}  # Przechowywanie w słowniku {numer_prawa_jazdy: obiekt_Customer}

    def register_customer(self, customer: Customer):
        """Rejestruje nowego klienta w bazie danych."""
        if not isinstance(customer, Customer):
            raise TypeError("Można zarejestrować tylko obiekt klasy Customer")
        if customer.license_number in self.customers:
            raise ValueError(f"Klient z prawem jazdy o numerze {customer.license_number} jest już zarejestrowany.")
        self.customers[customer.license_number] = customer

    def unregister_customer(self, license_number: str):
        """Usuwa klienta z bazy na podstawie numeru prawa jazdy."""
        if license_number in self.customers:
            del self.customers[license_number]
        else:
            raise ValueError("Nie znaleziono klienta o podanym numerze prawa jazdy.")

    def find_customer_by_license(self, license_number: str):
        """Wyszukuje i zwraca klienta na podstawie numeru prawa jazdy."""
        return self.customers.get(license_number, None)