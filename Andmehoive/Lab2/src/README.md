# Labor 2 — skriptid

Siin on Labori 2 skriptid. Nüüd on anduri ja ADC vahel op-amp (LM358). Atom loeb kahte viiku korraga: toores andur ja op-ampi väljund. Nii on mõlemad signaalid samas logis.

Skriptid on samad mis Laboris 1, muudetud on ainult seda, mis op-ampi jaoks vaja.

```text
andur -> GPIO33 (toores) -------------------\
andur -> op-amp -> GPIO25 ------------------ Atom (controller.py) -> USB -> arvuti (pump_controller.py)
      -> log.csv (live_logger.py)
      -> pumba käsk (compressor_client.py) -> MG400 API -> pump
```

## Kuidas käivitada

1. Käivita MG400 baaspaketi API (`http://127.0.0.1:8000`).
2. Ühenda Atom USB-ga. Skriptis on `PORT = "COM5"`.
3. **Enne Atomi külge panemist mõõda op-ampi väljund multimeetriga.** See ei tohi olla üle 3,3 V.
4. **Atmosfäär on faili alguses `ATM_KPA = 96.2` (kPa absoluutne).** Kontrolli seda: napp õhus, pump seisab, `p_kpa` peab olema umbes 0. Kui ei ole, muuda `ATM_KPA`.
5. Mine kausta `src` ja käivita:

```bash
python pump_controller.py suck opamp
```

- esimene sõna: `suck` (imemine), `blow` (puhumine) või `off` (ainult logi, pump ei käivitu);
- sõna `raw` või `opamp`: millise signaali järgi pumpa juhitakse (vaikimisi `opamp`).

Logisse lähevad **alati mõlemad** signaalid, teine sõna muudab ainult juhtimist.

Näide: `python pump_controller.py off raw ../../Lab1/data/l1_noise_off.csv`

**Logi nimi:** pane viimaseks sõnaks faili nimi, näiteks `l1_noise_off.csv`. Siis ei pea logi ümber nimetama. Kui sellise nimega fail on juba olemas, programm ei kirjuta seda üle ja lõpeb.

**Automaatne lõpp:** `t=30` lõpetab 30 s pärast, `n=10` lõpetab pärast 10 pumba käivitust (kui 10. tsükkel on läbi ja pump seisab). Võib panna mõlemad, lõpp tuleb sellest, mis enne juhtub. Ilma nendeta töötab kuni `Esc`.

Näide: `python pump_controller.py suck raw t=60 ../../Lab1/data/l1_hold_glass.csv`

**Klahvid töö ajal:** `1` = imemine, `2` = puhumine, `0` = pump seisma (režiim `off`), `Esc` = lõpp.

Režiimis `off` ei saada programm pumbale ühtegi käsku, ka alguses ja lõpus mitte. Nii saab logida targa kasti või müra, ilma et programm pumpa segaks.

6. Lõpeta **Esc** või **Ctrl+C**. Pump lülitub välja.
7. Logi tekib faili `src/log.csv` ja järgmine käivitus kirjutab selle üle. Tõsta logi kausta `../data/` kuupäevaga.

Vaja on Pythoni pakette: `pyserial`, `keyboard`, `numpy`, `matplotlib`.

---

## controller.py

**Kus töötab:** Atomi peal (MicroPython).

**Miks on vaja:** loeb korraga kahte pinget, et saaks võrrelda.

**Mida teeb:**
- loeb kahte ADC viiku, mõlemal sumbuvus 11 dB (0–3,3 V):
  - **GPIO25** — op-ampi väljund;
  - **GPIO33** — toores andur (sama signaal mis Laboris 1);
- iga **10 ms** (100 Hz) saadab ühe rea: `adc25 V25 adc33 V33`, näiteks `3117 2.512 887 0.715`.

## pump_controller.py

**Kus töötab:** arvutis. See on põhiprogramm.

**Miks on vaja:** loeb Atomit, kirjutab logi ja lülitab pumpa.

**Mida teeb:** sama mis Laboris 1 (riba, seisuaja alampiir, käivituste piir, 0,5 s ilma andmeteta → pump seisma, lõpus alati `off`). Lisaks:
- arvutab rõhu mõlemast signaalist:
  - `raw`: anduri valem otse GPIO33 pingest;
  - `opamp`: kõigepealt anduri pinge tagasi `V_andur = (V_out - OFFSET) / GAIN`, siis sama valem;
- kirjutab iga mõõtmise kohta **kaks rida**: üks `raw`, üks `opamp`.

`GAIN` ja `OFFSET` on faili alguses (praegu 5,24 ja −1,27). **Need tuleb panna `plot_result.py` uue mõõtmise järgi** (`k` ja `b`), vana `result.csv` tehti siis, kui GPIO33 nägi ainult 0–1 V.

## live_logger.py

**Kus töötab:** arvutis.

**Miks on vaja:** kirjutab mõõtmised faili `log.csv`.

Veerud: `t_ms, config, adc, volts, p_kpa, pump`.
- `config` — `raw` (toores andur) või `opamp` (op-ampi väljund);
- `p_kpa` — rõhk atmosfääri suhtes, kPa;
- teised nagu Laboris 1.

Ekraanile prindib iga 10. mõõtmise kohta ühe `raw` ja ühe `opamp` rea.

## compressor_client.py

**Kus töötab:** arvutis.

**Miks on vaja:** saadab pumbale käsu (`suck` / `blow` / `off`) MG400 API kaudu.

Käsitsi proovimine:

```bash
python compressor_client.py off
```

## plot_result.py

**Kus töötab:** arvutis, eraldi programm. Atomit ei ole vaja.

**Miks on vaja:** näitab, kuidas op-amp signaali muudab: sisend (andur) vs väljund. Sealt tulevad `GAIN` ja `OFFSET`.

**Mida teeb:**
1. Loeb faili `result.csv` (eraldaja `;`, veerud `analog` ja `real vool`).
   - `analog` — op-ampi väljund, ADC GPIO25, V;
   - `real vool` — toores anduri pinge, ADC GPIO33, V.
   Mõlemad veerud on mõõdetud ADC-ga, mitte multimeetriga.
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

Uue `result.csv` saab logist: võta `log.csv`-st sama `t_ms`-iga `opamp` ja `raw` read ja pane nende `volts` kõrvuti.

## pick_web.py

**Kus töötab:** arvutis. Veebileht aadressil `http://127.0.0.1:8010`.

**Miks on vaja:** Labori 1 katse "robot võtab klaasi kümme korda". Robot viib napi klaasile, imeb, tõstab, viib teise kohta, puhub ja laseb lahti. Leht teeb seda ise ja kirjutab samal ajal logi (100 Hz, `raw` + `opamp`).

**Enne käivitamist:**
1. Ava MG400 leht (`http://127.0.0.1:8000`), ühenda ja luba robot (Connect, Enable).
2. Vii robot nii, et napp **puudutab klaasi** esimeses kohas, ja salvesta see **slot 1**. Teine koht (kuhu klaas läheb) → **slot 2**. Salvesta asend, kus napp puudutab klaasi, mitte õhus.
3. Klaas pane slot 1 kohale.

**Käivitamine** (kaustas `Lab2/src`):

```bash
python pick_web.py ../../Lab1/data/l1_pick_10x.csv
```

Ava brauseris `http://127.0.0.1:8010`.

**Nupud:**
- **STOP** — robot seisma (`/api/stop`) ja pump välja. Vajuta, kui midagi läheb valesti.
- **Imemine / Puhumine / Pump seis** — pump käsitsi.
- **Slot 1 kohale / Slot 2 kohale** — robot läheb `LIFT_MM` (40 mm) kõrgusele slotti kohale.
- **Auto: N haaret** — N tsüklit järjest.

**Üks tsükkel:**
1. slotti kohale 40 mm kõrgusele → alla klaasini;
2. imemine, kuni rõhk jõuab −30 kPa (kui 5 s jooksul ei jõua → stopp, "no grip");
3. tõstmine 40 mm, kontroll: rõhk peab olema alla −15 kPa (muidu → stopp, "glass lost");
4. teise slotti kohale → alla;
5. puhumine 0,5 s (üks impulss), pump välja → üles.

Paaritu tsükkel viib klaasi 1 → 2, paaris 2 → 1, nii et klaas käib edasi-tagasi.

Tabelis on iga tsükli kohta: mitu sekundit vaakum tuli, rõhk tõstes ja viies, tsükli aeg.

**Ohutus:**
- Esimene kord vaata, et robot liigub aeglaselt (MG400 lehel kiirus madal), käsi STOP nupu juures.
- Kui Atomist ei tule 0,5 s andmeid, pump läheb välja ja automaat peatub.
- Programmi lõpus (Ctrl+C) pump välja.
- Imemise ajal hoiab leht riba −15 / −30 kPa, aga seisuaja alampiiri ja käivituste piiri siin ei ole: leht on mõeldud jälgitud katseks.

Testitud simulaatoriga (vale Atom ja vale MG400 API): 10 / 10 tsüklit, STOP ja Atomi vaikimine töötavad. Päris robotiga ei ole veel proovitud.
