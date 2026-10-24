# Labor 1 — analüüs

## noise_analysis.py

**Miks on vaja:** arvutab logidest numbrid, mida ülesanne küsib: logija sagedus, Pa ühe ADC sammu kohta, müra LSB-des ja kPa-des, spektri tipud.

**Mida teeb:**
1. Loeb `../data/l1_*.csv` failidest toore anduri read (`config = raw`).
2. Kontrollib `l1_10s.csv` põhjal, mitu rida tuleb 10 s kohta.
3. Arvutab ADC sammu suuruse (pinge vs ADC kood) ja sellest Pa ühe sammu kohta.
4. Arvutab müra (standardhälve) pump seisab / pump töötab. Pumba sisse- ja väljalülitamise järel 2 s jäetakse välja.
5. Teeb spektri (Welch, 100 Hz) ja salvestab pildi `../Docs/l1_spectrum.png`.

Vaja on pakette `numpy`, `scipy`, `matplotlib`.

```bash
python noise_analysis.py
```

Tulemused on kirjas failis [`../data/README.md`](../data/README.md).
