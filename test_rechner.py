import unittest

from rechner import berechne, euro


class RechnerTest(unittest.TestCase):
    def test_kosten(self):
        e = berechne(25, 600)
        self.assertEqual(e.monat_gesamt, 622.50)
        self.assertEqual(e.jahr_gesamt, 7470.00)
        self.assertEqual(e.lohnerhoehung_jahr_gesamt, 9038.70)
        self.assertEqual(e.differenz_zur_lohnerhoehung, 1568.70)

    def test_freigrenze(self):
        self.assertTrue(berechne(10, 1500).innerhalb_freigrenze)
        self.assertFalse(
            berechne(10, 1500, andere_sachbezuege=10).innerhalb_freigrenze
        )

    def test_fehleingaben(self):
        with self.assertRaises(ValueError):
            berechne(0, 600)
        with self.assertRaises(ValueError):
            berechne(10, 700)

    def test_format(self):
        self.assertEqual(euro(5970), "5.970,00 EUR")


if __name__ == "__main__":
    unittest.main()
