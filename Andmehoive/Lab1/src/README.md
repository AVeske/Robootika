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
2. Ühenda Atom USB-ga. Vaata, mis COM port tal on. Skriptis on `PORT = "COM5"`.
3. **Atmosfäär on faili alguses `ATM_KPA = 96.2` (kPa absoluutne).** Kontrolli seda: napp õhus, pump seisab, `p_kpa` peab olema umbes 0. Kui ei ole, muuda `ATM_KPA`.
4. Mine kausta `src` ja käivita:

```bash
python pump_controller.py suck
```

Puhumise jaoks:

```bash
python pump_controller.py blow
```

Ainult logi, pump ei käivitu kunagi (näiteks müra mõõtmiseks):

```bash
python pump_controller.py off
```

**Logi nimi:** pane viimaseks sõnaks faili nimi, näiteks `l1_noise_off.csv`. Siis ei pea logi ümber nimetama. Kui sellise nimega fail on juba olemas, programm ei kirjuta seda üle ja lõpeb.

**Automaatne lõpp:** `t=30` lõpetab 30 s pärast, `n=10` lõpetab pärast 10 pumba käivitust (kui 10. tsükkel on läbi ja pump seisab). Võib panna mõlemad, lõpp tuleb sellest, mis enne juhtub. Ilma nendeta töötab kuni `Esc`.

Näide: `python pump_controller.py suck t=60 l1_hold_glass.csv`

**Klahvid töö ajal:** `1` = imemine, `2` = puhumine, `0` = pump seisma (režiim `off`), `Esc` = lõpp.

Režiimis `off` ei saada programm pumbale ühtegi käsku, ka alguses ja lõpus mitte. Nii saab logida targa kasti või müra, ilma et programm pumpa segaks.

5. Lõpeta **Esc** või **Ctrl+C** klahviga. Pump lülitub välja.
6. Logi tekib faili `src/log.csv`. Iga uus käivitus kirjutab selle üle. Tõsta logi pärast kausta `../data/` ja pane nimesse kuupäev.

Vaja on Pythoni pakette: `pyserial` ja `keyboard`.

---

## controller.py

**Kus töötab:** Atomi peal (MicroPython).

**Miks on vaja:** Atom loeb anduri pinget ja saadab selle arvutisse.

**Mida teeb:**
- loeb ADC viiku **GPIO25** (sumbuvus 11 dB, ehk umbes 0–3,3 V);
- iga **10 ms** (100 Hz) saadab ühe rea: ADC kood (0–4095) ja pinge, näiteks `1043 0.839`.

Aeg on loetud taimeriga (`ticks`), nii et 10 s on 1000 rida.

Seda faili ei pea käsitsi Atomile panema. `pump_controller.py` saadab selle ise.

## pump_controller.py

**Kus töötab:** arvutis. See on põhiprogramm.

**Miks on vaja:** see paneb kõik kokku: loeb Atomit, arvutab rõhu, kirjutab logi ja lülitab pumpa.

**Mida teeb:**
1. Saadab Atomile `controller.py` ja paneb pumba alguses välja.
2. Arvutab rõhu andmelehe valemiga `P = (V / 5,0 - 0,04) / 0,0012858` ja lahutab atmosfääri `ATM_KPA` (96,2 kPa). Rõhk on **kPa atmosfääri suhtes**: imemine on miinus, puhumine pluss.
3. Otsustab pumba üle:
   - rõhk nõrgem kui `ON_KPA` (15 kPa) ja pump on seisnud vähemalt `MIN_OFF_S` (1 s) → pump käima;
   - rõhk jõudis `OFF_KPA`-ni (30 kPa) → pump seisma;
   - viimase minuti jooksul juba `MAX_STARTS_PER_MIN` (10) käivitust → pump ei käivitu;
   - rõhk üle `LIMIT_KPA` (130 kPa) → pump seisma.
4. **Kui Atomist ei tule 0,5 s jooksul rida → pump seisma.** Kui USB tõmmatakse välja, programm lõpeb ja pump lülitub välja.
5. Iga muutuse juures prindib põhjuse, näiteks `pump off - pressure reached`.
6. Lõpus (Esc, Ctrl+C) saadab alati `off`.

Numbrid on faili alguses. Need on esialgsed: muuda need targa kasti ja oma mõõtmiste järgi.

## live_logger.py

**Kus töötab:** arvutis, `pump_controller.py` kasutab seda.

**Miks on vaja:** mõõtmised peavad jääma faili, et neid hiljem analüüsida.

**Mida teeb:**
- avab faili `log.csv` (vana sisu kustub!) ja kirjutab päise;
- `write_log()` kirjutab ühe rea ja paneb selle kohe kettale;
- ekraanile prindib ainult iga 10. rea, sest 100 rida sekundis on liiga palju.

Veerud: `t_ms, adc, volts, p_kpa, pump`.
- `t_ms` — arvuti aeg, ms;
- `adc` — ADC kood 0–4095;
- `volts` — pinge, V (multimeetriga võrdlemiseks);
- `p_kpa` — rõhk atmosfääri suhtes, kPa;
- `pump` — 1 töötab, 0 seisab.

## compressor_client.py

**Kus töötab:** arvutis.

**Miks on vaja:** see on ainus koht, mis räägib pumbaga.

**Mida teeb:**
- saadab HTTP POST päringu aadressile `http://127.0.0.1:8000/api/pump`: `{"mode": "suck"}`, `{"mode": "blow"}` või `{"mode": "off"}`;
- kui API ei vasta, ei jookse programm kokku, vaid tagastab vea.

Pumpa saab proovida ka käsitsi:

```bash
python compressor_client.py off
```
