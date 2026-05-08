
SALDO_INICIAL       = 1000.0
RETIRO_MINIMO       = 20
RETIRO_MAX_DIA      = 3000
DEPOSITO_MINIMO     = 20
DEPOSITO_MAX_DIA    = 10000
MULTIPLO            = 10


def validar_monto_entero(texto):
    """
    Intenta convertir 'texto' a entero estricto.
    Rechaza decimales, letras y símbolos.
    Retorna (True, valor_int) o (False, mensaje_error).
    """
    texto = texto.strip()
    if not texto:
        return False, "Error: No ingresó ningún valor."
    # Rechazar punto decimal o coma
    if "." in texto or "," in texto:
        return False, "Error: Solo se aceptan números enteros, sin decimales."
    try:
        valor = int(texto)
    except ValueError:
        return False, "Error: Solo se aceptan números enteros (sin letras ni símbolos)."
    return True, valor


def validar_retiro(monto, saldo_actual, retirado_hoy):
    """
    Valida las reglas de negocio para un retiro.
    Retorna (True, None) si es válido, o (False, mensaje) si no.
    """
    if monto <= 0:
        return False, "Error: El monto debe ser mayor a cero."
    if monto < RETIRO_MINIMO:
        return False, f"Error: El monto mínimo de retiro es S/{RETIRO_MINIMO}."
    if monto % MULTIPLO != 0:
        return False, f"Error: Solo se permiten múltiplos de S/{MULTIPLO} (ej: 20, 30, 50, 100...)."
    if monto > saldo_actual:
        return False, f"Error: Saldo insuficiente. Su saldo disponible es S/{saldo_actual:.2f}."
    if retirado_hoy + monto > RETIRO_MAX_DIA:
        disponible = RETIRO_MAX_DIA - retirado_hoy
        return False, (f"Error: Supera el límite diario de retiro (S/{RETIRO_MAX_DIA}).\n"
                       f"       Puede retirar hasta S/{disponible} más hoy.")
    return True, None


def validar_deposito(monto, depositado_hoy):
    """
    Valida las reglas de negocio para un depósito.
    Retorna (True, None) si es válido, o (False, mensaje) si no.
    """
    if monto <= 0:
        return False, "Error: El monto debe ser mayor a cero."
    if monto < DEPOSITO_MINIMO:
        return False, f"Error: El monto mínimo de depósito es S/{DEPOSITO_MINIMO}."
    if monto % MULTIPLO != 0:
        return False, f"Error: Solo se permiten múltiplos de S/{MULTIPLO} (ej: 20, 50, 100, 500...)."
    if depositado_hoy + monto > DEPOSITO_MAX_DIA:
        disponible = DEPOSITO_MAX_DIA - depositado_hoy
        return False, (f"Error: Supera el límite diario de depósito (S/{DEPOSITO_MAX_DIA}).\n"
                       f"       Puede depositar hasta S/{disponible} más hoy.")
    return True, None


def mostrar_menu():
    print("\n" + "="*40)
    print("     CAJERO AUTOMÁTICO ATM")
    print("="*40)
    print("  1. Consultar Saldo")
    print("  2. Depositar Dinero")
    print("  3. Retirar Dinero")
    print("  4. Salir")
    print("="*40)


def main():
    saldo          = SALDO_INICIAL
    retirado_hoy   = 0.0
    depositado_hoy = 0.0

    print("\nBienvenido al Cajero ATM")

    while True:
        mostrar_menu()
        opcion_raw = input("Seleccione una opción: ").strip()

        # --- Validar que la opción sea un entero válido ---
        ok, resultado = validar_monto_entero(opcion_raw)
        if not ok: 
            print(resultado) 
            continue
        opcion = resultado

        # ── 1. Consultar Saldo ──────────────────────────
        if opcion == 1:
            print(f"\n  Saldo disponible: S/{saldo:.2f}")
            print(f"  Retirado hoy    : S/{retirado_hoy:.2f}  (límite S/{RETIRO_MAX_DIA})")
            print(f"  Depositado hoy  : S/{depositado_hoy:.2f}  (límite S/{DEPOSITO_MAX_DIA})")

        # ── 2. Depositar ────────────────────────────────
        elif opcion == 2:
            while True:
                monto_raw = input("  Ingrese el monto a depositar (S/): ").strip()
                ok, resultado = validar_monto_entero(monto_raw)
                if not ok:
                    print(f"  {resultado}  Intente nuevamente.")
                    continue
                monto = resultado
                ok, msg = validar_deposito(monto, depositado_hoy)
                if not ok:
                    print(f"  {msg}  Intente nuevamente.")
                    continue
                # Monto válido
                saldo          += monto
                depositado_hoy += monto
                print(f"  Depósito exitoso de S/{monto}.")
                print(f"  Nuevo saldo: S/{saldo:.2f}")
                break

        # ── 3. Retirar ──────────────────────────────────
        elif opcion == 3:
            while True:
                monto_raw = input("  Ingrese el monto a retirar (S/): ").strip()
                ok, resultado = validar_monto_entero(monto_raw)
                if not ok:
                    print(f"  {resultado}  Intente nuevamente.")
                    continue
                monto = resultado
                ok, msg = validar_retiro(monto, saldo, retirado_hoy)
                if not ok:
                    print(f"  {msg}  Intente nuevamente.")
                    continue
                saldo        -= monto
                retirado_hoy += monto
                print(f"  Retiro exitoso de S/{monto}.")
                print(f"  Nuevo saldo: S/{saldo:.2f}")
                break

        # ── 4. Salir ────────────────────────────────────
        elif opcion == 4:
            print("\n  Gracias por usar el Cajero ATM. ¡Hasta pronto!")
            break

        # ── Opción fuera de rango ───────────────────────
        else:
            print("  Error: Opción inválida. Ingrese un número del 1 al 4.")


if __name__ == "__main__":
    main()