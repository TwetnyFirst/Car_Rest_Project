from src.models import Car, CarStatus, Customer
#================================================================================================================
#Tests for the Car model

def test_new_car_has_available_status() -> None: # New Car should have status AVAILABLE

    car = Car(brand="Toyota", model="Yaris", year=2022, daily_rate=150.0)
    
    assert car.status == CarStatus.AVAILABLE


def test_car_change_status() -> None: # Test changing the status of a car

    car = Car(brand="Toyota", model="Yaris", year=2022, daily_rate=150.0)
    

    car.change_status(CarStatus.RENTED)
    assert car.status == CarStatus.RENTED
    
    car.change_status(CarStatus.MAINTENANCE)
    assert car.status == CarStatus.MAINTENANCE

def test_car_get_full_name() -> None: # Test getting the full name of a car

    car = Car(brand="Toyota", model="Yaris", year=2022, daily_rate=150.0) 
    
    assert car.get_full_name() == "Toyota Yaris 2022"


#================================================================================================================
#tests for Customer model
def test_customer_get_info() -> None: # Test getting the information of a customer

    customer = Customer(name="Jan", last_name="Kowalski", email="jan@poczta.pl", phone="123-456-7890", license_number="L1234567")
    
    assert customer.get_info() == "Customer: Jan Kowalski, Email: jan@poczta.pl, Phone: 123-456-7890, License: L1234567"

def test_customer_email() -> None: # test if the email of a customer contains '@' symbol

    customer = Customer(name="Jan", last_name="Kowalski", email="jan@poczta.pl", phone="123-456-7890", license_number="L1234567")
    
    assert customer.email.__contains__("@")