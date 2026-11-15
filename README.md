# bKV-Beitragsrechner

[![Tests](https://github.com/hadihachemm-star/bkv-beitragsrechner/actions/workflows/tests.yml/badge.svg)](https://github.com/hadihachemm-star/bkv-beitragsrechner/actions/workflows/tests.yml)

Kleiner Rechner für die betriebliche Krankenversicherung (bKV) mit Budgettarif.
Er zeigt einem Betrieb in Sekunden, was eine bKV pro Monat und Jahr kostet und
wie sie im Vergleich zu einer gleich hohen Brutto-Gehaltserhöhung dasteht.

> **Hinweis:** Alle Beiträge in diesem Projekt sind gerundete Beispielwerte. Sie
> orientieren sich an der Spanne öffentlich genannter Marktbeiträge (Stand
> 11/2026), sind aber kein Angebot, kein Tarif eines Versicherers und keine
> Steuer- oder Rechtsberatung.

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
  Beitrag je Mitarbeiter/Monat : 24,90 EUR
  Arbeitgeberkosten/Monat      : 622,50 EUR
  Arbeitgeberkosten/Jahr       : 7.470,00 EUR
  Innerhalb 50-EUR-Freigrenze  : ja
  Gleich hohe Lohnerhoehung/Jahr (inkl. AG-Anteil): 9.038,70 EUR
  Mehrkosten der Lohnerhoehung : 1.568,70 EUR
```

Optionen:

| Option | Bedeutung | Standard |
|---|---|---|
| `--ag-nebenkosten` | Arbeitgeberanteil zur Sozialversicherung | `0.21` |
| `--andere-sachbezuege` | Weitere Sachbezüge je Mitarbeiter und Monat in Euro | `0` |

## Annahmen und Grenzen

- Budgetstufen und Beiträge stehen in `BEISPIELTARIFE` und sind Beispielwerte.
  Echte Beiträge unterscheiden sich je nach Versicherer, Tarif und Leistungsumfang.
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
