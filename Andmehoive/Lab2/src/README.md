# Labor 2 — skriptid

Siin on Labori 2 skriptid. Nüüd on anduri ja ADC vahel op-amp (LM358). Atom loeb kahte viiku korraga.

Skriptid on samad mis Laboris 1, muudetud on ainult seda, mis op-ampi jaoks vaja.

```text
andur -> op-amp -> Atom (controller.py) -> USB -> arvuti (pump_controller.py)
      -> log.csv (live_logger.py)
      -> pumba käsk (compressor_client.py) -> MG400 API -> pump
```

## Kuidas käivitada

1. Käivita MG400 baaspaketi API (`http://127.0.0.1:8000`).
2. Ühenda Atom USB-ga. Skriptis on port `COM5`.
3. **Enne Atomi külge panemist mõõda op-ampi väljund multimeetriga.** See ei tohi olla üle 3,3 V.
4. Mine kausta `src` ja käivita:

```bash
python pump_controller.py
```

5. Lõpeta **Esc** või **Ctrl+C**. Pump lülitub välja.
6. Logi tekib faili `src/log.csv` ja järgmine käivitus kirjutab selle üle. Tõsta logi kausta `../data/` kuupäevaga.

Vaja on Pythoni pakette: `pyserial`, `keyboard`, `numpy`, `matplotlib`.

---

## controller.py

**Kus töötab:** Atomi peal (MicroPython).

**Miks on vaja:** loeb korraga kahte pinget, et saaks võrrelda.

**Mida teeb:**
- loeb kahte ADC viiku: **GPIO25** ja **GPIO33**;
- iga **100 ms** saadab ühe rea kahe numbriga, näiteks `0.839 0.840`.

Erinevus Laborist 1: oli üks viik ja rida `0.839 V`, nüüd on kaks viiku ja ilma `V`-ta.

## pump_controller.py

**Kus töötab:** arvutis. See on põhiprogramm.

**Miks on vaja:** loeb Atomit, kirjutab logi ja lülitab pumpa.

**Mida teeb:** sama mis Laboris 1 (hüsterees 98 kPa → `suck`, alla 70 kPa → `off`, lõpus alati `off`).

Erinevus Laborist 1: loeb rea kahest numbrist ja kasutab **ainult esimest** (GPIO25). Rõhu valem on sama mis Laboris 1 (toore anduri valem).

## live_logger.py

**Kus töötab:** arvutis.

**Miks on vaja:** kirjutab mõõtmised faili `log.csv`.

Sama fail mis Laboris 1. Veerud: `time_ms, volts, pressure_kpa, compressor`.

## compressor_client.py

**Kus töötab:** arvutis.

**Miks on vaja:** saadab pumbale käsu (`suck` / `off`) MG400 API kaudu.

Sama fail mis Laboris 1. Käsitsi proovimine:

```bash
python compressor_client.py off
```

## plot_result.py

**Kus töötab:** arvutis, eraldi programm. Atomit ei ole vaja.

**Miks on vaja:** näitab, kuidas op-amp signaali muudab: sisend (andur) vs väljund (ADC).

**Mida teeb:**
1. Loeb faili `result.csv` (eraldaja `;`, veerud `analog` ja `real vool`).
   - `analog` — op-ampi väljund, mida ADC nägi, V;
   - `real vool` — anduri pinge, V.
2. Leiab punktid, kus väljund on lae vastu (küllastus, 3,148 V), ja jätab need sirge arvutamisest välja.
3. Arvutab sirge `y = k·x + b` ja R².
4. Joonistab graafiku ja salvestab `result.png`.

Praeguste andmetega: 60 punkti, neist 21 küllastuses, `k ≈ 5,24`, `b ≈ −1,27 V`.

```bash
python plot_result.py
```

## result.csv, result.xlsx, result.png

- `result.csv` — op-ampi mõõtmised, `plot_result.py` sisend;
- `result.xlsx` — samad andmed Excelis;
- `result.png` — `plot_result.py` tehtud graafik.
