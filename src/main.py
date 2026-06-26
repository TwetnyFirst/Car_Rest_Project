import sys
from models import Car, Customer
from services import FleetManager, CustomerRegistry, RentalService, LoyaltyProgram


def main():
    # 1. Inicjalizacja wszystkich serwisów
    fleet_manager = FleetManager()
    customer_registry = CustomerRegistry()
    rental_service = RentalService()
    loyalty_program = LoyaltyProgram()

    # 2. Mockowanie danych
    fleet_manager.add_car(Car("Toyota", "Corolla", 2021, 120))
    fleet_manager.add_car(Car("BMW", "X5", 2023, 350))
    fleet_manager.add_car(Car("Ford", "Focus", 2020, 100))

    test_customer = Customer("Jan", "Kowalski", "jan@example.com", "123-456", "PRAWO123")
    customer_registry.register_customer(test_customer)

    # 3. Główna pętla programu
    while True:
        print("\n" + "=" * 40)
        print(" 🚗 CAR RENTAL SERVICE - MENU GŁÓWNE 🚗")
        print("=" * 40)
        print("1. Pokaż dostępne samochody")
        print("2. Zarejestruj nowego klienta")
        print("3. Wypożycz samochód")
        print("4. Zwróć samochód")
        print("5. Wyjdź")

        choice = input("\nWybierz opcję (1-5): ")

        if choice == '1':
            print("\n--- Dostępne samochody ---")
            available_cars = fleet_manager.get_available_cars()
            if not available_cars:
                print("Brak dostępnych aut w tej chwili.")
            else:
                for idx, car in enumerate(available_cars, 1):
                    print(f"{idx}. {car.get_full_name()} - {car.get_info_for_rent()}")

        elif choice == '2':
            print("\n--- Rejestracja klienta ---")
            name = input("Imię: ")
            last_name = input("Nazwisko: ")
            email = input("Email: ")
            phone = input("Telefon: ")
            license_number = input("Numer prawa jazdy: ")

            try:
                new_customer = Customer(name, last_name, email, phone, license_number)
                customer_registry.register_customer(new_customer)
                print(f"✅ Zarejestrowano klienta: {name} {last_name}")
            except ValueError as e:
                print(f"❌ Błąd: {e}")

        elif choice == '3':
            print("\n--- Wypożyczenie samochodu ---")
            license_num = input("Podaj numer prawa jazdy klienta: ")
            customer = customer_registry.find_customer_by_license(license_num)

            if not customer:
                print("❌ Nie znaleziono klienta o podanym numerze prawa jazdy.")
                continue

            available_cars = fleet_manager.get_available_cars()
            if not available_cars:
                print("❌ Wszystkie auta są aktualnie wypożyczone.")
                continue

            for idx, car in enumerate(available_cars, 1):
                print(f"{idx}. {car.get_full_name()} (Cena: ${car.daily_rate}/dzień)")

            try:
                car_idx = int(input("\nWybierz numer samochodu z listy powyżej: ")) - 1
                if car_idx < 0 or car_idx >= len(available_cars):
                    print("❌ Nieprawidłowy numer auta.")
                    continue

                selected_car = available_cars[car_idx]
                days = int(input("Na ile dni chcesz wypożyczyć pojazd? "))

                # Logika wypożyczenia
                rental_service.rent_car(customer, selected_car, days)
                print(f"✅ Sukces! Wypożyczono {selected_car.get_full_name()} dla {customer.name}.")

            except ValueError as e:
                print(f"❌ Błąd: {e}")

        elif choice == '4':
            print("\n--- Zwrot samochodu ---")
            if not rental_service.active_rentals:
                print("Brak aktywnych wypożyczeń do zwrotu.")
                continue

            for idx, rental in enumerate(rental_service.active_rentals, 1):
                print(
                    f"{idx}. {rental.car.get_full_name()} (Wypożyczający: {rental.customer.name} {rental.customer.last_name})")
            try:
                rent_idx = int(input("\nWybierz numer wypożyczenia, które chcesz zakończyć: ")) - 1
                if rent_idx < 0 or rent_idx >= len(rental_service.active_rentals):
                    print("❌ Nieprawidłowy wybór.")
                    continue

                selected_rental = rental_service.active_rentals[rent_idx]
                customer = selected_rental.customer

                # Kończymy wypożyczenie, odbieramy fakturę (z services.py)
                invoice = rental_service.return_car(selected_rental)
                invoice.mark_as_paid()

                # Aplikujemy zniżki z programu lojalnościowego
                final_amount = loyalty_program.calculate_discount(customer, invoice.amount)

                # Po udanym zwrocie zapisujemy klientowi "+1 wypożyczenie" na poczet przyszłych zniżek
                loyalty_program.add_completed_rental(customer)

                print(f"\n✅ Pomyślnie zwrócono: {selected_rental.car.get_full_name()}")
                if final_amount < invoice.amount:
                    print(f"🎉 Klient otrzymał zniżkę dla stałych klientów!")
                    print(f"💰 Pierwotna cena: ${invoice.amount:.2f}")
                    print(f"💰 Do zapłaty (po zniżce): ${final_amount:.2f}")
                else:
                    print(f"💰 Do zapłaty: ${final_amount:.2f}")

            except ValueError as e:
                print(f"❌ Błąd: {e}")

        elif choice == '5':
            print("\nZamykanie aplikacji. Do zobaczenia!")
            sys.exit()

        else:
            print("❌ Wybrano nieprawidłową opcję. Spróbuj ponownie.")


if __name__ == "__main__":
    main()