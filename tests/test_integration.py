import unittest
from src.models import Car, Customer, CarStatus
from src.services import FleetManager, CustomerRegistry
from src.services import Rental, Invoice, RentalService
class TestRentalProcessIntegration(unittest.TestCase):

    def setUp(self):
        self.fleet_manager = FleetManager()
        self.registry = CustomerRegistry()
        self.rental_service = RentalService()

    # Test integracyjny 1: Pełen proces sukcesu (Dodanie -> Rejestracja -> Wypożyczenie -> Zwrot -> Faktura)
    def test_full_rental_process_success(self):
        car = Car("Audi", "A4", 2021, 150.0)
        customer = Customer("Anna", "Kowalska", "anna@test.pl", "987", "PRAWO123")

        self.fleet_manager.add_car(car)
        self.registry.register_customer(customer)

        # Klient i auto istnieją, auto dostępne
        self.assertIn(car, self.fleet_manager.get_available_cars())

        # Wypożyczamy
        rental = self.rental_service.rent_car(customer, car, 4)

        # Auto nie powinno być już w "dostępnych" według Managera Floty
        self.assertNotIn(car, self.fleet_manager.get_available_cars())

        # Zwracamy i opłacamy
        invoice = self.rental_service.return_car(rental)
        invoice.mark_as_paid()

        self.assertTrue(invoice.is_paid)
        self.assertEqual(invoice.amount, 600.0)  # 4 dni * 150
        # Auto wraca do dostępnych
        self.assertIn(car, self.fleet_manager.get_available_cars())

    # Test integracyjny 2: Odrzucenie wypożyczenia auta, które Manager Floty przeniósł do serwisu
    def test_fleet_manager_maintenance_blocks_rental(self):
        car = Car("Toyota", "Yaris", 2019, 80.0)
        customer = Customer("Jan", "Nowak", "jan@test.pl", "111", "PRAWO456")
        self.fleet_manager.add_car(car)

        # Osoba 2 lub mechanik daje auto do serwisu
        car.change_status(CarStatus.MAINTENANCE)

        # Osoba 3 próbuje je wynająć (powinno zostać zablokowane)
        with self.assertRaises(ValueError):
            self.rental_service.rent_car(customer, car, 2)

        self.assertIn(car, self.fleet_manager.get_cars_in_maintenance())
        # Test integracyjny 3: Wypożyczanie kilku aut z floty i śledzenie dostępności
    def test_multiple_cars_fleet_filtering(self):
        car1 = Car("Ford", "Focus", 2018, 90.0)
        car2 = Car("Skoda", "Octavia", 2022, 120.0)
        customer = Customer("Piotr", "Z", "p@test.pl", "222", "PRAWO789")

        self.fleet_manager.add_car(car1)
        self.fleet_manager.add_car(car2)

        # Na początku obydwa dostępne
        self.assertEqual(len(self.fleet_manager.get_available_cars()), 2)

        # Wypożyczamy jedno z nich
        self.rental_service.rent_car(customer, car1, 1)

        # Manager floty powinien widzieć tylko jedno dostępne
        available_cars = self.fleet_manager.get_available_cars()
        self.assertEqual(len(available_cars), 1)
        self.assertEqual(available_cars[0].brand, "Skoda")

if __name__ == '__main__':
    unittest.main()
