import unittest
from src.models import Car, Customer, CarStatus
from src.services import FleetManager, CustomerRegistry
from src.services import Rental, Invoice, RentalService

class TestRentalProcessUnit(unittest.TestCase):
    """TESTY JEDNOSTKOWE"""

    def setUp(self):
        self.car = Car("BMW", "X5", 2020, 100.0)
        self.customer = Customer("John", "Doe", "john@example.com", "123", "L123")
        self.service = RentalService()

    # Test 1: Obliczanie ceny za X dni
    def test_rental_calculate_total(self):
        rental = Rental(self.customer, self.car, 5)  # 5 dni * 100$
        self.assertEqual(rental.calculate_total(), 500.0)

    # Test 2: Zmiana statusu faktury na opłaconą
    def test_invoice_mark_as_paid(self):
        invoice = Invoice(250.0)
        self.assertFalse(invoice.is_paid)
        invoice.mark_as_paid()
        self.assertTrue(invoice.is_paid)

    # Test 3: Prawidłowe utworzenie wypożyczenia i zmiana statusu auta
    def test_rent_car_success(self):
        rental = self.service.rent_car(self.customer, self.car, 3)
        self.assertEqual(self.car.status, CarStatus.RENTED)
        self.assertIn(rental, self.service.active_rentals)

    # Test 4: Próba wypożyczenia niedostępnego auta rzuca błąd
    def test_rent_car_unavailable_raises_error(self):
        self.car.change_status(CarStatus.MAINTENANCE)
        with self.assertRaises(ValueError):
            self.service.rent_car(self.customer, self.car, 3)

    # Test 5: Poprawny zwrot auta wystawia fakturę i odblokowuje auto
    def test_return_car_generates_invoice(self):
        rental = self.service.rent_car(self.customer, self.car, 2)
        invoice = self.service.return_car(rental)

        self.assertEqual(self.car.status, CarStatus.AVAILABLE)
        self.assertFalse(rental.is_active)
        self.assertEqual(invoice.amount, 200.0)
        self.assertNotIn(rental, self.service.active_rentals)

if __name__ == '__main__':
    unittest.main()
