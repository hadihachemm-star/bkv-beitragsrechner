from contextlib import redirect_stderr, redirect_stdout
from decimal import Decimal
from io import StringIO
import unittest

from rechner import berechne, euro, main


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

    def test_cent_rundung(self):
        for anzahl, satz, erwartete_kosten in [
            (3, 0.0125, 907.60),
            (1, 0.0625, 317.48),
        ]:
            with self.subTest(anzahl=anzahl, satz=satz):
                self.assertEqual(berechne(anzahl, 600, satz).lohnerhoehung_jahr_gesamt,
                                 erwartete_kosten)
        self.assertEqual(berechne(3, 600, 0.0125).differenz_zur_lohnerhoehung, 11.20)

    def test_freigrenze_exakt(self):
        self.assertTrue(berechne(1, 1500, andere_sachbezuege=0.50).innerhalb_freigrenze)
        for betrag in (0.51, Decimal("0.50000000000000000001")):
            with self.subTest(betrag=betrag):
                self.assertFalse(berechne(1, 1500, andere_sachbezuege=betrag).innerhalb_freigrenze)
        stdout = StringIO()
        with redirect_stdout(stdout):
            self.assertEqual(main(["1", "1500", "--andere-sachbezuege",
                                   "0.50000000000000000001"]), 0)
        self.assertIn("nein - steuerliche Behandlung pruefen", stdout.getvalue())

    def test_ungueltige_zahleneingaben(self):
        for anzahl, budget in ((1.5, 600), (True, 600), (2, 600.0), (10**306, 600)):
            with self.subTest(anzahl=anzahl, budget=budget), self.assertRaises(ValueError):
                berechne(anzahl, budget)
        for feld in ("ag_nebenkosten", "andere_sachbezuege"):
            for wert in (float("nan"), float("inf"), float("-inf")):
                with self.subTest(feld=feld, wert=wert), self.assertRaises(ValueError):
                    berechne(25, 600, **{feld: wert})

    def test_cli_ungueltige_betraege(self):
        for betrag in ("nan", "inf", "abc"):
            stdout, stderr = StringIO(), StringIO()
            with self.subTest(betrag=betrag), redirect_stdout(stdout), redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as fehler:
                    main(["25", "600", "--andere-sachbezuege", betrag])
                self.assertEqual(fehler.exception.code, 2)
                self.assertEqual(stdout.getvalue(), "")
                self.assertIn("error:", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
