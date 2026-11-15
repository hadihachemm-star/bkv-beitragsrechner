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
        return round(self.lohnerhoehung_jahr_gesamt - self.jahr_gesamt, 2)


def berechne(
    mitarbeiter: int,
    budget: int,
    ag_nebenkosten: float = AG_NEBENKOSTEN_STANDARD,
    andere_sachbezuege: float = 0.0,
) -> Ergebnis:
    """Berechnet die Arbeitgeberkosten fuer einen Budgettarif."""
    if mitarbeiter < 1:
        raise ValueError("Es wird mindestens ein Mitarbeiter benoetigt.")
    if budget not in BEISPIELTARIFE:
        stufen = ", ".join(str(b) for b in sorted(BEISPIELTARIFE))
        raise ValueError(f"Unbekannte Budgetstufe {budget}. Moeglich: {stufen}")
    if not 0 <= ag_nebenkosten < 1:
        raise ValueError("ag_nebenkosten muss zwischen 0 und 1 liegen.")
    if andere_sachbezuege < 0:
        raise ValueError("andere_sachbezuege darf nicht negativ sein.")

    beitrag = BEISPIELTARIFE[budget]
    monat = round(beitrag * mitarbeiter, 2)
    jahr = round(monat * 12, 2)
    lohn = round(jahr * (1 + ag_nebenkosten), 2)
    frei = beitrag + andere_sachbezuege <= SACHBEZUGSFREIGRENZE
    return Ergebnis(mitarbeiter, budget, beitrag, monat, jahr, frei, lohn)


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
    p.add_argument("--ag-nebenkosten", type=float, default=AG_NEBENKOSTEN_STANDARD,
                   help="Arbeitgeberanteil Sozialversicherung, z. B. 0.21")
    p.add_argument("--andere-sachbezuege", type=float, default=0.0,
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
