import unittest
from models import Car, Customer, CarStatus
from services import FleetManager, CustomerRegistry
from services import Rental, Invoice, RentalService, LoyaltyProgram

class TestRentalProcessUnit(unittest.TestCase):

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


class TestLogisticsManager(unittest.TestCase):

    def setUp(self):
        # Inicjalizacja przed każdym testem osobno
        self.fleet_manager = FleetManager()
        self.registry = CustomerRegistry()

        # Obiekty testowe
        self.car1 = Car("BMW", "X5", 2020, 100)
        self.car2 = Car("Audi", "A4", 2019, 80)
        self.car3 = Car("BMW", "3 Series", 2021, 90)
        self.car4 = Car("Tesla", "Model 3", 2022, 120)

        # Zmiana statusów aut na potrzeby testów filtracji
        self.car3.change_status(CarStatus.MAINTENANCE)  # BMW w serwisie
        self.car4.change_status(CarStatus.RENTED)  # Tesla wypożyczona

        self.customer1 = Customer("John", "Doe", "john@example.com", "123-456-7890", "L12345678")

    def test_add_and_remove_car(self) -> None:
        """Test 1: Sprawdzenie poprawnego dodawania i usuwania pojazdu z floty."""
        self.fleet_manager.add_car(self.car1)
        self.assertIn(self.car1, self.fleet_manager.cars)
        self.assertEqual(len(self.fleet_manager.cars), 1)

        self.fleet_manager.remove_car(self.car1)
        self.assertNotIn(self.car1, self.fleet_manager.cars)

    def test_search_by_brand(self) -> None:
        """Test 2: Wyszukiwanie samochodów po marce (case-insensitive)."""
        self.fleet_manager.add_car(self.car1)
        self.fleet_manager.add_car(self.car2)
        self.fleet_manager.add_car(self.car3)

        bmw_cars = self.fleet_manager.search_by_brand("bmw")
        self.assertEqual(len(bmw_cars), 2)


    def test_filter_available_cars(self) -> None:
        """Test 3: Filtrowanie tylko dostępnych samochodów."""
        self.fleet_manager.add_car(self.car1)
        self.fleet_manager.add_car(self.car3)
        self.fleet_manager.add_car(self.car4)

        available = self.fleet_manager.get_available_cars()
        self.assertEqual(len(available), 1)

    def test_get_cars_in_maintenance(self) -> None:
        """Test 4: Sprawdzanie czy poprawnie odfiltrowuje auta w serwisie."""
        self.fleet_manager.add_car(self.car1)
        self.fleet_manager.add_car(self.car3)

        maintenance_cars = self.fleet_manager.get_cars_in_maintenance()
        self.assertEqual(len(maintenance_cars), 1)

    def test_customer_registration_and_lookup(self) -> None:
        """Test 5: Rejestracja klienta oraz wyszukiwanie po numerze prawa jazdy."""
        self.registry.register_customer(self.customer1)
        found = self.registry.find_customer_by_license("L12345678")

        self.assertIsNotNone(found)
        self.assertEqual(found.name, "John")
        self.assertEqual(found.last_name, "Doe")


class TestLoyaltyProgram(unittest.TestCase):

    def setUp(self):

        self.loyalty_program = LoyaltyProgram()
        self.customer = Customer(
            name="Anna",
            last_name="Nowak",
            email="anna@example.com",
            phone="987-654",
            license_number="DL98765"
        )

    def test_add_completed_rental(self):

        # Początkowo klient nie powinien mieć żadnych wypożyczeń (historia zwraca 0)
        initial_count = self.loyalty_program.rental_history.get(self.customer.license_number, 0)
        self.assertEqual(initial_count, 0)

        # Dodajemy pierwsze wypożyczenie
        self.loyalty_program.add_completed_rental(self.customer)
        self.assertEqual(self.loyalty_program.rental_history[self.customer.license_number], 1)

        # Dodajemy drugie wypożyczenie i sprawdzamy, czy wartość wzrosła do 2
        self.loyalty_program.add_completed_rental(self.customer)
        self.assertEqual(self.loyalty_program.rental_history[self.customer.license_number], 2)

    def test_calculate_discount(self):

        base_amount = 100.0

        # Scenariusz 1: 0 wypożyczeń -> brak zniżki (0%)
        amount = self.loyalty_program.calculate_discount(self.customer, base_amount)
        self.assertEqual(amount, 100.0)

        # Scenariusz 2: 3 wypożyczenia -> zniżka 10%
        for _ in range(3):
            self.loyalty_program.add_completed_rental(self.customer)

        amount = self.loyalty_program.calculate_discount(self.customer, base_amount)
        self.assertEqual(amount, 90.0)  # 100 * 0.9

        # Scenariusz 3: 5 wypożyczeń (dodajemy kolejne 2) -> zniżka 20%
        for _ in range(2):
            self.loyalty_program.add_completed_rental(self.customer)

        amount = self.loyalty_program.calculate_discount(self.customer, base_amount)
        self.assertEqual(amount, 80.0)  # 100 * 0.8

if __name__ == '__main__':
    unittest.main()

