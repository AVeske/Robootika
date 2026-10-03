# 1. How to run the project!

## MG400 Setup

Tee all järgnevad läbi, et saada Repo endale lokaalsesse arvutisse ja valmispanna töö keskkond.
```bash
git clone https://github.com/AVeske/mg400-base-Fork.git
cd mg400-base
python3 -m venv .venv && source .venv/Scripts/activate
pip install -e .
```
Käivita server (meie oma ei vaja, et liigutaks z-floor allapoole `--z-floor -150`)
Vali üks kahest viisist, kudias jooksutada.
```bash
python -m mg400.server

mg400 serve
```
Profit - Server jookseb!


## AtomS3R Setup

Tõmbame alla järgneva Repo ja liigume vastavasse Image server kausta (kasutame Atom oma, sest meil on AtomS3R seade.) 

ÜHENDA ATOMS3R ENDA ARVUTI/JAAMA KÜLGE LÄBI USB KAABLI!
```bash
git clone https://github.com/AVeske/ESP32-Image-Server-Fork.git
cd ESP32-Image-Server/atom-image-server 
```

Kasutasime PlatformIO IDE VSCode'is, et ehitada (Build) ja üleslaaidda (Upload) Mikrokontrolleri kood meie AtomS3R peale.
- Ava projekt läbi PlatfromIO Extensioni (VSCode laiendus)
- Tekivad eraldi nupud VSCode alumisele ribale, et saaks `Build` ja `Upload` teha.
- Saab kasutada ka command line:
```bash
pio run -t upload
pio device monitor
```

# 2. Mis me päriselt ära tegime:

## AtomS3R koodis:
### Mis meil oli vaja:
1. Ühendamisel enda Access Point viskaks automaatselt valmis tehtud leheküljele
2. Lisada nupp leheküljele, et näidata võrgu andmeid Atomi enda ekraani peal
3. Saaks Atomi nupu vajutusega valida tähti
4. Nupu pikemalt allhoidmisega saadaks valitud tähe üle API tööjaama/sülearvutisse

### Kuidas lahendasime:
1. Access Point ühendamine oli juba olemas; Lisasime `main.cpp` faili DNSServeri, mis siis WiFi'sse ühendamisel suunab kohe "Sisselogimis" lehele. (Telefoni peal võib see mingi notification ette visata, selle peale vajutades avaneb see lehekülg)
2. Tegime lisa index_html-h faili, mis pani juurde `TEST DISPLAY` nupu, mis saadab siis olemasoleva reame võrgu info AtomS3R ekraanile.
3. Lõime uue faili `letter_selector.cpp` faili, mille abil saame nupu(Atomi ekraani) vajutusega läbi minna terve tähestiku A-Z
4. Lõime uue faili `letter_sender.cpp`, mis saab saata valitud tähe samas võrgus olevasse kuulavasse tööjaama.

### BONUS POINTS:
1. Kuna kooli poolt antud tööjaamadel ei ole WiFi võimekust, siis lisasime ka ühenduse, et saaks tähti saata üle COM PORTI.
2. Selle jaoks tuleb `letter_sender.h` teha valik, kas saadame tähe üle COM PORTi või üle WiFi.
3. Selle jaoks lisasime ka uue faili `letter_station.py`
4. COM PORT kasutamiseks tuleb eraldi käivitada eraldi lisatud pythoni file, mis saaks saata tööjaama. Tähtede valimine ja kõik muu toimub ikka Atomi pealt.
```bash 
python tools/letter_station.py --url http://localhost:8000/api/letter
```
4. Peale valiku tegemist tuleb uuesti `Build` ja `Upload` AtomS3R teha.

## MG400 koodis:
### Mis meil oli vaja:
1. Võtta täht vastu üle API
2. Valmis teha tähtede jaoks koordinaadid. Et robot teaks kuidas kirjutada.
3. Saata kättesaadud tähe koordinaadid robotile kirjutamiseks
4. Saata mitu tähte järjest, et see neid ükshaaval kirjutaks.
5. Leidma õige kõrguse, et robot saaks kirjutada

### Kuidas lahendasime:
1. Lõime uue API endpointi `letter_api.py`, mis kuulab `/api/letter`.
2. Tegime `letters.py` faili, kus on tähtede kirjutus kooridnaadid roboti jaoks.
3. Lõime faili `robot_writer.py` , mis kasutab ära olemasolevat `move_to` funktsiooni, et saata koordinaadid robotile ja panna ta päriselt liikuma.
4. Lõime faili `letter_queue.py`, et hoida tähti järjekorras seniks kuni eelmine kirjutab.
5. Katse eksitus meetod, et leida õige kõrgus, kus pastakas kirjutab ilma, et robot jookseks "Collision" Errorisse.

