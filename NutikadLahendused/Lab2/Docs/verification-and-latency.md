# Postkontori kontroll ja latentsuse mõõtmine

## Koodikontroll (24.10.2026)

| Nõue | Koodis tuvastatud | Päris katse |
|---|---|---|
| Unknown job → refused | Flask lubab ainult letter ja show_image; Atom keeldub tundmatust tööst enne jaamale saatmist | Veel dokumenteerimata |
| Üks täht, numbrid keelatud | Flask lubab ühe A–Z tähe, väiketäht tehakse suureks; Atom kontrollib uuesti | Veel dokumenteerimata |
| Vana töö ei liigu | Flask eemaldab vähemalt 30 s vana ootel töö enne poll-vastust; staatusepäring teeb sama | Veel dokumenteerimata |
| Internet katkeb töö ajal | Atom säilitab lõpptulemused RAM-is ja proovib iga 5 s järel uuesti; Flask võtab vastu hilise ja korduva tulemuse | Jaama töö lõpuni tegemine vajab päris katset |
| Atom vooluta → OFFLINE | Pärast üle 10 s ilma autentitud pollita OFFLINE, last_seen säilib; lehe päringuvahe on 2 s | Veel dokumenteerimata |

Kontrollitud failid: selle repo `Server/app.py`, `Server/tests/test_app.py` ning
kõrvalrepo `ESP32-Image-Server-Fork/atom-image-server/src/server_client.cpp`,
`letter_sender.cpp` ja `main.cpp`. Jaama MG400 teostust tööruumis ei leitud.

Tundmatu töö ja vigane letter on kaks eri katset. Mõlemal peab olema refused
ning poll ei tohi väljastada ühtegi uut tööd. Tähtede kontroll ei asenda
unknown job kontrolli.

Serveri aegumine puudutab **ootel** tööd. Juba Atomile saadetud töö ei aegu
Flaskis ning võib lõpuni töötada. Atomil/jaamal pole täiendavat töö vanuse
kontrolli: serveri piir ei taga täitmise alustamist 30 s sees, kui jaam ise
hoiab töid järjekorras. Katsetes saada üks töö korraga.

Internetikatkestus ja voolukatkestus on erinevad: Atomi saatmata tulemused ning
serveri tööd on RAM-is. Neid ei säilitata restardi üle. Katkestuskatse ajal
ära taaskäivita serverit ega Atomi. Serveri restart nullib ka töö ID loenduri,
seega võivad vanad tulemused uute ID-dega kattuda; see pole praegu lahendatud.

Jaam peab tagastama `/api/letter` päringule kiiresti vastuvõtu kinnituse ja
käivitama töö iseseisvalt. Atom ootab jaama HTTP-vastust kuni 3 sekundit.
Töö lõpus saadab jaam Atomi `/api/result` aadressile `{id, result: done}` või
`error`, sama töö ID-ga. Jaam peab kordama saatmist kuni HTTP 200 vastuseni:
Atom vastab 503, kuni avalik server on tulemuse tegelikult kinnitanud.
`Atom Accepted` tähendab edastamist, mitte roboti töö lõppu; selle vaheoleku
saatmine pole Atomi koodis korduskatsega. Lõpptulemused on korduskatsega.
Kui interneti kadumine võtab maha ka jaama–Atomi võrgu, peab jaam hoidma
saatmata tulemust ise; selle teostus vajab jaama koodi kontrollimist.

## Käsitsi kontroll laboris

Enne iga katset lase eelmine töö lõpetada ja kontrolli tühja järjekorda.
Salvesta kuupäev, koodi commitid, töö ID, nähtud tulemus ja video/logi failinimi.
Ära kirjuta allolevaid katseid tehtuks enne seadmega kontrollimist.

1. Ava juhtimisleht mobiilse andmesidega (WiFi väljas). Brauseri konsoolist
   saab saata `fetch('/api/jobs', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({job:'unknown',arg:'A'})}).then(async r => console.log(r.status, await r.json()))`.
   Oota HTTP 400 / refused; robot ei liigu. Korda letter argumentidega `1`,
   `AB` ja tühja stringiga. Lubatud `A` peab jõudma jaamani.
2. Lülita Atom välja, saada veebist üks letter töö, oota vähemalt 35 s.
   Lehel peab olema expired. Lülita Atom sisse: poll peab vastama msg:null
   ning robot ei tohi selle töö tõttu liikuda. Korda ka show_image tööga.
3. Saada letter töö ja oota esimene liigutus. Katkesta **internetiühendus**,
   jättes jaama, roboti ja Atomi tööle ning kohaliku võrgu alles. Robot peab
   lõpetama. Taasta internet ja kontrolli, et sama ID staatus muutub done-ks.
   Logis peavad olema saatmiskatsed ja lõpuks Server confirmed result.
   Korda kolm korda. Kohaliku võrgu katkestus on eraldi lisakatse.
4. Pärast autentitud polli pane last_seen kirja ja võta Atom voolust välja.
   Umbes 10–12 s pärast peab leht näitama OFFLINE ning sama last_seen aega.
   Atomi tagasi ühendamisel peab ilmuma ONLINE ja uus aeg.

Serveri automaatkontroll (ei liiguta robotit): Server kaustas
`.venv/Scripts/python.exe -m unittest discover -s tests -v` (Windows) või
`.venv/bin/python -m unittest discover -s tests -v` (Linux).

## Latentsus: 30 + 30 vaatlust

Mõõdetav on `esimene nähtav roboti liigutus − SEND-vajutus`, mitte HTTP aeg,
Atom Accepted ega done saabumise aeg. Pilditöö ei sobi roboti liikumise
mõõtmiseks. Kasuta mõlemas seerias sama letter_A tööd ja samu roboti seadeid.

1. Atomi lokaalses `src/secrets.h` failis määra `POLL_INTERVAL_MS = 1000`.
   Tee Build ja Upload. Võtmeid reposse ei lisata. Teises seerias kasuta
   `POLL_INTERVAL_MS = 5000`, ehita ja laadi uuesti üles.
2. Filmil peavad samal ajal näha olema SEND-nupp ja robot. Näiteks kõrvalvaataja
   kaamera salvestab telefonis mobiilse andmesidega avatud lehe ning roboti.
   Kasuta sama kaamera ajajoont mõlema sündmuse jaoks; eri seadmete kellade
   ajatemplite lahutamine ei ole ilma sünkroonimiseta usaldusväärne.
3. Märgi t0 kaader, kus SEND vajutatakse, ja t1 kaader, kus robot esimest
   korda liigub. Püsiva 60 fps video korral `latency_ms = (t1-t0)*1000/60`.
   Muutuva kaadrisagedusega videol kasuta kaadrite tegelikke ajatempleid.
   Kaadripõhine vaatlus annab ligikaudse mõõtmise; 60 fps kaadrivahe on 16,7 ms.
4. Enne järgmist vajutust peab robot olema töö lõpetanud ja järjekord tühi.
   Ära saada 30 tööd korraga. Varieeri vajutuste vahet, et neid mitte kogemata
   pollimise rütmiga sünkroniseerida. Tee soojendus enne mõõteseeriat.
5. Täida `Measurements/lab2_latency.csv`: read 1–30 on 1 s intervalliga,
   31–60 on 5 s intervalliga. Tühjad latency_ms väljad on mõõtmata, mitte nullid.
   Pane video, kaadrid/ajatemplid, FPS ja ebaõnnestunud katsed eraldi märkmetesse.
   Ära eemalda aeglasi mõõtmisi; ühendusveaga katse dokumenteeri ja korda.
6. Võrdluseks mõõda Labori 1 otsene Atom → jaam tee sama esimese liigutuseni.
   Täida `Measurements/lab1_latency.csv` (intervall 0 = pollimist pole).
   Mallis on 30 vaatlust; olemasolevat Labori 1 mõõtmist võib kasutada, kui
   meetod ja tingimused on võrreldavad. Ära asenda seda arvutatud oletusega.

Lab2 kaustast kokkuvõtte arvutamine (Python standardteek, lisapakette pole):

```bash
python Tools/summarize_latency.py Measurements/lab2_latency.csv --lab1 Measurements/lab1_latency.csv
```

Väljundis on iga seeria mõõtmiste arv, keskmine, min, max ja Labori 1 keskmise
suhtes lisandunud viivitus. Tühjade mallide puhul kuvatakse INCOMPLETE.
1 s intervall tähendab nominaalselt 3600, 5 s intervall 720 polli tunnis.
Need on arvutuslikud sagedused, mitte mõõdetud võrgupäringute arvud:
HTTP kestus, tööd ja tulemuste kordussaatmine võivad tegelikku sagedust vähendada.
Pollingust tulenev ooteaeg on juhusliku vajutuse korral eeldatavalt umbes
pool intervallist; see pole roboti kogulatentsuse mõõtmistulemus.

## Katsete protokoll

| Katse | Kuupäev / commitid | Töö ID / video / logi | Tegelik tulemus |
|---|---|---|---|
| Unknown ja vigane täht | | | Mõõtmata |
| Aegunud letter ja show_image | | | Mõõtmata |
| Internet katkeb, katse 1 | | | Mõõtmata |
| Internet katkeb, katse 2 | | | Mõõtmata |
| Internet katkeb, katse 3 | | | Mõõtmata |
| Atom vooluta, OFFLINE ja last_seen | | | Mõõtmata |
| 1 s, 30 mõõtmist | | | Mõõtmata |
| 5 s, 30 mõõtmist | | | Mõõtmata |
| Labori 1 võrdlus | | | Mõõtmata |
