import unittest
from agente import analizar, decidir_riesgo


class TestIntegracion(unittest.TestCase):
    def test_url_invalida(self):
        self.assertIn("error", analizar("javascript:alert(1)"))

    def test_url_valida_retorna_estructura(self):
        r = analizar("https://example.com", "Hola", False)
        self.assertIn("p_fraude", r)
        self.assertIn(r["nivel"], {"ALTO", "MEDIO", "BAJO", "NO VERIFICADO", "INSUFICIENTE"})

    def test_decision_alta(self):
        self.assertEqual(decidir_riesgo(0.9, {"R": None, "C": None})["nivel"], "ALTO")

    def test_decision_no_verificada(self):
        self.assertEqual(decidir_riesgo(0.1, {"R": None, "C": True})["nivel"], "NO VERIFICADO")


if __name__ == "__main__":
    unittest.main()
