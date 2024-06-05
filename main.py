from datetime import datetime
from dateutil.relativedelta import relativedelta
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def calculate_compound_interest(principal, rate, time):
    """Calculates compound interest on the principal."""
    return principal * ((1 + rate / 100) ** time) - principal

def get_positive_float(prompt):
    """Prompts the user for a positive float value."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                raise ValueError("La cantidad no puede ser negativa.")
            return value
        except ValueError as e:
            print(f"{Fore.RED}Entrada inválida: {e}")

def get_date(prompt):
    """Prompts the user for a date in the format DD/MM/YYYY."""
    while True:
        try:
            date_str = input(prompt)
            return datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            print(f"{Fore.RED}Formato de fecha inválido. Por favor, use DD/MM/AAAA.")

def get_yes_or_no(prompt):
    """Prompts the user for a 's' or 'n' response."""
    while True:
        response = input(prompt).lower()
        if response in ['s', 'n']:
            return response
        print(f"{Fore.RED}Entrada inválida. Por favor, introduce 's' o 'n'.")

def print_summary(title, amortized_capital, amount_remaining, end_date):
    """Prints a summary of the loan status."""
    print("\n" + "═" * 40)
    print(f"{Fore.BLUE}{Style.BRIGHT}          {title}          ")
    print("═" * 40)
    print(f"Capital amortizado hasta la fecha: {amortized_capital:.2f} EUR")
    print(f"Queda por pagar: {amount_remaining:.2f} EUR")
    print(f"Fecha de finalización estimada: {end_date.strftime('%d/%m/%Y')}")
    print("═" * 40 + "\n")

def calculate_amortization(base_amount, interest_rate, opening_fee, paid_until_now):
    """Calculates the amortized capital and the remaining amount to be paid."""
    accumulated_interest = calculate_compound_interest(
        base_amount, interest_rate, paid_until_now / 12)
    amortized_capital = max(
        paid_until_now - accumulated_interest - opening_fee, 0)
    return amortized_capital

def main():
    """Main function to run the loan calculation program."""
    base_amount = get_positive_float("Introduce la cuantía base del préstamo: ")
    interest_rate = get_positive_float("Introduce el tipo de interés anual (%): ")
    opening_fee = get_positive_float("Introduce la comisión de apertura (cantidad fija): ")

    total_amount = base_amount + opening_fee
    if interest_rate > 0:
        total_amount *= (1 + interest_rate / 100)

    installment_value = get_positive_float("Introduce el valor de cada cuota: ")
    start_date = get_date("Introduce la fecha de inicio del préstamo (formato DD/MM/AAAA): ")

    current_date = datetime.now()
    months_passed = (current_date.year - start_date.year) * 12 + (current_date.month - start_date.month)
    paid_until_now = months_passed * installment_value

    amortized_capital = calculate_amortization(base_amount, interest_rate, opening_fee, paid_until_now)
    amount_remaining = max(total_amount - paid_until_now, 0)

    total_installments = int(total_amount // installment_value)
    end_date = start_date + relativedelta(months=total_installments)

    print_summary("RESUMEN DEL PRÉSTAMO", amortized_capital, amount_remaining, end_date)

    if get_yes_or_no("¿Quieres aportar una cuantía extraordinaria? (s/n): ") == 'n':
        print(f"\n{Fore.RED}No se realizará una aportación extraordinaria. Fin del programa.")
        return

    extra_payment = get_positive_float("Introduce la cuantía extraordinaria: ")
    while extra_payment > amount_remaining:
        print(f"{Fore.RED}Entrada inválida: La cuantía extraordinaria no puede ser mayor que lo que queda por pagar ({amount_remaining:.2f} EUR).")
        extra_payment = get_positive_float("Introduce la cuantía extraordinaria: ")

    amortized_capital += extra_payment
    amount_remaining -= extra_payment
    amount_remaining = max(amount_remaining, 0)

    remaining_installments_post = int(amount_remaining // installment_value)
    if amount_remaining % installment_value != 0:
        remaining_installments_post += 1

    end_date_post = current_date + relativedelta(months=remaining_installments_post)
    print_summary("RESUMEN DESPUÉS DE LA APORTACIÓN EXTRA", amortized_capital, amount_remaining, end_date_post)

if __name__ == "__main__":
    main()
