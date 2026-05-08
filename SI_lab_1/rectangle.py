
def calcular_area(base, altura):
    """
    Calcula el área de un rectángulo dadas su base y altura.
    Lanza un ValueError si los valores son menores o iguales a cero.
    """
    if base <= 0 or altura <= 0:
        raise ValueError("La base y la altura deben ser valores positivos mayores que cero.")
    return base * altura

def main():
    print("--- Calculadora de Área de Rectángulo ---")
    try:
        # Solicitamos los datos al usuario y los convertimos a float (permite enteros y decimales)
        base = float(input("Ingrese la base del rectángulo: "))
        altura = float(input("Ingrese la altura del rectángulo: "))
        
        # Calculamos el área
        area = calcular_area(base, altura)
        
        # Imprimimos el resultado de forma clara
        print("\n--- Resultado ---")
        print(f"Base ingresada: {base}")
        print(f"Altura ingresada: {altura}")
        print(f"Área calculada: {area}")
        
    except ValueError as e:
        print(f"\nError: Entrada inválida. {e}")

if __name__ == "__main__":
    main()
