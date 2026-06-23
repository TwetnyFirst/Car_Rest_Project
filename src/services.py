from src.models import Car, Customer, CarStatus

class FleetManager:
    """
    Klasa odpowiedzialna za zarządzanie listą samochodów w wypożyczalni.
    Umożliwia dodawanie, usuwanie oraz zaawansowane filtrowanie aut.
    """
    def __init__(self) -> None:
        self.cars: list[Car] = []

    def add_car(self, car: Car) -> None:
        """Dodaje nowy samochód do floty."""
        if not isinstance(car, Car):
            raise TypeError("Można dodać tylko obiekt klasy Car")
        self.cars.append(car)
        
    def remove_car(self, car: Car) -> None:
        """Usuwa samochód z floty."""
        if car in self.cars:
            self.cars.remove(car)
        else:
            raise ValueError("Podany samochód nie znajduje się we flocie")

    def get_available_cars(self) -> list[Car]:
        """Zwraca listę samochodów, które są aktualnie dostępne."""
        return [car for car in self.cars if car.status == CarStatus.AVAILABLE]

    def search_by_brand(self, brand: str) -> list[Car]:
        """Wyszukuje samochody według marki."""
        return [car for car in self.cars if car.brand.strip().lower() == brand.strip().lower()]

    def get_cars_in_maintenance(self) -> list[Car]:
        """Zwraca listę samochodów w serwisie."""
        return [car for car in self.cars if car.status == CarStatus.MAINTENANCE]


class CustomerRegistry:
    """
    Klasa odpowiedzialna za zarządzanie bazą klientów wypożyczalni.
    """
    def __init__(self) -> None:
        # Słownik, gdzie klucz to str (prawo jazdy), a wartość to obiekt Customer
        self.customers: dict[str, Customer] = {}  

    def register_customer(self, customer: Customer) -> None:
        """Rejestruje nowego klienta w bazie danych."""
        if not isinstance(customer, Customer):
            raise TypeError("Można zarejestrować tylko obiekt klasy Customer")
        if customer.license_number in self.customers:
            raise ValueError(f"Klient o numerze {customer.license_number} już istnieje.")
        self.customers[customer.license_number] = customer

    def unregister_customer(self, license_number: str) -> None:
        """Usuwa klienta z bazy na podstawie numeru prawa jazdy."""
        if license_number in self.customers:
            del self.customers[license_number]
        else:
            raise ValueError("Nie znaleziono klienta o podanym numerze prawa jazdy.")

    def find_customer_by_license(self, license_number: str) -> Customer | None:
        """Wyszukuje i zwraca klienta lub None, jeśli go nie ma."""
        return self.customers.get(license_number, None)
