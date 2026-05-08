import unittest # para definir las clases de prueba y los casos de prueba
from atm import validar_monto_entero, validar_retiro, validar_deposito

# CLASE 1 para validar que el monto ingresado es un int, no decimales, letras o simbolos
class TestValidarMontoEntero(unittest.TestCase):
    """Pruebas para la función validar_monto_entero"""

    # ── Entradas válidas ────────────────────────────────────────────────────
    def test_TC01_entrada_entera_positiva(self): 
        """TC-01: Número entero positivo normal"""
        ok, val = validar_monto_entero("500") # colocar un int positivo normal 
        self.assertTrue(ok) # verificar que se reconoce como válido
        self.assertEqual(val, 500) # verificar que el valor parseado es el esperado (500)

    def test_TC02_entrada_entera_grande(self):
        """TC-02: Número entero grande (límite superior)"""
        ok, val = validar_monto_entero("10000") 
        self.assertTrue(ok)
        self.assertEqual(val, 10000)

    def test_TC03_opcion_menu_valida(self):
        """TC-03: Dígito de opción de menú (1-4)"""
        for digito in ["1", "2", "3", "4"]:
            ok, val = validar_monto_entero(digito)
            self.assertTrue(ok, f"Debería aceptar '{digito}'")

    # ── Entradas con decimales ──────────────────────────────────────────────
    def test_TC04_decimal_con_punto(self):
        """TC-04: Valor con punto decimal → rechazado"""
        ok, msg = validar_monto_entero("100.50")
        self.assertFalse(ok)
        self.assertIn("decimal", msg.lower())

    def test_TC05_decimal_con_coma(self):
        """TC-05: Valor con coma decimal → rechazado"""
        ok, msg = validar_monto_entero("100,50")
        self.assertFalse(ok)
        self.assertIn("decimal", msg.lower())

    def test_TC06_solo_punto(self):
        """TC-06: Solo un punto → rechazado"""
        ok, msg = validar_monto_entero(".")
        self.assertFalse(ok)

    # ── Entradas con letras o símbolos ─────────────────────────────────────
    def test_TC07_letras_en_monto(self):
        """TC-07: Letras en el monto → rechazado"""
        ok, msg = validar_monto_entero("abc")
        self.assertFalse(ok)
        self.assertIn("enteros", msg.lower())

    def test_TC08_monto_alfanumerico(self):
        """TC-08: Combinación letra+número → rechazado"""
        ok, msg = validar_monto_entero("50a")
        self.assertFalse(ok)

    def test_TC09_simbolo_arroba(self):
        """TC-09: Símbolo @ → rechazado"""
        ok, msg = validar_monto_entero("@200")
        self.assertFalse(ok)

    def test_TC10_simbolo_slash(self):
        """TC-10: Símbolo S/ (sol peruano) → rechazado"""
        ok, msg = validar_monto_entero("S/200")
        self.assertFalse(ok)

    def test_TC11_espacios_internos(self):
        """TC-11: Espacios internos → rechazado"""
        ok, msg = validar_monto_entero("1 00")
        self.assertFalse(ok)

    # ── Entradas vacías ─────────────────────────────────────────────────────
    def test_TC12_cadena_vacia(self):
        """TC-12: Cadena vacía → rechazado"""
        ok, msg = validar_monto_entero("")
        self.assertFalse(ok)
        self.assertIn("ningún", msg.lower())

    def test_TC13_solo_espacios(self):
        """TC-13: Solo espacios en blanco → rechazado"""
        ok, msg = validar_monto_entero("   ")
        self.assertFalse(ok)

    # ── Valores negativos y cero ────────────────────────────────────────────
    def test_TC14_numero_negativo(self):
        """TC-14: Número negativo → se parsea pero las reglas de negocio lo rechazarán"""
        ok, val = validar_monto_entero("-100")
        self.assertTrue(ok)          # el parseo no falla; la lógica de negocio lo rechaza
        self.assertEqual(val, -100)

    def test_TC15_cero(self):
        """TC-15: Cero → se parsea; la lógica de negocio lo rechazará"""
        ok, val = validar_monto_entero("0")
        self.assertTrue(ok)
        self.assertEqual(val, 0)


class TestValidarRetiro(unittest.TestCase):
    """Pruebas para la función validar_retiro"""

    # ── Retiros válidos ─────────────────────────────────────────────────────
    def test_TC16_retiro_valido_minimo(self):
        """TC-16: Retiro exactamente del mínimo permitido (S/20)"""
        ok, msg = validar_retiro(20, 1000, 0)
        self.assertTrue(ok)
        self.assertIsNone(msg)

    def test_TC17_retiro_valido_tipico(self):
        """TC-17: Retiro típico (S/200) con saldo suficiente"""
        ok, msg = validar_retiro(200, 1000, 0)
        self.assertTrue(ok)

    def test_TC18_retiro_valido_multiplo_no_redondo(self):
        """TC-18: Retiro de S/30 (múltiplo de 10, no de 100)"""
        ok, msg = validar_retiro(30, 500, 0)
        self.assertTrue(ok)

    def test_TC19_retiro_exacto_saldo(self):
        """TC-19: Retirar exactamente todo el saldo disponible"""
        ok, msg = validar_retiro(1000, 1000, 0)
        self.assertTrue(ok)

    def test_TC20_retiro_maximo_diario(self):
        """TC-20: Retiro que alcanza exactamente el límite diario (S/3000)"""
        ok, msg = validar_retiro(3000, 5000, 0)
        self.assertTrue(ok)

    # ── Retiros inválidos: monto ────────────────────────────────────────────
    def test_TC21_retiro_cero(self):
        """TC-21: Retiro de S/0 → rechazado"""
        ok, msg = validar_retiro(0, 1000, 0)
        self.assertFalse(ok)
        self.assertIn("mayor a cero", msg)

    def test_TC22_retiro_negativo(self):
        """TC-22: Retiro negativo → rechazado"""
        ok, msg = validar_retiro(-50, 1000, 0)
        self.assertFalse(ok)

    def test_TC23_retiro_menor_minimo(self):
        """TC-23: Retiro de S/10 (menor que el mínimo S/20) → rechazado"""
        ok, msg = validar_retiro(10, 1000, 0)
        self.assertFalse(ok)
        self.assertIn("mínimo", msg)

    def test_TC24_retiro_no_multiplo_de_10(self):
        """TC-24: Retiro de S/25 (no múltiplo de 10) → rechazado"""
        ok, msg = validar_retiro(25, 1000, 0)
        self.assertFalse(ok)
        self.assertIn("múltiplos", msg)

    def test_TC25_retiro_no_multiplo_15(self):
        """TC-25: Retiro de S/15 (no múltiplo de 10) → rechazado"""
        ok, msg = validar_retiro(15, 1000, 0)
        self.assertFalse(ok)

    # ── Retiros inválidos: saldo insuficiente ───────────────────────────────
    def test_TC26_retiro_mayor_que_saldo(self):
        """TC-26: Retirar más de lo que hay en cuenta → rechazado"""
        ok, msg = validar_retiro(200, 100, 0)
        self.assertFalse(ok)
        self.assertIn("insuficiente", msg)

    def test_TC27_retiro_exactamente_uno_mas_del_saldo(self):
        """TC-27: Retirar saldo + S/10 → rechazado"""
        ok, msg = validar_retiro(1010, 1000, 0)
        self.assertFalse(ok)

    # ── Retiros inválidos: límite diario ────────────────────────────────────
    def test_TC28_supera_limite_diario(self):
        """TC-28: Ya se retiró S/3000 hoy, intento de retiro adicional → rechazado"""
        ok, msg = validar_retiro(20, 5000, 3000)
        self.assertFalse(ok)
        self.assertIn("límite diario", msg)

    def test_TC29_supera_limite_diario_parcialmente(self):
        """TC-29: Retirado S/2900, intento de S/200 supera el límite diario → rechazado"""
        ok, msg = validar_retiro(200, 5000, 2900)
        self.assertFalse(ok)
        self.assertIn("límite diario", msg)

    def test_TC30_justo_en_limite_diario_acumulado(self):
        """TC-30: Retirado S/2980 hoy, intento de S/20 → llega exacto al límite, válido"""
        ok, msg = validar_retiro(20, 5000, 2980)
        self.assertTrue(ok)

    # ── Combinaciones extremas ──────────────────────────────────────────────
    def test_TC31_saldo_cero_retiro_cualquiera(self):
        """TC-31: Saldo en S/0, cualquier retiro → rechazado por saldo insuficiente"""
        ok, msg = validar_retiro(20, 0, 0)
        self.assertFalse(ok)

    def test_TC32_retiro_S100_saldo_exacto(self):
        """TC-32: Retiro S/100 con saldo exacto S/100 → válido"""
        ok, msg = validar_retiro(100, 100, 0)
        self.assertTrue(ok)


class TestValidarDeposito(unittest.TestCase):
    """Pruebas para la función validar_deposito"""

    # ── Depósitos válidos ───────────────────────────────────────────────────
    def test_TC33_deposito_valido_minimo(self):
        """TC-33: Depósito exactamente del mínimo permitido (S/20)"""
        ok, msg = validar_deposito(20, 0)
        self.assertTrue(ok)
        self.assertIsNone(msg)

    def test_TC34_deposito_valido_tipico(self):
        """TC-34: Depósito típico S/500"""
        ok, msg = validar_deposito(500, 0)
        self.assertTrue(ok)

    def test_TC35_deposito_maximo_diario_exacto(self):
        """TC-35: Depósito que alcanza exactamente el límite diario (S/10000)"""
        ok, msg = validar_deposito(10000, 0)
        self.assertTrue(ok)

    def test_TC36_deposito_acumulado_en_limite(self):
        """TC-36: Depositado S/9980, depósito de S/20 → llega exacto al límite"""
        ok, msg = validar_deposito(20, 9980)
        self.assertTrue(ok)

    # ── Depósitos inválidos: monto ──────────────────────────────────────────
    def test_TC37_deposito_cero(self):
        """TC-37: Depósito de S/0 → rechazado"""
        ok, msg = validar_deposito(0, 0)
        self.assertFalse(ok)
        self.assertIn("mayor a cero", msg)

    def test_TC38_deposito_negativo(self):
        """TC-38: Depósito negativo → rechazado"""
        ok, msg = validar_deposito(-100, 0)
        self.assertFalse(ok)

    def test_TC39_deposito_menor_minimo(self):
        """TC-39: Depósito de S/10 (menor que S/20 mínimo) → rechazado"""
        ok, msg = validar_deposito(10, 0)
        self.assertFalse(ok)
        self.assertIn("mínimo", msg)

    def test_TC40_deposito_no_multiplo_10(self):
        """TC-40: Depósito de S/55 (no múltiplo de 10) → rechazado"""
        ok, msg = validar_deposito(55, 0)
        self.assertFalse(ok)
        self.assertIn("múltiplos", msg)

    def test_TC41_deposito_no_multiplo_25(self):
        """TC-41: Depósito de S/25 (no múltiplo de 10) → rechazado"""
        ok, msg = validar_deposito(25, 0)
        self.assertFalse(ok)

    # ── Depósitos inválidos: límite diario ──────────────────────────────────
    def test_TC42_supera_limite_diario(self):
        """TC-42: Ya depositado S/10000 hoy, intento adicional → rechazado"""
        ok, msg = validar_deposito(20, 10000)
        self.assertFalse(ok)
        self.assertIn("límite diario", msg)

    def test_TC43_supera_limite_diario_parcialmente(self):
        """TC-43: Depositado S/9900, intento de S/200 supera límite diario → rechazado"""
        ok, msg = validar_deposito(200, 9900)
        self.assertFalse(ok)

    def test_TC44_deposito_S1000_primer_operacion(self):
        """TC-44: Primer depósito del día de S/1000 → válido"""
        ok, msg = validar_deposito(1000, 0)
        self.assertTrue(ok)


if __name__ == "__main__":
    unittest.main(verbosity=2)