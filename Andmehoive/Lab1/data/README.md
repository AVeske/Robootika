# Labor 1 — logid

Logid on tehtud skriptiga `../src/pump_controller.py`. Andur on otse ADC küljes (toores signaal).

Veerud:

| Veerg | Mis see on |
| :--- | :--- |
| `time_ms` | arvuti aeg, Unix millisekundites |
| `volts` | anduri pinge ADC viigul, V |
| `pressure_kpa` | rõhk, kPa **absoluutne** (atmosfäär ≈ 99 kPa) |
| `compressor` | pumba olek: `suck`, `off` või `None` (alguses) |

## Failid

| Fail | Kuupäev | Ridu | Kestus | Sagedus | Pinge |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `log_2026-10-03_1.csv` | 03.10.2026 12:24 | 397 | 39,7 s | 10 Hz | 0,474–0,852 V |
| `log_2026-10-03_2.csv` | 03.10.2026 12:41 | 271 | 27,0 s | 10 Hz | 0,517–0,858 V |

Mõlemas on näha imemine (`suck`) ja seis (`off`).

## Numbrid: `log_2026-10-03_1.csv`

Skript: vana `pump_controller.py`, riba 98 kPa sisse / 70 kPa välja (absoluutne). Arvutatud logist.

| Mis | Number |
| :--- | :--- |
| Ridu / kestus | 397 rida / 39,7 s |
| Samm ridade vahel | keskmiselt 100 ms (75–113 ms) → 10 Hz |
| Atmosfäär (esimene rida) | 99,4 kPa (0,839 V) |
| Väikseim rõhk | 42,6 kPa abs = −56,8 kPa atmosfääri suhtes |
| Käivitusi | 11 korda 39,7 s jooksul = **16,6 käivitust minutis** |
| Pumba tööaeg | 0,2–5,3 s, keskmiselt 1,4 s |
| Seisuaeg | 0,2–6,2 s, keskmiselt 2,2 s |
| Töötsükkel | ~40 % |
| Sisselülitus (rõhk enne `suck`) | 98,9–101,4 kPa abs |
| Väljalülitus (rõhk enne `off`) | 42,6–69,5 kPa abs |
| Pinge pumba töö ajal | ~0,749 V ≈ 85,5 kPa abs |
| Müra, pump seisab (25 rida, 0,573 V) | std 7,7 mV ≈ **9,6 LSB** ≈ 1,2 kPa |
| Müra, pump töötab (~0,749 V) | std 13,1 mV ≈ **16,2 LSB** |
| Üks ADC samm (arvutatud) | 3,3 V / 4096 = 0,81 mV → 0,81 / 6,43 mV/kPa ≈ **125 Pa** |

Mida see näitab:
- **Pump lühitsüklib**: 16,6 käivitust minutis, seisuaeg mõnikord ainult 0,2–0,4 s. Seisuaja alampiiri ei olnud.
- **Väljalülitus hüppab 42–70 kPa vahel**, kuigi piir on 70 kPa. Rõhk langeb ühe rea (100 ms) jooksul ~85 → ~50 kPa, 10 Hz on selleks liiga aeglane.
- **Rõhk tõuseb pärast väljalülitust tagasi atmosfääri** 0,2–6 s jooksul: haare lekib.
- Müra pumbaga on umbes 1,7 korda suurem kui ilma pumbata.

**Tähelepanu:** logid on 10 Hz, sest `controller.py` ootab iga rea vahel 100 ms. Ülesanne küsib 100 Hz.

## Uus formaat (alates 24.10.2026)

Need kaks vana logi on tehtud vana skriptiga. Uued logid on 100 Hz ja veergudega `t_ms, adc, volts, p_kpa, pump`, kus `p_kpa` on rõhk **atmosfääri suhtes** ja `pump` on 1/0. Vaata [`../src/README.md`](../src/README.md).

## Mõõtmised 24.10.2026 (100 Hz, napp robotil õhus)

Tehtud skriptiga `Lab2/src/pump_controller.py`, sest Atom loeb seal mõlemat viiku. Labori 1 andmed on read `config = raw` (GPIO33, andur otse ADC-s, vahel ei ole midagi). Analüüs: [`../notebooks/noise_analysis.py`](../notebooks/noise_analysis.py).

| Fail | Mis tehti | Napp | Pump |
| :--- | :--- | :--- | :--- |
| `l1_10s.csv` | logija kontroll, 10 s | õhus | seisab |
| `l1_noise_off.csv` | müra, 30 s | õhus | seisab |
| `l1_noise_on.csv` | müra, 30 s | õhus | töötab (käivitub 1 s pärast) |
| `l1_noise_servo_off.csv` | müra, servod välja, 30 s | õhus | seisab |

### Logija kontroll

| Mis | Number | Nõue |
| :--- | :--- | :--- |
| Ridu 10 s kohta | 998 rida 9,96 s jooksul = 100,2 Hz → **1002 rida / 10 s** | 1000 ± 5 ✅ |
| Pinge atmosfääris (ADC) | **0,818 V** | — |
| Pinge atmosfääris (multimeeter, Vout) | **0,833 V** | — |
| Vahe ADC vs multimeeter | 0,015 V = **1,8 %** (ADC näitab vähem) | ≤ 2 % ✅ |
| Atmosfäär | 0,818–0,819 V → **96,2 kPa abs** (andmelehe valem, toide 5,0 V) | `ATM_KPA = 96.2` skriptides |

Multimeetri järgi on atmosfäär 0,833 V → 98,5 kPa abs. Skriptid kasutavad ADC numbrit (96,2), sest pump otsustab ADC lugemi järgi ja nii on atmosfäär 0 kPa.

### Üks ADC samm

| Mis | Number |
| :--- | :--- |
| Mõõdetud (pinge vs ADC kood kõigist logidest) | 0,819 mV sammu kohta (ideaal 3,3 V / 4096 = 0,806 mV) |
| Anduri tundlikkus | 5 V · 0,0012858 = 6,43 mV/kPa |
| **Pa ühe ADC sammu kohta** | 0,819 / 6,43 ≈ **127 Pa** (arvutatud 125 Pa) |

### Müra

Pumbaga logist on võetud ainult read, kus pump töötab, ilma 2 s üleminekuta.

| Olukord | Ridu | Keskmine | Müra (std) | Müra kPa | Tipud spektris |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Pump seisab | 2795 | 0,819 V | **8,7 LSB** | 1,11 kPa | 0,6 Hz (aeglane triiv) |
| Pump töötab (napp õhus) | 2701 | 0,735 V (≈ −13 kPa) | **12,0 LSB** | 1,54 kPa | **19,5 Hz**, **39,1 Hz**, väike 10 Hz |
| Pump seisab, MG400 servod väljas | 2795 | 0,819 V | **8,7 LSB** | 1,10 kPa | 10 Hz |

Tipu kõrgus müra põhja (mediaani) suhtes:

| Sagedus | Pump seisab | Pump töötab | Servod väljas |
| :--- | :--- | :--- | :--- |
| 0,4 Hz | 5,8× | 2,6× | 4,4× |
| 10 Hz | 2,1× | 3,5× | 7,6× |
| 19,5 Hz | 1,0× | **86×** | 0,9× |
| 39,1 Hz | 0,6× | **12,6×** | 0,6× |
| 49,8 Hz | 0,4× | 0,8× | 1,6× |

Spekter: ![Labori 1 müra spekter](../Docs/l1_spectrum.png)

Tippude nimed:
- **19,5 Hz — pumba mootor.** Kontrollitud allika väljalülitamisega: pump seisab → tippu ei ole.
- **39,1 Hz — sama mootori 2. harmooniline** (2 × 19,5 Hz). Kaob koos pumbaga.
- **50 Hz (võrk) ei ole näha.** 100 Hz juures on 50 Hz täpselt Nyquisti sagedus, nii et see läheb spektri serva või 0 Hz peale. Selle nägemiseks on vaja suuremat sagedust või ostsilloskoobi FFT-d.
- **MG400 servod — mõõdetavat mõju ei ole.** Kontrollitud allika väljalülitamisega (`l1_noise_servo_off.csv`, Disable): müra 8,71 LSB servod väljas vs 8,69 LSB servod sees, ükski tipp ei kadunud.
- **10 Hz — allikas teadmata.** Ei ole pump ega servod: servod väljas oli ta isegi kõrgem (7,6× vs 2,1×). Kandidaat: USB / arvuti (logija prindib iga 10. rea ehk 10 korda sekundis). Kontrollimata.
- **0,4–0,6 Hz — aeglane triiv** (temperatuur, toide), mitte võnkumine.

**Kaks allikat on kontrollitud väljalülitamisega:** pumba mootor (tipp kaob) ja MG400 servod (muutust ei ole).

Võrdlus 03.10 logiga (10 Hz): siis 9,6 LSB pump seisab, 16,2 LSB pump töötab. Nüüd 100 Hz juures 8,7 ja 12,0 LSB.
