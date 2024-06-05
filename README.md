# Calculadora de Préstamos

Este proyecto es una calculadora de préstamos que permite a los usuarios calcular el capital amortizado, la cantidad restante por pagar y la fecha de finalización estimada de un préstamo. También ofrece la opción de realizar aportaciones extraordinarias para ver cómo afectan al saldo pendiente y a la duración del préstamo.

## Requisitos

- Python 3.x
- Paquetes listados en `requirements.txt`

## Instalación

1. Clona este repositorio o descarga los archivos.
2. Navega hasta el directorio del proyecto.
3. Instala las dependencias utilizando `pip`:

   ```sh
   pip install -r requirements.txt
   ```

## Uso

Ejecuta el script principal:

```sh
python main.py
```

Sigue las instrucciones en la terminal para ingresar la información del préstamo.

### Ejemplo de Uso

1. Introduce la cuantía base del préstamo.
2. Introduce el tipo de interés anual (%). Si no existen intereses, introduce cero.
3. Introduce la comisión de apertura (cantidad fija).
4. Introduce el valor de cada cuota.
5. Introduce la fecha de inicio del préstamo (formato DD/MM/AAAA).
6. El programa mostrará un resumen del préstamo, incluyendo el capital amortizado hasta la fecha, la cantidad restante por pagar y la fecha de finalización estimada.
7. Preguntará si deseas realizar una aportación extraordinaria. Si es así, introduce la cantidad. El programa actualizará el resumen con la nueva información.

### Estructura del Proyecto

- `main.py`: Archivo principal que contiene el código de la calculadora de préstamos.
- `requirements.txt`: Lista de dependencias necesarias para ejecutar el proyecto.
- `README.md`: Este archivo, que contiene la descripción del proyecto y las instrucciones de uso.
