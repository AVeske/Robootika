# Pumba juhtimine — Labor 3

Laborite 1 ja 2 pumbajuhtimine: `../../Lab1/Docs/Dokumentatsioon.md`. Seal juhib Atom + Python pumbakasti MG400 DO liini kaudu ja pump hoiab napi vaakumi.

## Mis Laboris 3 muutus

Pump teeb nüüd ka teist tööd: **puhub süstlasse**. Tilga pikkust ei otsusta pump (tema käivitus ja seiskumine on aeglased ja ebatäpsed), vaid **solenoidklapp** süstla ees. Pump hoiab rõhku, klapp annab selle rõhu süstlale ainult impulsi ajaks.

```
pump ──► klapp port 3      port 2 ──┬──► süstal ──► otsik ──► tilk
              port 1 → õhku         └──► rõhuandur (MPX5700AP)
```

## Klapp

| | |
| :--- | :--- |
| Tüüp | 3/2 normaalselt suletud (3 porti) |
| Mähis | 24 V DC, silt 1 W; mõõdetud 0,037 A ≈ 0,89 W, ≈ 650 Ω |
| Kaitsediood | joodetud mähise klemmidele; valge-roheline juhe = +, roheline = − |
| Vooluta | pump kinni, süstal pordi 1 kaudu õhku → tilka ei tule |
| Vooluga | pump → süstal → tilk |

Vooluta olek on ohutu olek: kui Atom jookseb kokku, USB tõmmatakse välja või katkestus klapi kinni paneb, läheb süstal õhku ja vaik ei voola.

## Ahel

```
Atom G26 ── Grove ── Mini 3A Relay Unit (HK4100F, 5 V mähis)
BP 24 V + ──► COM (vasak)
NO (keskmine) ──► klapi + (valge-roheline)
klapi − (roheline) ──► BP 24 V −
NC (parem) — tühi
```

- Atomi 5 V ja klapi 24 V ahel on releega eraldatud. Ühine maa (BP − ↔ Atomi GND) ainult ostsilloskoobi mõõtmiseks.
- BP: 24,0 V, voolupiir 0,10 A.

## Ajastus (osa 1 mõõtmised)

| | Väärtus |
| :--- | :--- |
| Atom: impulss viigul | käsk + 0,09 ms, hajuvus ≤ 15 µs (`machine.Timer` ONE_SHOT) |
| Käsk → 24 V mähisel | ≈ 2,4 ms |
| Käsu lõpp → mähis 0 V | ≈ 2,9–3,1 ms |
| Pinge mähisel | ≈ käsk + 0,5 ms |
| Relee põrge | ≈ 0,4 ms ainult sisselülitusel |
| Mähise vool pärast väljalülitust | kustub dioodi kaudu, KAARDISTA ISE (saba pikkus, klapi mehaaniline sulgumine rõhukõveralt) |

## Rikked ja kaitse

- **Kinnine otsik / tühi süstal** → rõhukõver muutub (dP/dt); katkestus (IRQ) paneb klapi kohe kinni ja alarm jääb lukku, kuni see maha võetakse (osa 4).
- **Atom kokku / USB välja** → relee vabastab, klapp vooluta, süstal õhku.
- **Klapi juhtmed tagurpidi** → diood juhib, BP läheb voolupiiri (CC 0,1 A), midagi ei põle; klapp ei tööta.

KAARDISTA ISE: kas pumpa ennast tuleb ka L3-s DO kaudu juhtida (rõhu hoidmine süstla jaoks) ja millise rõhuga.
