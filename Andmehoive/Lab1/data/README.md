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

**Tähelepanu:** logid on 10 Hz, sest `controller.py` ootab iga rea vahel 100 ms. Ülesanne küsib 100 Hz.
