# Labor 2 — logid

Logid on tehtud skriptiga `../src/pump_controller.py`, op-amp on sees.

Veerud on samad mis Laboris 1: `time_ms, volts, pressure_kpa, compressor`.

## Failid

| Fail | Kuupäev | Ridu | Kestus | Sagedus | Pinge |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `log_2026-10-24.csv` | 24.10.2026 10:33 | 8594 | 862,9 s (~14 min) | 10 Hz | 0,146–3,148 V |

**Tähelepanu:**
- `volts` on GPIO25 ehk **op-ampi väljund**. Toores andur (GPIO33) logisse ei jõua.
- `pressure_kpa` on arvutatud toore anduri valemiga, aga sisend on op-ampi väljund. Seega see rõhk **ei ole õige** (näiteks 458 kPa). Õige rõhu jaoks on vaja op-ampi võimendust ja nihet.
- 3,148 V on ADC lagi (küllastus), umbes 6 % ridadest.

## Uus formaat (alates 24.10.2026)

See logi on tehtud vana skriptiga. Uued logid on 100 Hz ja veergudega `t_ms, config, adc, volts, p_kpa, pump`: iga mõõtmise kohta üks `raw` ja üks `opamp` rida. Vaata [`../src/README.md`](../src/README.md).
