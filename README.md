# bKV-Beitragsrechner

Kleiner Rechner für die betriebliche Krankenversicherung (bKV) mit Budgettarif.
Er zeigt einem Betrieb in Sekunden, was eine bKV pro Monat und Jahr kostet und
wie sie im Vergleich zu einer gleich hohen Brutto-Gehaltserhöhung dasteht.

> **Hinweis:** Alle Beiträge in diesem Projekt sind frei erfundene Beispielwerte.
> Sie sind kein Angebot, kein Tarif eines Versicherers und keine Steuer- oder
> Rechtsberatung.

## Was der Rechner macht

- Arbeitgeberkosten pro Monat und Jahr für eine wählbare Budgetstufe
- Prüfung gegen die monatliche 50-Euro-Freigrenze für Sachbezüge
- Vergleich mit einer gleich hohen Lohnerhöhung inklusive Arbeitgeberanteil

## Benutzung

Benötigt nur Python 3.9 oder neuer, keine weiteren Pakete.

```bash
python rechner.py 25 600
```

```text
bKV-Budgettarif 600 EUR Jahresbudget, 25 Mitarbeiter
  Beitrag je Mitarbeiter/Monat : 19,90 EUR
  Arbeitgeberkosten/Monat      : 497,50 EUR
  Arbeitgeberkosten/Jahr       : 5.970,00 EUR
  Innerhalb 50-EUR-Freigrenze  : ja
  Gleich hohe Lohnerhoehung/Jahr (inkl. AG-Anteil): 7.223,70 EUR
  Mehrkosten der Lohnerhoehung : 1.253,70 EUR
```

Optionen:

| Option | Bedeutung | Standard |
|---|---|---|
| `--ag-nebenkosten` | Arbeitgeberanteil zur Sozialversicherung | `0.21` |
| `--andere-sachbezuege` | Weitere Sachbezüge je Mitarbeiter und Monat in Euro | `0` |

## Annahmen und Grenzen

- Budgetstufen und Beiträge stehen in `BEISPIELTARIFE` und sind erfunden.
- Der Lohnvergleich ist bewusst vereinfacht: Er rechnet nur den
  Arbeitgeberanteil auf den Bruttobetrag und betrachtet nicht, was beim
  Mitarbeiter netto ankommt.
- Die Freigrenze ist als Konstante hinterlegt; der aktuelle Stand ist vor
  Verwendung zu prüfen.

## Tests

```bash
python -m unittest
```

## Lizenz

MIT
