"""
PRUEBAS ESCRITAS PRIMERO (TDD)
Archivo: test_calificaciones.py

Clases de equivalencia analizadas:
  VÁLIDAS:
    CE1: 0  <= nota <= 10  → "Insuficiente"
    CE2: 11 <= nota <= 15  → "Regular"
    CE3: 16 <= nota <= 20  → "Excelente"

  INVÁLIDAS:
    CEI1: nota < 0               → ValueError
    CEI2: nota > 20              → ValueError
    CEI3: tipo incorrecto        → ValueError
          (float, str, None, bool, list, etc.)
    CEI4: cadena con caracteres especiales / espacios → ValueError
    CEI5: cadena vacía           → ValueError
"""

import pytest
from calificaciones import evaluar_rendimiento


# ══════════════════════════════════════════════════════
# FASE RED — representantes de cada clase válida
# ══════════════════════════════════════════════════════

class TestClasesEquivalenciaValidas:

    def test_ce1_representante_5_insuficiente(self):
        assert evaluar_rendimiento(5) == "Insuficiente"

    def test_ce2_representante_13_regular(self):
        assert evaluar_rendimiento(13) == "Regular"

    def test_ce3_representante_18_excelente(self):
        assert evaluar_rendimiento(18) == "Excelente"


# ══════════════════════════════════════════════════════
# FASE REFACTOR — valores límite (Myers BVA)
# ══════════════════════════════════════════════════════

class TestValoresLimite:

    def test_limite_minimo_absoluto_0(self):
        assert evaluar_rendimiento(0) == "Insuficiente"

    def test_limite_1_sobre_minimo(self):
        assert evaluar_rendimiento(1) == "Insuficiente"

    def test_limite_ultimo_insuficiente_10(self):
        assert evaluar_rendimiento(10) == "Insuficiente"

    def test_limite_primer_regular_11(self):
        assert evaluar_rendimiento(11) == "Regular"

    def test_limite_ultimo_regular_15(self):
        assert evaluar_rendimiento(15) == "Regular"

    def test_limite_primer_excelente_16(self):
        assert evaluar_rendimiento(16) == "Excelente"

    def test_limite_maximo_absoluto_20(self):
        assert evaluar_rendimiento(20) == "Excelente"


# ══════════════════════════════════════════════════════
# CLASES INVÁLIDAS — fuera de rango
# ══════════════════════════════════════════════════════

class TestClasesEquivalenciaInvalidas_Rango:

    def test_cei1_negativo_menos1(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento(-1)

    def test_cei1_negativo_grande(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento(-100)

    def test_cei2_mayor20_valor21(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento(21)

    def test_cei2_mayor20_valor_grande(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento(999)

    def test_mensaje_error_menciona_valor(self):
        with pytest.raises(ValueError, match="25"):
            evaluar_rendimiento(25)


# ══════════════════════════════════════════════════════
# CLASES INVÁLIDAS — tipos incorrectos (CEI3)
# ══════════════════════════════════════════════════════

class TestClasesEquivalenciaInvalidas_Tipos:

    def test_cei3_float_decimal(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento(15.5)

    def test_cei3_float_entero_representado(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento(15.0)

    def test_cei3_none(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento(None)

    def test_cei3_lista_vacia(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento([])

    def test_cei3_diccionario(self): 
        with pytest.raises(ValueError):
            evaluar_rendimiento({}) 

    def test_cei3_bool_true(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento(True) 

    def test_cei3_bool_false(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento(False)


# ══════════════════════════════════════════════════════
# CLASES INVÁLIDAS — cadenas de texto (CEI4 / CEI5)
# ══════════════════════════════════════════════════════

class TestClasesEquivalenciaInvalidas_Strings:

    def test_cei4_cadena_numerica(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento("15")

    def test_cei4_cadena_letras(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento("quince")

    def test_cei4_cadena_con_espacios(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento("  15  ")

    def test_cei4_cadena_solo_espacio(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento("   ")

    def test_cei4_caracter_especial_arroba(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento("@15")

    def test_cei4_caracter_especial_signo_dolar(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento("$20")

    def test_cei4_caracter_especial_slash(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento("15/20")

    def test_cei4_caracter_especial_punto(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento("15.")

    def test_cei4_caracter_especial_guion(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento("-15")

    def test_cei4_caracter_especial_emoji(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento("a")

    def test_cei4_caracter_especial_tabulacion(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento("\t15")

    def test_cei4_caracter_especial_salto_linea(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento("\n15")

    def test_cei5_cadena_vacia(self):
        with pytest.raises(ValueError):
            evaluar_rendimiento("")


# ══════════════════════════════════════════════════════
# PRUEBAS PARAMETRIZADAS
# ══════════════════════════════════════════════════════

class TestParametrizados:

    @pytest.mark.parametrize("nota,esperado", [
        (0,  "Insuficiente"),
        (5,  "Insuficiente"),
        (10, "Insuficiente"),
        (11, "Regular"),
        (13, "Regular"),
        (15, "Regular"),
        (16, "Excelente"),
        (18, "Excelente"),
        (20, "Excelente"),
    ])
    def test_rangos_completos(self, nota, esperado):
        assert evaluar_rendimiento(nota) == esperado

    @pytest.mark.parametrize("nota_invalida", [
        -100, -1, 21, 30, 100,
        None, [], {},
        "", "  ", "\t", "\n",
        "15", "quince", "@", "$20", "abc",
    ])
    def test_toda_entrada_invalida_lanza_error(self, nota_invalida):
        with pytest.raises(ValueError):
            evaluar_rendimiento(nota_invalida)