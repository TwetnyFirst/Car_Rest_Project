
class CarStatus:
    AVAILABLE = 'available'
    RENTED = 'rented'
    MAINTENANCE = 'maintenance'

class Car:
    def __init__(self,brand, model, year, daily_rate):
        self.brand = brand,
        self.model = model,
        self.year = year,
        self.daily_rate = daily_rate,
        self.status = CarStatus.AVAILABLE

    def get_full_name(self):
        return f'{self.brand} {self.model} {self.year}'
    
    def get_info_for_rent(self):
        return f'Car is {self.status}, daily rate: ${self.daily_rate}'
    
    def change_status(self, new_status):
        if new_status in (CarStatus.AVAILABLE, CarStatus.RENTED, CarStatus.MAINTENANCE):
            self.status = new_status
        else:
            raise ValueError(f'Invalid status: {new_status}')
    

