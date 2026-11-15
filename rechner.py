"""bKV-Beitragsrechner (Beispielprojekt).

Rechnet fuer einen Betrieb aus, was eine betriebliche Krankenversicherung
(bKV) mit Budgettarif pro Monat und Jahr kostet, und stellt das einer
gleich hohen Brutto-Gehaltserhoehung gegenueber.

Die Beitraege in BEISPIELTARIFE sind gerundete Beispielwerte, die sich an
der Spanne oeffentlich genannter Marktbeitraege orientieren (Stand 11/2026).
Sie sind kein Angebot und kein Tarif eines Versicherers.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from decimal import Context, Decimal, InvalidOperation, ROUND_HALF_EVEN, localcontext
from sys import float_info

# Jahresbudget je Mitarbeiter in Euro -> Beispiel-Monatsbeitrag in Euro
BEISPIELTARIFE: dict[int, float] = {
    300: 12.90,
    600: 24.90,
    900: 33.90,
    1200: 42.90,
    1500: 49.50,
}

# Monatliche Freigrenze fuer Sachbezuege (§ 8 Abs. 2 Satz 11 EStG).
# Vor Verwendung den aktuellen Stand pruefen.
SACHBEZUGSFREIGRENZE = 50.00

# Vereinfachte Annahme: Arbeitgeberanteil zur Sozialversicherung auf Bruttolohn.
AG_NEBENKOSTEN_STANDARD = 0.21
CENT = Decimal("0.01")


@dataclass(frozen=True)
class Ergebnis:
    mitarbeiter: int
    budget: int
    beitrag_je_ma: float
    monat_gesamt: float
    jahr_gesamt: float
    innerhalb_freigrenze: bool
    lohnerhoehung_jahr_gesamt: float

    @property
    def differenz_zur_lohnerhoehung(self) -> float:
        """Mehrkosten einer gleich hohen Brutto-Lohnerhoehung pro Jahr."""
        jahr = Decimal(f"{self.jahr_gesamt:.2f}")
        lohn = Decimal(f"{self.lohnerhoehung_jahr_gesamt:.2f}")
        with localcontext(Context(prec=float_info.max_10_exp + 4)):
            return float(lohn - jahr)


def _dezimal_argument(text: str) -> Decimal:
    try:
        return Decimal(text)
    except InvalidOperation as fehler:
        raise argparse.ArgumentTypeError("Ungueltige Dezimalzahl.") from fehler


def _dezimalzahl(wert: float | Decimal, feld: str) -> Decimal:
    if isinstance(wert, (int, float, Decimal)) and not isinstance(wert, bool):
        zahl = Decimal(str(wert)) if isinstance(wert, float) else Decimal(wert)
        if zahl.is_finite():
            return zahl
    raise ValueError(f"{feld} muss eine endliche Zahl sein.")


def _euro_float(betrag: Decimal) -> float:
    wert = float(betrag)
    if Decimal(f"{wert:.2f}") != betrag:
        raise ValueError("Der Betrag ist ausserhalb des darstellbaren Cent-Bereichs.")
    return wert


def berechne(
    mitarbeiter: int,
    budget: int,
    ag_nebenkosten: float | Decimal = AG_NEBENKOSTEN_STANDARD,
    andere_sachbezuege: float | Decimal = 0.0,
) -> Ergebnis:
    """Berechnet die Arbeitgeberkosten fuer einen Budgettarif."""
    if isinstance(mitarbeiter, bool) or not isinstance(mitarbeiter, int) or mitarbeiter < 1:
        raise ValueError("Die Mitarbeiterzahl muss eine positive Ganzzahl sein.")
    if isinstance(budget, bool) or not isinstance(budget, int) or budget not in BEISPIELTARIFE:
        stufen = ", ".join(str(b) for b in sorted(BEISPIELTARIFE))
        raise ValueError(f"Unbekannte Budgetstufe {budget}. Moeglich: {stufen}")
    if mitarbeiter > int(float_info.max):
        raise ValueError("Die Mitarbeiterzahl ist ausserhalb des darstellbaren Bereichs.")

    ag_satz = _dezimalzahl(ag_nebenkosten, "ag_nebenkosten")
    sachbezuege = _dezimalzahl(andere_sachbezuege, "andere_sachbezuege")
    if not 0 <= ag_satz < 1:
        raise ValueError("ag_nebenkosten muss zwischen 0 und 1 liegen.")
    if sachbezuege < 0:
        raise ValueError("andere_sachbezuege darf nicht negativ sein.")

    beitrag = Decimal(str(BEISPIELTARIFE[budget]))
    # Reserve enough significant digits for the count, tariff and rate.
    # A tiny rate may round away far below the cent without changing the result.
    praezision = len(str(mitarbeiter)) + len(ag_satz.as_tuple().digits) + 10
    with localcontext(Context(prec=max(28, praezision), rounding=ROUND_HALF_EVEN)):
        monat = beitrag * mitarbeiter
        jahr = monat * 12
        lohn = (jahr + jahr * ag_satz).quantize(CENT)
        frei = sachbezuege <= Decimal(str(SACHBEZUGSFREIGRENZE)) - beitrag
        # The derived difference must also survive the public float interface.
        _euro_float(lohn - jahr)
        return Ergebnis(mitarbeiter, budget, float(beitrag), _euro_float(monat),
                        _euro_float(jahr), frei, _euro_float(lohn))


def euro(wert: float) -> str:
    """Formatiert einen Betrag deutsch: 1.234,56 EUR."""
    text = f"{wert:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{text} EUR"


def bericht(e: Ergebnis) -> str:
    freigrenze = (
        "ja" if e.innerhalb_freigrenze else "nein - steuerliche Behandlung pruefen"
    )
    zeilen = [
        f"bKV-Budgettarif {e.budget} EUR Jahresbudget, {e.mitarbeiter} Mitarbeiter",
        f"  Beitrag je Mitarbeiter/Monat : {euro(e.beitrag_je_ma)}",
        f"  Arbeitgeberkosten/Monat      : {euro(e.monat_gesamt)}",
        f"  Arbeitgeberkosten/Jahr       : {euro(e.jahr_gesamt)}",
        f"  Innerhalb 50-EUR-Freigrenze  : {freigrenze}",
        f"  Gleich hohe Lohnerhoehung/Jahr (inkl. AG-Anteil): "
        f"{euro(e.lohnerhoehung_jahr_gesamt)}",
        f"  Mehrkosten der Lohnerhoehung : {euro(e.differenz_zur_lohnerhoehung)}",
        "",
        "Beispielwerte, kein Angebot, keine Steuer- oder Rechtsberatung.",
    ]
    return "\n".join(zeilen)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="bKV-Beitragsrechner (Beispielwerte)")
    p.add_argument("mitarbeiter", type=int, help="Anzahl versicherter Mitarbeiter")
    p.add_argument("budget", type=int, help="Jahresbudget je Mitarbeiter in EUR")
    p.add_argument("--ag-nebenkosten", type=_dezimal_argument, default=AG_NEBENKOSTEN_STANDARD,
                   help="Arbeitgeberanteil Sozialversicherung, z. B. 0.21")
    p.add_argument("--andere-sachbezuege", type=_dezimal_argument, default=0.0,
                   help="Weitere Sachbezuege je Mitarbeiter/Monat in EUR")
    a = p.parse_args(argv)
    try:
        e = berechne(a.mitarbeiter, a.budget, a.ag_nebenkosten, a.andere_sachbezuege)
    except ValueError as fehler:
        p.error(str(fehler))
    print(bericht(e))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
