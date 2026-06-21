

# Classes for Car 

class CarStatus: # all car statuses
    AVAILABLE = 'available'
    RENTED = 'rented'
    MAINTENANCE = 'maintenance'

class Car: 
    def __init__(self,brand, model, year, daily_rate): #for example - BMW, X5, 2020, 100 ($/per day)
        self.brand = brand
        self.model = model
        self.year = year
        self.daily_rate = daily_rate
        self.status = CarStatus.AVAILABLE

    def get_full_name(self): # returns full name of the car
        return f'{self.brand} {self.model} {self.year}'
    
    def get_info_for_rent(self): # returns information about the car for rent
        return f'Car is {self.status}, daily rate: ${self.daily_rate}'
    
    def change_status(self, new_status): # changes the status of the car
        if new_status in (CarStatus.AVAILABLE, CarStatus.RENTED, CarStatus.MAINTENANCE):
            self.status = new_status
        else:
            raise ValueError(f'Invalid status: {new_status}')
    def say():
        return "I am a car"
    

# Class for Customer
class Customer:
    def __init__(self, name, email, phone, license_number): # for example - John Doe, john.doe@example.com, 123-456-7890, L12345678
        self.name = name
        self.email = email
        self.phone = phone
        self.license_number = license_number

    def get_info(self): # returns information about the customer
        return f'Customer: {self.name}, Email: {self.email}, Phone: {self.phone}, License: {self.license_number}'
