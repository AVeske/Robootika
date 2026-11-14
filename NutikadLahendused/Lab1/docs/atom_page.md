# Atomi leht — Labori 1 seaded ja testid

## Kontrollitud lahendus

24.10.2026 vaadati üle kohaliku kõrvalrepo `ESP32-Image-Server-Fork/atom-image-server` failid `include/index_html.h`, `src/main.cpp` ja `src/letter_sender.h`. Veebilehe HTML asub `include/`, mitte `src/` kaustas. [Projekti asukoht ja käivitamine](letter_writer.md).

AtomS3R teenindab lehte aadressil `http://192.168.4.1/`, kui telefon on Atomi SoftAP-võrgus. Captive portal suunab telefoni sellele lehele; telefoni teavitus võib nõuda avamist. Võrguga liitumine ei nõua internetti. Kui automaatset akent ei ilmu, saab aadressi käsitsi avada vea uurimiseks.

## Mis lehel praegu olemas on

| Lehe osa / nupp | Mida saab teha | Kuidas tulemus seadmesse jõuab |
|---|---|---|
| `Source`: `LOAD IMG`, `LOAD .PNG` | Valida telefonist või arvutist pilt. | Pilt avatakse kõigepealt brauseris; valimine üksi seda Atomile ei saada. |
| `Slot (edit / send target)` | Valida üks neljast pildipesast, lehel 1–4. | API kasutab pesade numbreid 0–3. |
| `Device Preview`, `Zoom`, `FIT`, `FILL`, `1:1` | Eelvaadata ja sättida 128 × 128 ekraanile minevat pilti. | Need on brauseri pildiseaded; seadmesse saadetakse tulemus nupuga `SEND → SLOT`. |
| `SEND → SLOT` | Saata ettevalmistatud pilt valitud pessa ja ekraanile. | `POST /frame?slot=N`, multipart-fail: 32768 baiti RGB565 big-endian andmeid. Pilt salvestatakse LittleFS-i. |
| `SHOW THIS SLOT ON DEVICE` | Kuvada juba salvestatud pesa pilt. | `GET /show?slot=N`; tühi pesa annab HTTP 404. |
| `SAVE PNG + DATA`, `EXPORT .DAT` | Salvestada pildi eksport brauserist arvutisse või telefoni. | Need pole Atomi seadete salvestusnupud. |
| `Button gestures`: short, long, double | Määrata valitud pesa nupužesti tegevuseks pesa 1–4, URL või teise seadme viide. | `SAVE GESTURES` saadab `POST /buttons`; seadistus salvestatakse LittleFS-i. `GET /buttons` loeb selle tagasi. |
| `Lab settings`: `TEST DISPLAY` | Kuvada Atomi ekraanil seadme võrgu-/IP olek. | `GET /test-display` kutsub `showStatus()` ja tagastab HTTP 200 tekstiga `Status shown on display`. |
| `Network` | Näha seadme nime ja leitud teisi seadmeid; lisada teise seadme viide žestiväljale. | `GET /state` ja `GET /peers`. |

### Nupužestide seos tähevalikuga

Žestide seadistus kuulub algsele pildiserverile. Labori tähevaliku loogika kasutab lühikest vajutust tähe valimiseks ja pikka vajutust saatmiseks; seetõttu ei saa lubada, et iga žestiväli muudab samal ajal ka tähevaliku käitumist. Füüsilise nupu tegelik tegevus tuleb valitud režiimis eraldi kontrollida.

Tähejaama käivitamine on kirjas [letter_writer.md](letter_writer.md).

## Kuidas olemasolevat lehte laboris kontrollida

| Katse | Sammud | Oodatav tulemus | Selle ülevaatuse seis |
|---|---|---|---|
| Captive portal | Ühenda telefon Atomi võrku; ava vajadusel võrgu sisselogimise teavitus. | Avaneb sama Atomi leht ilma aadressi trükkimata. | Varasem test kirjeldatud allpool; uut seadmekatset ei tehtud. |
| Ekraani test | Vajuta `TEST DISPLAY`. | Lehel on päringu tagasiside; ekraanil võrgu-/IP olek. | Koodis olemas; uus seadmekatse tegemata. |
| Pildi saatmine | Laadi pilt, vali pesa, säti eelvaade ja vajuta `SEND → SLOT`. | Pilt jõuab ekraanile ja valitud pessa. | Uus seadmekatse tegemata. |
| Pesa vahetamine | Saada kahele pesale erinevad pildid ja kasuta `SHOW THIS SLOT ON DEVICE`. | Ekraanil on valitud pesa pilt. | Uus seadmekatse tegemata. |
| Žestide salvestus | Salvesta žest, värskenda lehte ja kontrolli väärtust uuesti; testi sobivas režiimis nuppu. | Salvestus säilib ja tegelik nupukäitumine vastab režiimile. | Uus seadmekatse tegemata. |

Katse juurde lisa kuupäev, kasutatud püsivara commit, telefoni mudel, tulemus ning foto/video või logi asukoht. Püsivara koodikontrolli ei märgita riistvarakatseks. Ükski kirjeldus selles failis ei kinnita uute seadete lisamist või püsivara üleslaadimist.

## Varasem arenduskirjeldus

Allpool on säilitatud senised sissekanded. Need kirjeldavad arendusetappe, mitte kõiki praeguse versiooni funktsioone. Jaama tähtede joonistamise failide kirjeldus kuulub jaama, mitte Atomi veebiseadete teostusse.

### Captive portal ja display test

Lisatud AtomS3R SoftAP režiimile captive portal, et WiFi võrku ühendudes saaks telefon avada olemasoleva veebiliidese ilma, et kasutaja peaks käsitsi sisestama `192.168.4.1`.

Lisatud:

- `DNSServer`, mis vastab SoftAP režiimis kõikidele DNS päringutele Atomi enda IP-aadressiga.
- tundmatute HTTP päringute redirect tagasi Atomi veebiliidesele.
- veebilehele testnupp, millega saab kontrollida Atomi ekraani.
- HTTP endpoint `/test-display`, mis kutsub olemasolevat `showStatus()` funktsiooni ja kuvab ekraanil seadme hetkeoleku.

Captive portali test:

- telefonist eemaldati varasem salvestatud WiFi ühendus;
- ühenduti uuesti Atomi loodud `Framer` WiFi võrku;
- telefon tuvastas captive portali ja kuvati võrgu sisselogimise popup;
- popupi avamisel kuvati olemasolev image-serveri veebileht.

Display testi käik:

`TEST DISPLAY` nupp veebilehel  
→ `GET /test-display`  
→ ESP32 WebServer  
→ `handleTestDisplay()`  
→ `showStatus()`  
→ Atomi ekraanil kuvatakse WiFi/IP ja seadme olek.

Lisatud C++ komponendid:

- `DNSServer` objekt DNS päringute töötlemiseks.
- HTTP route `/test-display`.
- callback-funktsioon `handleTestDisplay()`, mis kasutab olemasolevat `showStatus()` funktsiooni.

Õpitud mõisted:

- DNS — Domain Name System: süsteem, mis seob domeeninimed IP-aadressidega.
- Captive portal: WiFi võrk, kus klient suunatakse ühendamisel kohalikule veebilehele.
- HTTP endpoint: konkreetne URL, mille kaudu käivitatakse serveris kindel funktsioon.
- Callback: funktsioon, mille server kutsub hiljem vastava sündmuse või päringu saabumisel.
- HTTP 302 redirect: vastus, mis suunab kliendi teisele URL-ile.

Tulemus:

- Atom loob WiFi võrgu.
- Telefon saab võrku ühenduda.
- Captive portal töötab.
- Olemasolev image-serveri veebileht avaneb captive portali kaudu.
- Veebilehe testnupp kuvab AtomS3R ekraanil seadme hetkeoleku.


### Tähe valimine AtomS3R nupuga

Lisatud eraldi `letter_selector` moodul valitud tähe oleku ja kuvamise jaoks.

Lisatud failid:

- `src/letter_selector.h` — mooduli avalik liides.
- `src/letter_selector.cpp` — valitud tähe olek, järgmise tähe valimine ja ekraanile kuvamine.

Starter-projektis oli juba olemas nupuvajutuse kestuse mõõtmine ning short-, long- ja double-press eristamine. Seda loogikat ei kirjutatud ümber.

Single short press käitumine muudeti:

`AtomS3R button`
→ starteri short-press tuvastus
→ `nextLetter()`
→ `showSelectedLetter()`
→ ekraanil kuvatakse järgmine täht.

Tähed liiguvad järjest:

`A → B → C → ... → Z → A`

Long press ja double press jäid selles etapis starter-projekti olemasoleva `runGesture()` loogika kasutada.

Tähe saatmist jaama selles etapis veel ei lisatud.

# Muudatused

Projektile lisati tähtede kirjutamise võimalus. API kaudu saadetud täht kontrollitakse, pannakse järjekorda ja joonistatakse robotiga. Järgmine täht paigutatakse eelmise kõrvale.

## Lisatud failid

- **`letters.py`** – sisaldab tähtede A, B, C, S, D, I, T, H ja E kujusid koordinaatidena. Iga täht koosneb ühest või mitmest joonest. `get_letter_strokes()` tagastab tähe jooned ja `get_letter_width()` arvutab laiuse järgmise tähe paigutamiseks. Tähtede kõrgus on 24 mm.

- **`letter_drawing.py`** – muudab tähe koordinaadid roboti tegevuste plaaniks. Iga joone alguses tõstetakse pliiats üles, liigutakse alguspunkti ja langetatakse pliiats. Seejärel läbitakse joone punktid ning tõstetakse pliiats uuesti üles.

- **`robot_writer.py`** – täidab joonistamisplaani roboti liikumisfunktsiooni kaudu. Teisendab tähe kohalikud koordinaadid roboti koordinaatideks ning määrab pliiatsi kõrguse. Liikumised ootavad sihtpunkti jõudmist; ebaõnnestunud liikumine katkestab plaani veaga. Lisatud on tähtede paigutamise nihe, täpsemad liikumistolerantsid ja 0,2-sekundilised pausid pliiatsi tõstmisel ning langetamisel.

- **`letter_api.py`** – lisab POST `/api/letter` päringu, mille sisend on näiteks `{"letter": "A"}`. Kontrollib, et saadetud oleks üks toetatud täht, ja teisendab selle suurtäheks. Sobiv täht lisatakse järjekorda ning tagastatakse HTTP 202 koos järjekorra infoga. Vigane sisend annab HTTP 400.

- **`letter_queue.py`** – haldab tähtede kirjutamise järjekorda eraldi taustalõimes. Tähed kirjutatakse ükshaaval saabumise järjekorras, mistõttu API ei pea ootama kirjutamise lõppu. Pärast edukat kirjutamist nihutatakse järgmise tähe alguspunkti tähe laiuse ja 5 mm vahe võrra. Kirjutamisvead väljastatakse konsooli.

## Muudetud olemasolevad failid

- **`server.py`** – loob kirjutamisjärjekorra ja ühendab tähtede API olemasoleva `move_to()` funktsiooniga.
- **`limits.py`** – vaikimisi Z-alampiir muudeti −72 mm pealt −140 mm peale.

Roboti alguspunkt, pliiatsi kõrgused ja liikumise kvaliteet vajavad kontrollimist päris seadmel. API vastus kinnitab tähe järjekorda lisamist, mitte kirjutamise õnnestumist.
