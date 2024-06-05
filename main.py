from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def calcular_interes_compuesto(principal, tasa, tiempo):
    """ Calcula el interés compuesto sobre el principal. """
    return principal * ((1 + tasa/100) ** tiempo) - principal

def main():
    # Pedimos la cuantía base del préstamo
    cuantia_base = float(input("Introduce la cuantía base del préstamo: "))
    
    # Pedimos el tipo de interés
    interes = float(input("Introduce el tipo de interés anual (%): "))
    
    # Pedimos las comisiones
    comision_apertura = float(input("Introduce la comisión de apertura (cantidad fija): "))
    cuantia_total = cuantia_base + comision_apertura
    
    # Aplicar interés si es mayor que cero
    if interes > 0:
        cuantia_total *= (1 + interes / 100)
    
    # Pedimos el valor de cada cuota
    valor_cuota = float(input("Introduce el valor de cada cuota: "))
    
    # Pedimos la fecha de inicio del préstamo
    fecha_inicio = input("Introduce la fecha de inicio del préstamo (formato DD/MM/AAAA): ")
    fecha_inicio = datetime.strptime(fecha_inicio, "%d/%m/%Y")
    
    # Calculamos cuántas cuotas se han pagado hasta hoy
    fecha_actual = datetime.now()
    meses_pasados = (fecha_actual.year - fecha_inicio.year) * 12 + (fecha_actual.month - fecha_inicio.month)
    
    # Calculamos cuánto se ha pagado hasta ahora
    pagado_hasta_ahora = meses_pasados * valor_cuota

    # Calculamos el interés acumulado hasta la fecha
    interes_acumulado = calcular_interes_compuesto(cuantia_base, interes, meses_pasados / 12)
    
    # Capital amortizado es lo pagado hasta ahora menos el interés acumulado
    capital_amortizado = pagado_hasta_ahora - interes_acumulado - comision_apertura
    
    # Asegurar que no se reporte más capital amortizado del préstamo
    if capital_amortizado > cuantia_base:
        capital_amortizado = cuantia_base
    
    print(f"Capital amortizado hasta la fecha: {capital_amortizado:.2f} EUR")
    
    # Verificamos que no se haya pagado más de lo debido
    if pagado_hasta_ahora > cuantia_total:
        pagado_hasta_ahora = cuantia_total
    
    # Calculamos cuánto queda por pagar antes de cualquier pago extraordinario
    resta_pagar = cuantia_total - pagado_hasta_ahora
    print(f"Queda por pagar antes de la aportación extraordinaria: {resta_pagar:.2f} EUR")
    
    # Calculamos y mostramos la fecha de finalización antes del pago extraordinario
    meses_restantes = int(resta_pagar // valor_cuota)
    fecha_finalizacion = fecha_actual + relativedelta(months=meses_restantes)
    print(f"Fecha de finalización estimada antes de la aportación extraordinaria: {fecha_finalizacion.strftime('%d/%m/%Y')}")

    # Preguntamos si el usuario quiere realizar un pago extraordinario
    respuesta = input("¿Quieres aportar una cuantía extraordinaria? (s/n): ")
    if respuesta.lower() == 'n':
        return  # Finaliza el programa si no se desea hacer un pago extraordinario

    pago_extraordinario = float(input("Introduce la cuantía extraordinaria: "))
    
    # Calculamos cuánto queda por pagar tras el pago extraordinario
    resta_pagar_post = resta_pagar - pago_extraordinario
    print(f"Queda por pagar después de la aportación extraordinaria: {resta_pagar_post:.2f} EUR")
    
    # Calculamos las cuotas restantes después del pago extraordinario
    cuotas_restantes_post = int(resta_pagar_post // valor_cuota)
    if resta_pagar_post % valor_cuota != 0:
        cuotas_restantes_post += 1  # Añadimos una cuota más si queda un resto

    # Calculamos y mostramos la fecha de finalización después del pago extraordinario
    fecha_finalizacion_post = fecha_actual + relativedelta(months=cuotas_restantes_post)
    print(f"Fecha de finalización estimada después de la aportación extraordinaria: {fecha_finalizacion_post.strftime('%d/%m/%Y')}")

if __name__ == "__main__":
    main()
