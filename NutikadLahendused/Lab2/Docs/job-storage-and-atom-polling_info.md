# Tööde salvestamine ja Atomi suhtlus serveriga

### Hetkeseis: 04.10

Veebilehel sisestatud tööd saadetakse Flask serverisse päringuga:

`POST /api/jobs`

Praeguses lahenduses ei salvestata töid faili ega andmebaasi, vaid ainult serveri RAM-i. Selleks kasutatakse muutujaid:

```
current_job = None
last_job = None
```
Uue töö saabumisel loob server tööobjekti, näiteks:

```
job = {
    "id": 1,
    "job": "letter",
    "arg": "A",
    "status": "waiting",
    "created_at": datetime.now()
}
```
Seejärel salvestatakse see aktiivse tööna:

```
current_job = job
last_job = job
```
Andmevoog on seega:

`Veebileht → POST /api/jobs → Flask → current_job RAM-is`

Kuna andmed paiknevad ainult mälus, kaovad Flask serveri restardi korral aktiivne töö, eelmine töö, töö ID loendur ning seadme viimase ühenduse aeg. Praeguse labori jaoks on see piisav, kuna eesmärk on eelkõige demonstreerida veebilehe, serveri ja seadme vahelist suhtlust. Vajadusel saaks hiljem lisada püsiva salvestuse, näiteks SQLite andmebaasi.

### Atomi poolne tööde küsimine
Atom ei loe andmeid otse veebilehelt, vaid suhtleb Flask serveri API-ga.

Selleks kasutab Atom pollimist ehk saadab regulaarselt serverile päringu, et kontrollida, kas uus töö on saadaval.

Atom teeb umbes iga 1–2 sekundi järel päringu aadressile:

`POST https://narva1.roboarena.org/api/poll`

Päring sisaldab autentimiseks API võtit:

```
X-API-Key: <API-võti>
```
ning näiteks seadme olekut:

```
{
  "device": "team-atom",
  "robot": "ready"
}
```
Kui uut tööd ei ole, vastab server näiteks:

```
{
  "msg": null
}
```
Kui veebilehe kaudu on sisestatud uus töö, näiteks täht `A`, vastab server:

```
{
  "msg": 5,
  "job": "letter",
  "arg": "A"
}
```
Atom loeb vastusest välja töö tüübi ja argumendi ning annab saadud info edasi järgmisele süsteemiosale.

Üldine andmevoog on:

`Kasutaja veebilehel → Flask server → Atom → jaam → MG400`

Täpsemalt:

`POST /api/jobs` salvestab veebilehelt saadetud töö serverisse ning `POST /api/poll` kaudu küsib Atom serverilt regulaarselt, kas uus töö on saadaval.
