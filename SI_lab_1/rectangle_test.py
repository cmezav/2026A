# rectangle_test.py
import unittest
from SI_lab_1.rectangle import calcular_area

class TestAreaRectangulo(unittest.TestCase):

    def test_area_valores_enteros(self):
        # Caso 1: Enteros positivos
        self.assertEqual(calcular_area(5, 10), 50)
        self.assertEqual(calcular_area(1, 1), 1)

    def test_area_valores_decimales(self):
        # Caso 2: Decimales positivos
        self.assertAlmostEqual(calcular_area(2.5, 4.0), 10.0)
        self.assertAlmostEqual(calcular_area(3.3, 2.2), 7.26)

    def test_area_valores_mixtos(self):
        # Caso 3: Combinación de entero y decimal
        self.assertAlmostEqual(calcular_area(3, 4.5), 13.5)

    def test_valores_cero_o_negativos(self):
        # Caso 4: Excepciones esperadas para valores inválidos
        with self.assertRaises(ValueError):
            calcular_area(0, 10)
        with self.assertRaises(ValueError):
            calcular_area(5, -2)
        with self.assertRaises(ValueError):
            calcular_area(-3, -4)

if __name__ == '__main__':
    unittest.main()
