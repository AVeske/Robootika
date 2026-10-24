# Labor 1 — skriptid

Siin on Labori 1 skriptid. Andur (MPX5700AP) on otse Atomi ADC viigu küljes, vahel ei ole midagi.

Kuidas asjad liiguvad:

```text
andur -> Atom (controller.py) -> USB -> arvuti (pump_controller.py)
      -> log.csv (live_logger.py)
      -> pumba käsk (compressor_client.py) -> MG400 API -> pump
```

## Kuidas käivitada

1. Käivita MG400 baaspaketi API ([KKallas/mg400-base](https://github.com/KKallas/mg400-base)). See peab töötama aadressil `http://127.0.0.1:8000`.
2. Ühenda Atom USB-ga. Vaata, mis COM port tal on. Skriptis on `COM5`.
3. Mine kausta `src` ja käivita:

```bash
python pump_controller.py
```

4. Lõpeta **Esc** või **Ctrl+C** klahviga. Pump lülitub välja.
5. Logi tekib faili `src/log.csv`. Iga uus käivitus kirjutab selle üle. Tõsta logi pärast kausta `../data/` ja pane nimesse kuupäev.

Vaja on Pythoni pakette: `pyserial` ja `keyboard`.

---

## controller.py

**Kus töötab:** Atomi peal (MicroPython).

**Miks on vaja:** Atom loeb anduri pinget ja saadab selle arvutisse.

**Mida teeb:**
- loeb ADC viiku **GPIO25** (sumbuvus 11 dB, ehk umbes 0–3,3 V);
- iga **100 ms** saadab ühe rea, näiteks `0.839 V`.

Seda faili ei pea käsitsi Atomile panema. `pump_controller.py` saadab selle ise.

## pump_controller.py

**Kus töötab:** arvutis. See on põhiprogramm.

**Miks on vaja:** see paneb kõik kokku: loeb Atomit, arvutab rõhu, kirjutab logi ja lülitab pumpa.

**Mida teeb:**
1. Avab pordi `COM5`, kiirus 115200.
2. Peatab Atomil vana programmi ja saadab sinna `controller.py`.
3. Loeb Atomist pinge ja arvutab rõhu andmelehe valemiga:
   `P = (V / 5,0 - 0,04) / 0,0012858` (kPa, absoluutne).
4. Kirjutab iga rea logisse (`live_logger.py`).
5. Otsustab pumba üle (hüsterees):
   - rõhk **≥ 98 kPa** (umbes atmosfäär) → pump imeb (`suck`);
   - rõhk **< 70 kPa** (vaakum on käes) → pump seisab (`off`);
   - nende vahel jääb vana olek.
6. Saadab käsu ainult siis, kui olek muutub.
7. Lõpus (Esc, Ctrl+C) saadab alati `off`.

## live_logger.py

**Kus töötab:** arvutis, `pump_controller.py` kasutab seda.

**Miks on vaja:** mõõtmised peavad jääma faili, et neid hiljem analüüsida.

**Mida teeb:**
- avab faili `log.csv` (vana sisu kustub!) ja kirjutab päise;
- funktsioon `write_log()` kirjutab ühe rea ja prindib selle ka ekraanile;
- iga rida läheb kohe kettale (`flush`), nii et kui programm katkeb, jääb logi alles.

Veerud: `time_ms, volts, pressure_kpa, compressor`.

## compressor_client.py

**Kus töötab:** arvutis.

**Miks on vaja:** see on ainus koht, mis räägib pumbaga.

**Mida teeb:**
- saadab HTTP POST päringu aadressile `http://127.0.0.1:8000/api/pump`, näiteks `{"mode": "suck"}` või `{"mode": "off"}`;
- kui API ei vasta, ei jookse programm kokku, vaid tagastab vea.

Pumpa saab proovida ka käsitsi:

```bash
python compressor_client.py off
```
