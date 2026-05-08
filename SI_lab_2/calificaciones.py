def evaluar_rendimiento(nota):
    """
    Evalua el rendimiento academico segun la nota recibida.

    Parametros:
        nota (int): Calificacion entera entre 0 y 20.

    Retorna:
        str: "Insuficiente" (0-10), "Regular" (11-15) o "Excelente" (16-20)

    Lanza:
        ValueError: Si la nota no es valida o esta fuera del rango.
    """

    # Rechazar bool
    if isinstance(nota, bool):
        raise ValueError("No se permiten valores booleanos (True/False).")

    # Rechazar cualquier cosa que no sea int
    if not isinstance(nota, int):
        raise TypeError(
            f"Entrada invalida. Se esperaba un entero y se recibio: {type(nota).__name__}"
        )

    # Validar rango
    if nota < 0 or nota > 20:
        raise ValueError(
            f"La nota debe estar entre 0 y 20. Se recibio: {nota}"
        )

    # Evaluacion
    if nota <= 10:
        return "Insuficiente"
    elif nota <= 15:
        return "Regular"
    else:
        return "Excelente"


# ==========================
# PROGRAMA PRINCIPAL
# ==========================

print("=== SISTEMA DE EVALUACION ACADEMICA ===")
print("Ingrese notas entre 0 y 20.")
print("Escriba 'salir' para terminar.\n")

while True:

    entrada = input("Ingrese una nota: ").strip()

    # Opcion para terminar
    if entrada.lower() == "salir":
        print("\nPrograma finalizado.")
        break

    try:

        # Rechazar vacios
        if entrada == "":
            raise ValueError("No se permiten entradas vacias.")

        # Rechazar alfanumericos
        if entrada.isalnum() and not entrada.isdigit():
            raise ValueError(
                "No se permiten valores alfanumericos."
            )

        # Rechazar simbolos especiales
        if not entrada.lstrip("-").isdigit():
            raise ValueError(
                "Solo se permiten numeros enteros."
            )

        # Convertir a entero
        nota = int(entrada)

        # Evaluar
        resultado = evaluar_rendimiento(nota)

        print(f"Resultado: {resultado}\n")

    except TypeError as e:
        print(f"Error de tipo: {e}\n")

    except ValueError as e:
        print(f"Error de validacion: {e}\n")

    except Exception as e:
        print(f"Ocurrio un error inesperado: {e}\n")