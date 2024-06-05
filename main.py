from datetime import datetime
from dateutil.relativedelta import relativedelta
from rich import print
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

console = Console()


def calculate_compound_interest(principal, rate, time):
    """Calculates compound interest on the principal."""
    return principal * ((1 + rate / 100) ** time) - principal


def get_positive_float(prompt):
    """
    Prompts the user for a positive float value.

    Args:
        prompt (str): The message to display to the user.

    Returns:
        float: The positive float value entered by the user.
    """
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print(
                    f"[bold red]Entrada inválida: La cantidad no puede ser negativa.[/bold red]")
                continue
            return value
        except ValueError as e:
            print(f"[bold red]Entrada inválida: {e}[/bold red]")


def get_date(prompt):
    """
    Prompts the user for a date in the format DD/MM/YYYY.

    Args:
        prompt (str): The message to display to the user.

    Returns:
        datetime: The date entered by the user.
    """
    while True:
        try:
            date_str = input(prompt)
            return datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            print(
                f"[bold red]Formato de fecha inválido. Por favor, use DD/MM/AAAA.[/bold red]")


def get_yes_or_no(prompt):
    """
    Prompts the user for a 's' or 'n' response.

    Args:
        prompt (str): The message to display to the user.

    Returns:
        str: 's' or 'n' based on user input.
    """
    while True:
        response = input(prompt).lower()
        if response in ['s', 'n']:
            return response
        print(f"[bold red]Entrada inválida. Por favor, introduce 's' o 'n'.[/bold red]")


def print_summary(title, amortized_capital, amount_remaining, end_date):
    """
    Prints a summary of the loan status.

    Args:
        title (str): The title of the summary.
        amortized_capital (float): The amount of capital amortized.
        amount_remaining (float): The remaining amount to be paid.
        end_date (datetime): The estimated end date of the loan.
    """
    table = Table(title=title, style="bold magenta")
    table.add_column("Concepto", justify="left", style="cyan", no_wrap=True)
    table.add_column("Cantidad", justify="right", style="green")

    table.add_row("Capital amortizado hasta la fecha:",
                  f"{amortized_capital:.2f} EUR")
    table.add_row("Queda por pagar:", f"{amount_remaining:.2f} EUR")
    table.add_row("Fecha de finalización estimada:",
                  end_date.strftime('%d/%m/%Y'))

    console.print(Panel(Align.center(
        table), title=f"[bold green]{title}[/bold green]", border_style="bright_magenta"))


def main():
    """Main function to run the loan calculation program."""
    base_amount = get_positive_float(
        "Introduce la cuantía base del préstamo: ")

    print(f"[bold blue]Si no existen intereses, introduce cero.[/bold blue]")
    interest_rate = get_positive_float(
        "Introduce el tipo de interés anual (%): ")

    opening_fee = get_positive_float(
        "Introduce la comisión de apertura (cantidad fija): ")

    total_amount = base_amount + opening_fee
    if interest_rate > 0:
        total_amount *= (1 + interest_rate / 100)

    installment_value = get_positive_float(
        "Introduce el valor de cada cuota: ")
    start_date = get_date(
        "Introduce la fecha de inicio del préstamo (formato DD/MM/AAAA): ")

    current_date = datetime.now()
    months_passed = (current_date.year - start_date.year) * \
        12 + (current_date.month - start_date.month)
    paid_until_now = months_passed * installment_value
    accumulated_interest = calculate_compound_interest(
        base_amount, interest_rate, months_passed / 12)
    amortized_capital = paid_until_now - accumulated_interest - opening_fee

    if amortized_capital > base_amount:
        amortized_capital = base_amount

    amount_remaining = total_amount - paid_until_now
    total_installments = int(total_amount // installment_value)
    end_date = start_date + relativedelta(months=total_installments)

    print_summary("Resumen del Préstamo", amortized_capital,
                  amount_remaining, end_date)

    response = get_yes_or_no(
        "¿Quieres aportar una cuantía extraordinaria? (s/n): ")
    if response == 'n':
        print(
            "\n[bold red]No se realizará una aportación extraordinaria. Fin del programa.[/bold red]")
        return

    while True:
        extra_payment = get_positive_float(
            "Introduce la cuantía extraordinaria: ")
        if extra_payment > amount_remaining:
            print(
                f"[bold red]Entrada inválida: La cuantía extraordinaria no puede ser mayor que lo que queda por pagar ({amount_remaining:.2f} EUR).[/bold red]")
        else:
            break

    amortized_capital += extra_payment
    amount_remaining -= extra_payment
    amount_remaining = max(amount_remaining, 0)

    remaining_installments_post = int(amount_remaining // installment_value)
    if amount_remaining % installment_value != 0:
        remaining_installments_post += 1

    end_date_post = current_date + \
        relativedelta(months=remaining_installments_post)

    table_post = Table(
        title="Resumen Después de la Aportación Extraordinaria", style="bold magenta")
    table_post.add_column("Concepto", justify="left",
                          style="cyan", no_wrap=True)
    table_post.add_column("Cantidad", justify="right", style="green")

    table_post.add_row(
        "Queda por pagar después de la aportación extraordinaria:", f"{amount_remaining:.2f} EUR")
    table_post.add_row("Fecha de finalización estimada después de la aportación extraordinaria:",
                       end_date_post.strftime('%d/%m/%Y'))

    console.print(Panel(Align.center(
        table_post), title="[bold green]Resumen Después de la Aportación Extraordinaria[/bold green]", border_style="bright_magenta"))


if __name__ == "__main__":
    main()
