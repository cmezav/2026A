# atm.py
# Clase Atm con lógica de negocio pura (sin input())
# Sigue el mismo esquema de excepciones de BankAccount (Ejercicio 3.2)

# ─── Excepciones personalizadas ─────────────────────────────────────────────
class SaldoInsuficienteError(Exception):
    """Se lanza cuando se intenta retirar más del saldo disponible."""
    pass

class MontoInvalidoError(Exception):
    """Se lanza cuando el monto es cero, negativo o no cumple reglas de negocio."""
    pass


# ─── Clase principal ─────────────────────────────────────────────────────────
class Atm:
    RETIRO_MINIMO    = 20.0
    RETIRO_MAX_DIA   = 3000.0
    DEPOSITO_MINIMO  = 20.0
    DEPOSITO_MAX_DIA = 10000.0
    MULTIPLO         = 10.0

    def __init__(self, titular: str, saldo_inicial: float = 1000.0):
        if saldo_inicial < 0:
            raise MontoInvalidoError("El saldo inicial no puede ser negativo.")
        self.titular        = titular
        self._saldo         = saldo_inicial
        self._retirado_hoy  = 0.0
        self._depositado_hoy = 0.0

    # ── Propiedad de solo lectura ────────────────────────────────────────────
    @property
    def saldo(self) -> float:
        return self._saldo

    # ── Consultar saldo ──────────────────────────────────────────────────────
    def consultar_saldo(self) -> float:
        """Retorna el saldo actual sin modificar el estado."""
        return self._saldo

    # ── Depositar ────────────────────────────────────────────────────────────
    def depositar(self, monto: float) -> None:
        """
        Deposita 'monto' en la cuenta.
        Raises:
            MontoInvalidoError: si el monto es <= 0, menor al mínimo,
                                no múltiplo de 10, o supera el límite diario.
        """
        if monto <= 0:
            raise MontoInvalidoError(
                f"Monto inválido: {monto}. Debe ser mayor a cero.")
        if monto < self.DEPOSITO_MINIMO:
            raise MontoInvalidoError(
                f"Monto mínimo de depósito es S/{self.DEPOSITO_MINIMO}.")
        if monto % self.MULTIPLO != 0:
            raise MontoInvalidoError(
                f"Solo se permiten múltiplos de S/{self.MULTIPLO}.")
        if self._depositado_hoy + monto > self.DEPOSITO_MAX_DIA:
            disponible = self.DEPOSITO_MAX_DIA - self._depositado_hoy
            raise MontoInvalidoError(
                f"Supera el límite diario de depósito. "
                f"Puede depositar hasta S/{disponible} más hoy.")
        self._saldo          += monto
        self._depositado_hoy += monto

    # ── Retirar ──────────────────────────────────────────────────────────────
    def retirar(self, monto: float) -> None:
        """
        Retira 'monto' de la cuenta.
        Raises:
            MontoInvalidoError:      si el monto es <= 0, menor al mínimo,
                                     no múltiplo de 10, o supera el límite diario.
            SaldoInsuficienteError:  si el monto supera el saldo disponible.
        """
        if monto <= 0:
            raise MontoInvalidoError(
                f"Monto inválido: {monto}. Debe ser mayor a cero.")
        if monto < self.RETIRO_MINIMO:
            raise MontoInvalidoError(
                f"Monto mínimo de retiro es S/{self.RETIRO_MINIMO}.")
        if monto % self.MULTIPLO != 0:
            raise MontoInvalidoError(
                f"Solo se permiten múltiplos de S/{self.MULTIPLO}.")
        if monto > self._saldo:
            raise SaldoInsuficienteError(
                f"Saldo insuficiente: tiene S/{self._saldo:.2f}, "
                f"intenta retirar S/{monto}.")
        if self._retirado_hoy + monto > self.RETIRO_MAX_DIA:
            disponible = self.RETIRO_MAX_DIA - self._retirado_hoy
            raise MontoInvalidoError(
                f"Supera el límite diario de retiro. "
                f"Puede retirar hasta S/{disponible} más hoy.")
        self._saldo        -= monto
        self._retirado_hoy += monto