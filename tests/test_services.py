import unittest
from src.models import Car, Customer, CarStatus
from src.services import FleetManager, CustomerRegistry


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


if __name__ == '__main__':
    unittest.main()
