# AGENTS.md — Labor 3

Juhend agendile/meeskonnakaaslasele, kes selles kaustas töötab.

- `src/` — Atomi püsivara (klapi impulss riistvarataimeriga, IRQ alarm) ja Pythoni logija.
- `data/` — `drops.csv`, `placement.csv`, `curves/` (rõhukõver tilga kohta), `plates/` (tilgaplaatide pildid).
- `notebooks/` — tilgad, dP/dt, filtrid, spektrid.
- `docs/` — skeem, `scope/` ostsilloskoobi pildid, `falstad/`, `recipe.md`, `latency.csv`, `pump_control.md`, `bom.md`.
- Midagi ei kustutata: vale number jääb, parandus tuleb alla.
- ISR-is ainult klapp kinni + lipp; kõik muu põhitsüklis.
- Atomi viik on 3,3 V — LM358 väljund ei lähe otse viiku.
