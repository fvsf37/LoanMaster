from datetime import datetime, timedelta


def main():
    # Pedimos la cuantía total del préstamo (intereses incluidos)
    cuantia_total = float(
        input("Introduce la cuantía total del préstamo (intereses incluidos): "))

    # Pedimos el valor de cada cuota
    valor_cuota = float(input("Introduce el valor de cada cuota: "))

    # Pedimos la fecha de inicio del préstamo
    fecha_inicio = input(
        "Introduce la fecha de inicio del préstamo (formato DD/MM/AAAA): ")
    fecha_inicio = datetime.strptime(fecha_inicio, "%d/%m/%Y")

    # Calculamos cuántas cuotas se han pagado hasta hoy
    fecha_actual = datetime.now()
    meses_pasados = (fecha_actual.year - fecha_inicio.year) * \
        12 + (fecha_actual.month - fecha_inicio.month)

    # Calculamos cuánto se ha pagado hasta ahora
    pagado_hasta_ahora = meses_pasados * valor_cuota

    # Verificamos que no se haya pagado más de lo debido
    if pagado_hasta_ahora > cuantia_total:
        pagado_hasta_ahora = cuantia_total

    # Calculamos cuánto queda por pagar antes de cualquier pago extraordinario
    resta_pagar = cuantia_total - pagado_hasta_ahora

    # Mostramos la deuda restante antes del pago extraordinario
    print(
        f"Queda por pagar antes de la aportación extraordinaria: {resta_pagar:.2f} EUR")

    # Calculamos y mostramos la fecha de finalización antes del pago extraordinario
    meses_restantes = int(resta_pagar // valor_cuota)
    fecha_finalizacion = fecha_inicio + timedelta(days=meses_restantes * 30)
    print(
        f"Fecha de finalización estimada antes de la aportación extraordinaria: {fecha_finalizacion.strftime('%d/%m/%Y')}")

    # Preguntamos si el usuario quiere realizar un pago extraordinario
    respuesta = input("¿Quieres aportar una cuantía extraordinaria? (s/n): ")
    pago_extraordinario = 0
    if respuesta.lower() == 's':
        pago_extraordinario = float(
            input("Introduce la cuantía extraordinaria: "))

    # Calculamos cuánto queda por pagar tras el pago extraordinario
    resta_pagar_post = resta_pagar - pago_extraordinario
    print(
        f"Queda por pagar después de la aportación extraordinaria: {resta_pagar_post:.2f} EUR")

    # Calculamos las cuotas restantes después del pago extraordinario
    cuotas_restantes_post = int(resta_pagar_post // valor_cuota)
    if resta_pagar_post % valor_cuota != 0:
        cuotas_restantes_post += 1  # Añadimos una cuota más si queda un resto

    # Calculamos y mostramos la fecha de finalización después del pago extraordinario
    fecha_finalizacion_post = fecha_inicio + \
        timedelta(days=cuotas_restantes_post * 30)
    print(
        f"Fecha de finalización estimada después de la aportación extraordinaria: {fecha_finalizacion_post.strftime('%d/%m/%Y')}")


if __name__ == "__main__":
    main()
