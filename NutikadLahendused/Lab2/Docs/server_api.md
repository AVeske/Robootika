# Server API

See dokument kirjeldab Nutilahenduste Labor 2 Flask serveri API endpoint'e ja nende kasutamist.

Server töötab postkontori põhimõttel:

1. Kasutaja saadab veebilehe kaudu töö serverisse.
2. Server hoiab töö ootel.
3. Atom küsib serverilt perioodiliselt uut tööd.
4. Kui töö on olemas, lubatud ja veel kehtiv, annab server selle Atomile.
5. Atom annab töö edasi jaamale.
6. Jaam täidab töö MG400 robotiga.
7. Atom saadab töö tulemuse serverile tagasi.
8. Veebileht küsib serverilt roboti ja viimase töö staatust.

Server ei algata ise ühendust Atomiga. Atom võtab serveriga ise ühendust.

---

## GET /

### Kasutaja

Veebibrauser.

### Eesmärk

Avab roboti juhtimise veebilehe.

### Vastus

Server tagastab:

`templates/index.html`

Veebilehe kaudu saab:

- näha roboti ONLINE / OFFLINE staatust;
- näha, millal Atom viimati serveriga ühendust võttis;
- valida lubatud töö;
- sisestada töö argumendi;
- saata töö serverisse;
- näha viimase töö staatust.

---

# POST /api/jobs

## Kasutaja

Veebileht / kasutaja.

## Eesmärk

Lisab serverisse uue töö.

Töö salvestatakse serverisse ja Atom saab selle järgmise pollimise käigus küsida.

## Request

HTTP method:

`POST`

Content-Type:

`application/json`

Näide:

```json
{
  "job": "letter",
  "arg": "A"
}
```

## Väljad

### job

Töö tüüp.

Praegu lubatud tööde nimekiri:

- `letter`
- `show_image`
- `move_test_piece`

### arg

Töö argument.

Näiteks `letter` töö puhul:

```json
{
  "job": "letter",
  "arg": "A"
}
```

`letter` töö puhul peab argument olema täpselt üks märk.

## Edukas vastus

Näide:

```json
{
  "job_id": 1,
  "status": "accepted"
}
```

HTTP status:

`201`

## Keelatud töö

Näide:

```json
{
  "job": "move_robot_10mm",
  "arg": "left"
}
```

Vastus:

```json
{
  "status": "refused",
  "reason": "Unknown or forbidden job"
}
```

HTTP status:

`400`

## Vale letter argument

Näiteks:

```json
{
  "job": "letter",
  "arg": "ABC"
}
```

Vastus:

```json
{
  "status": "refused",
  "reason": "Letter must be exactly one character"
}
```

HTTP status:

`400`

---

# POST /api/poll

## Kasutaja

Atom.

## Eesmärk

Atom kasutab seda endpoint'i perioodiliselt, et:

- anda serverile teada, et Atom on online;
- uuendada `last_seen` aega;
- saata serverile oma olek;
- küsida serverilt järgmist ootel tööd.

Server ise Atomiga ühendust ei alusta.

## Authentication

Atom peab saatma HTTP headeri:

`X-API-Key`

Näide:

```text
X-API-Key: <ATOM_API_KEY>
```

API key väärtus ei ole Git repos ega `app.py` failis.

Server loeb selle environment variable'ist:

```text
ATOM_API_KEY
```

## Request

HTTP method:

`POST`

Content-Type:

`application/json`

Näide:

```json
{
  "device": "team-atom",
  "robot": "ready"
}
```

Praeguses serveriversioonis kasutatakse poll päringut eelkõige Atomi online oleku ja töö küsimise jaoks.

## Vastus, kui töö on olemas

Näide:

```json
{
  "msg": 1,
  "job": "letter",
  "arg": "A"
}
```

### msg

Töö ID.

### job

Töö tüüp.

### arg

Töö argument.

## Vastus, kui tööd ei ole

```json
{
  "msg": null
}
```

## Vale API key

Kui `X-API-Key` puudub või on vale:

```json
{
  "error": "unauthorized"
}
```

HTTP status:

`401`

---

# Töö aegumine

Töö ei tohi jääda serverisse lõputult ootama.

Praegune töö kehtivusaeg on:

```text
30 sekundit
```

Serveris:

```text
JOB_TTL_SECONDS = 30
```

Kui Atom pollib pärast seda, kui töö on olnud serveris kauem kui 30 sekundit:

- töö staatuseks saab `expired`;
- tööd Atomile ei saadeta;
- robot ei hakka aegunud töö tõttu liikuma;
- `/api/poll` vastab:

```json
{
  "msg": null
}
```

See takistab olukorda, kus robot hakkaks pärast pikemat offline perioodi täitma vana käsku.

---

# POST /api/result

## Kasutaja

Atom.

## Eesmärk

Atom saadab serverile töö tulemuse pärast töö lõpetamist.

## Authentication

Vajalik HTTP header:

```text
X-API-Key: <ATOM_API_KEY>
```

## Request

HTTP method:

`POST`

Content-Type:

`application/json`

Näide:

```json
{
  "id": 1,
  "result": "done"
}
```

## Väljad

### id

Töö ID, mille Atom sai `/api/poll` vastusest.

### result

Töö tulemus.

Lubatud väärtused:

- `done`
- `refused`
- `error`

## Edukas vastus

```json
{
  "status": "ok"
}
```

## Tundmatu töö ID

Kui saadetud ID ei vasta viimasele serveris teadaolevale tööle:

```json
{
  "error": "Unknown job"
}
```

HTTP status:

`400`

## Vale result väärtus

Kui `result` ei ole üks järgmistest:

- `done`
- `refused`
- `error`

vastab server:

```json
{
  "error": "Invalid result"
}
```

HTTP status:

`400`

## Kui serveris pole ühtegi tööd

```json
{
  "error": "No job exists"
}
```

HTTP status:

`400`

---

# GET /api/status

## Kasutaja

Veebileht.

## Eesmärk

Veebileht küsib serverilt:

- kas Atom on ONLINE või OFFLINE;
- millal Atom viimati serveriga ühendust võttis;
- milline oli viimane töö;
- mis on viimase töö staatus.

## Request

HTTP method:

`GET`

Request body puudub.

## Näide vastusest

```json
{
  "robot_status": "ONLINE",
  "last_seen": "09:14:30",
  "last_job": {
    "id": 1,
    "job": "letter",
    "arg": "A",
    "status": "done"
  }
}
```

---

# ONLINE / OFFLINE loogika

Server salvestab iga `/api/poll` päringu ajal aja:

```text
last_seen
```

Praegune timeout:

```text
10 sekundit
```

Serveris:

```text
ONLINE_TIMEOUT_SECONDS = 10
```

Kui Atom on viimase 10 sekundi jooksul serverit pollinud:

```text
ONLINE
```

Kui viimasest pollist on möödas rohkem kui 10 sekundit:

```text
OFFLINE
```

Kui Atom pole pärast serveri käivitamist veel kordagi pollinud:

```text
OFFLINE
```

---

# Töö staatused

Töö võib serveris olla järgmistes staatustes.

## waiting

Töö on serverisse lisatud ja ootab, et Atom selle küsiks.

## sent

Atom küsis töö serverilt ja server andis selle välja.

## done

Robot täitis töö edukalt.

## refused

Töö tegemisest keelduti.

Näiteks robot ei olnud lubatud või töö täitmine ei olnud ohutu.

## error

Töö täitmisel tekkis viga.

## expired

Töö aegus enne, kui Atom selle serverilt küsis.

Aegunud tööd robotile ei saadeta.

---

# Lubatud tööde põhimõte

Serverist robotile saadetakse ainult eelnevalt defineeritud kõrgema taseme töid.

Näiteks lubatud töö:

```json
{
  "job": "letter",
  "arg": "A"
}
```

Server ei tohi saata robotile:

- koordinaate;
- otseseid liigutuskäske;
- kiiruse käske;
- käsku liikuda näiteks 10 mm vasakule;
- pumba otsest ON/OFF juhtimist.

Robotile saadetakse ainult selline töö, mille jaam oskab algusest lõpuni ise täita.

---

# Authentication

Atom kasutab serveriga suhtlemisel API key'd.

HTTP header:

```text
X-API-Key
```

Server loeb võtme environment variable'ist:

```text
ATOM_API_KEY
```

API key:

- ei ole `app.py` failis;
- ei ole Git repos;
- ei ole `server_api.md` failis;
- ei saadeta kasutajale veebilehel.

Näide lokaalsel Windows testimisel:

```powershell
$env:ATOM_API_KEY="SINU_VÕTI"
```

Pärast seda käivitatakse Flask samas terminalis:

```powershell
python app.py
```

---

# API kokkuvõte

| Method | Endpoint | Kasutaja | Eesmärk |
|---|---|---|---|
| GET | `/` | Brauser | Avab juhtimislehe |
| POST | `/api/jobs` | Veebileht | Lisab uue töö |
| POST | `/api/poll` | Atom | Uuendab olekut ja küsib töö |
| POST | `/api/result` | Atom | Saadab töö tulemuse |
| GET | `/api/status` | Veebileht | Küsib roboti ja töö staatust |

---

# Üldine andmevoog

```text
KASUTAJA / BRAUSER
        |
        | POST /api/jobs
        v
    FLASK SERVER
        |
        | töö jääb ootele
        |
        ^ POST /api/poll
        |
       ATOM
        |
        | töö
        v
       JAAM
        |
        v
      MG400
        |
        | tulemus
        v
       ATOM
        |
        | POST /api/result
        v
    FLASK SERVER
        |
        ^ GET /api/status
        |
KASUTAJA / BRAUSER
```

Server ei loo ise ühendust Atomi ega robotiga.

Atom võtab ise serveriga perioodiliselt ühendust.
```
