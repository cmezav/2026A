# test_atm.py
import pytest
from SI_lab_1.atm import Atm, SaldoInsuficienteError, MontoInvalidoError


# ════════════════════════════════════════════════════════════════════
# FIXTURE prepara el estado inicial para cada test
# ════════════════════════════════════════════════════════════════════
@pytest.fixture
def cajero():
    """Fixture: retorna un Atm con S/.1000 de saldo inicial."""
    return Atm(titular="Juan Quispe", saldo_inicial=1000.0)


# ════════════════════════════════════════════════════════════════════
# TC-01  Saldo inicial correcto
# ════════════════════════════════════════════════════════════════════
def test_TC01_saldo_inicial(cajero):
    # Arrange (hecho por el fixture)
    # Act
    saldo = cajero.consultar_saldo()
    # Assert
    assert saldo == 1000.0, f"Esperado 1000.0, obtuvo {saldo}"


# ════════════════════════════════════════════════════════════════════
# TC-02  Depósito válido
# ════════════════════════════════════════════════════════════════════
def test_TC02_deposito_valido(cajero):
    # Arrange
    monto = 500.0
    # Act
    cajero.depositar(monto)
    # Assert
    assert cajero.saldo == 1500.0


# ════════════════════════════════════════════════════════════════════
# TC-03  Retiro válido
# ════════════════════════════════════════════════════════════════════
def test_TC03_retiro_valido(cajero):
    # Arrange
    monto = 300.0
    # Act
    cajero.retirar(monto)
    # Assert
    assert cajero.saldo == 700.0


# ════════════════════════════════════════════════════════════════════
# TC-04  Retiro exacto al saldo disponible
# ════════════════════════════════════════════════════════════════════
def test_TC04_retiro_exacto_saldo(cajero):
    cajero.retirar(1000.0)
    assert cajero.saldo == 0.0


# ════════════════════════════════════════════════════════════════════
# TC-05  Retiro mayor al saldo → SaldoInsuficienteError
# ════════════════════════════════════════════════════════════════════
def test_TC05_retiro_mayor_saldo_lanza_excepcion(cajero):
    with pytest.raises(SaldoInsuficienteError):
        cajero.retirar(1010.0)


# ════════════════════════════════════════════════════════════════════
# TC-06  Depósito de monto negativo → MontoInvalidoError
# ════════════════════════════════════════════════════════════════════
def test_TC06_deposito_negativo_lanza_excepcion(cajero):
    with pytest.raises(MontoInvalidoError):
        cajero.depositar(-200.0)


# ════════════════════════════════════════════════════════════════════
# TC-07  Depósito de monto cero → MontoInvalidoError
# ════════════════════════════════════════════════════════════════════
def test_TC07_deposito_cero_lanza_excepcion(cajero):
    with pytest.raises(MontoInvalidoError):
        cajero.depositar(0)


# ════════════════════════════════════════════════════════════════════
# TC-08  Retiro de monto negativo → MontoInvalidoError
# ════════════════════════════════════════════════════════════════════
def test_TC08_retiro_negativo_lanza_excepcion(cajero):
    with pytest.raises(MontoInvalidoError):
        cajero.retirar(-50.0)


# ════════════════════════════════════════════════════════════════════
# TC-09  Saldo inicial negativo → MontoInvalidoError
# ════════════════════════════════════════════════════════════════════
def test_TC09_saldo_inicial_negativo_lanza_excepcion():
    with pytest.raises(MontoInvalidoError):
        Atm("Error", saldo_inicial=-500.0)


# ════════════════════════════════════════════════════════════════════
# TC-10  Múltiples depósitos acumulados (parametrize)
# ════════════════════════════════════════════════════════════════════
@pytest.mark.parametrize("montos, saldo_esperado", [
    ([100.0, 200.0, 300.0], 1600.0),   # 1000 + 600
    ([20.0,  30.0,  50.0],  1100.0),   # 1000 + 100
    ([500.0, 500.0],        2000.0),   # 1000 + 1000
])
def test_TC10_multiples_depositos(cajero, montos, saldo_esperado):
    # Act
    for m in montos:
        cajero.depositar(m)
    # Assert
    assert abs(cajero.saldo - saldo_esperado) < 0.001, (
        f"Esperado {saldo_esperado}, obtuvo {cajero.saldo}"
    )


# ════════════════════════════════════════════════════════════════════
# TC-11  Múltiples retiros acumulados (parametrize)
# ════════════════════════════════════════════════════════════════════
@pytest.mark.parametrize("montos, saldo_esperado", [
    ([100.0, 200.0, 300.0], 400.0),    # 1000 - 600
    ([20.0,  30.0,  50.0],  900.0),    # 1000 - 100
    ([500.0, 500.0],        0.0),      # 1000 - 1000
])
def test_TC11_multiples_retiros(cajero, montos, saldo_esperado):
    for m in montos:
        cajero.retirar(m)
    assert abs(cajero.saldo - saldo_esperado) < 0.001, (
        f"Esperado {saldo_esperado}, obtuvo {cajero.saldo}"
    )


# ════════════════════════════════════════════════════════════════════
# TC-12  Consulta de saldo no modifica el estado
# ════════════════════════════════════════════════════════════════════
def test_TC12_consultar_saldo_no_modifica_estado(cajero):
    # Act: consultar tres veces
    s1 = cajero.consultar_saldo()
    s2 = cajero.consultar_saldo()
    s3 = cajero.consultar_saldo()
    # Assert: todas iguales y saldo interno inalterado
    assert s1 == s2 == s3 == 1000.0
    assert cajero.saldo == 1000.0


# ════════════════════════════════════════════════════════════════════
# CASOS ADICIONALES
# ════════════════════════════════════════════════════════════════════

# TC-13  Retiro monto no múltiplo de 10 → MontoInvalidoError
def test_TC13_retiro_no_multiplo_lanza_excepcion(cajero):
    with pytest.raises(MontoInvalidoError):
        cajero.retirar(25.0)

# TC-14  Depósito monto no múltiplo de 10 → MontoInvalidoError
def test_TC14_deposito_no_multiplo_lanza_excepcion(cajero):
    with pytest.raises(MontoInvalidoError):
        cajero.depositar(55.0)

# TC-15  Retiro menor al mínimo (S/10) → MontoInvalidoError
def test_TC15_retiro_menor_minimo_lanza_excepcion(cajero):
    with pytest.raises(MontoInvalidoError):
        cajero.retirar(10.0)

# TC-16  Depósito menor al mínimo (S/10) → MontoInvalidoError
def test_TC16_deposito_menor_minimo_lanza_excepcion(cajero):
    with pytest.raises(MontoInvalidoError):
        cajero.depositar(10.0)