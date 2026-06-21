from src.models import Car, CarStatus

# car1 = Car(brand="Toyota", model="Yaris",year=2022, daily_rate=150.0)
# print(car1.get_full_name())  # Output: "Toyota Yaris (2022)"

def test_new_car_has_available_status() -> None:

    car = Car(brand="Toyota", model="Yaris", year=2022, daily_rate=150.0)
    
    assert car.status == CarStatus.AVAILABLE