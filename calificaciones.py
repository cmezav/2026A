def evaluar_rendimiento(nota):
    """
    Evalua el rendimiento academico segun la nota recibida.

    Parametros:
        nota (int): Calificacion entera entre 0 y 20.

    Retorna:
        str: "Insuficiente" (0-10), "Regular" (11-15) o "Excelente" (16-20)

    Lanza:
        ValueError: Si la nota no es int puro, o esta fuera del rango 0-20.
    """
    # Validacion de tipo: bool es subclase de int, debe rechazarse
    if isinstance(nota, bool) or not isinstance(nota, int):
        raise ValueError(
            f"La nota debe ser un entero puro, se recibio: {type(nota).__name__!r}"
        )

    # Validacion de rango
    if nota < 0 or nota > 20:
        raise ValueError(
            f"La nota debe estar entre 0 y 20, se recibio: {nota}"
        )

    # Logica de evaluacion
    if nota <= 10:
        return "Insuficiente"
    elif nota <= 15:
        return "Regular"
    else:
        return "Excelente"