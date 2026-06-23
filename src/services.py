from src.models import Car, Customer, CarStatus
from datetime import datetime

class Invoice:
    """Dokument finansowy dla wypożyczenia."""

    def __init__(self, amount: float):
        self.amount = amount
        self.is_paid = False
        self.created_at = datetime.now()

    def mark_as_paid(self):
        """Zmienia status faktury na opłaconą."""
        self.is_paid = True


class Rental:
    """Obiekt transakcji reprezentujący wypożyczenie."""

    def __init__(self, customer: Customer, car: Car, days: int):
        self.customer = customer
        self.car = car
        self.days = days
        self.is_active = True

    def calculate_total(self) -> float:
        """Oblicza całkowity koszt wypożyczenia bazując na stawce dziennej."""
        return self.car.daily_rate * self.days


class RentalService:
    """Główny serwis obsługujący logikę wypożyczeń i zwrotów."""

    def __init__(self):
        self.active_rentals = []

    def rent_car(self, customer: Customer, car: Car, days: int) -> Rental:
        """
        Powiązuje klienta z samochodem.
        Zmienia status auta, tworzy obiekt Rental i dodaje go do aktywnych wypożyczeń.
        """
        if car.status != CarStatus.AVAILABLE:
            raise ValueError(f"Samochód {car.get_full_name()} nie jest dostępny do wypożyczenia.")
        if days <= 0:
            raise ValueError("Liczba dni wypożyczenia musi być większa niż 0.")

        # Blokujemy samochód
        car.change_status(CarStatus.RENTED)

        # Tworzymy i zapisujemy transakcję
        rental = Rental(customer, car, days)
        self.active_rentals.append(rental)

        return rental

    def return_car(self, rental: Rental) -> Invoice:
        """
        Kończy wypożyczenie, odblokowuje samochód i wystawia rachunek.
        """
        if not rental.is_active:
            raise ValueError("To wypożyczenie zostało już zakończone.")

        # Odblokowujemy samochód
        rental.car.change_status(CarStatus.AVAILABLE)
        rental.is_active = False

        if rental in self.active_rentals:
            self.active_rentals.remove(rental)

        # Wystawiamy fakturę
        invoice = Invoice(rental.calculate_total())
        return invoice
