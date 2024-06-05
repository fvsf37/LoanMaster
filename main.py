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


def main():
    """Main function to run the loan calculation program."""
    base_amount = float(input("Introduce la cuantía base del préstamo: "))
    interest_rate = float(input("Introduce el tipo de interés anual (%): "))
    opening_fee = float(
        input("Introduce la comisión de apertura (cantidad fija): "))
    total_amount = base_amount + opening_fee

    if interest_rate > 0:
        total_amount *= (1 + interest_rate / 100)

    installment_value = float(input("Introduce el valor de cada cuota: "))
    start_date = input(
        "Introduce la fecha de inicio del préstamo (formato DD/MM/AAAA): ")
    start_date = datetime.strptime(start_date, "%d/%m/%Y")

    current_date = datetime.now()
    months_passed = (current_date.year - start_date.year) * \
        12 + (current_date.month - start_date.month)
    paid_until_now = months_passed * installment_value
    accumulated_interest = calculate_compound_interest(
        base_amount, interest_rate, months_passed / 12)
    amortized_capital = paid_until_now - accumulated_interest - opening_fee

    if amortized_capital > base_amount:
        amortized_capital = base_amount

    # Create the initial summary table
    table = Table(title="Resumen del Préstamo", style="bold magenta")
    table.add_column("Concepto", justify="left", style="cyan", no_wrap=True)
    table.add_column("Cantidad", justify="right", style="green")

    table.add_row("Capital amortizado hasta la fecha:",
                  f"{amortized_capital:.2f} EUR")

    if paid_until_now > total_amount:
        paid_until_now = total_amount

    amount_remaining = total_amount - paid_until_now
    table.add_row("Queda por pagar:", f"{amount_remaining:.2f} EUR")

    total_installments = int(total_amount // installment_value)
    end_date = start_date + relativedelta(months=total_installments)
    table.add_row("Fecha de finalización estimada:",
                  end_date.strftime('%d/%m/%Y'))

    console.print(Panel(Align.center(
        table), title="[bold green]Resumen del Préstamo[/bold green]", border_style="bright_magenta"))

    response = input("\n¿Quieres aportar una cuantía extraordinaria? (s/n): ")
    if response.lower() == 'n':
        print(
            "\n[bold red]No se realizará una aportación extraordinaria. Fin del programa.[/bold red]")
        return

    extra_payment = float(input("Introduce la cuantía extraordinaria: "))
    amount_remaining_post = amount_remaining - extra_payment

    # Create the summary table after the extra payment
    table_post = Table(
        title="Resumen Después de la Aportación Extraordinaria", style="bold magenta")
    table_post.add_column("Concepto", justify="left",
                          style="cyan", no_wrap=True)
    table_post.add_column("Cantidad", justify="right", style="green")

    table_post.add_row("Queda por pagar después de la aportación extraordinaria:",
                       f"{amount_remaining_post:.2f} EUR")

    remaining_installments_post = int(
        amount_remaining_post // installment_value)
    if amount_remaining_post % installment_value != 0:
        remaining_installments_post += 1

    end_date_post = current_date + \
        relativedelta(months=remaining_installments_post)
    table_post.add_row("Fecha de finalización estimada después de la aportación extraordinaria:",
                       end_date_post.strftime('%d/%m/%Y'))

    console.print(Panel(Align.center(
        table_post), title="[bold green]Resumen Después de la Aportación Extraordinaria[/bold green]", border_style="bright_magenta"))


if __name__ == "__main__":
    main()
