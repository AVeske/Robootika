# Server API — kes kellele mida saadab

Uuendatud 24.10.2026. Serveri kirjeldus vastab [app.py](../Server/app.py) ja [veebilehe](../Server/templates/index.html) praegusele teostusele. Avalik baas-URL on `https://narva1.roboarena.org`; allpool toodud API teed lisatakse selle lõppu.

## Osapooled ja vastutus

| Saatja → saaja | Mida saadetakse | Milleks / vastus |
|---|---|---|
| Kasutaja brauser → server | `GET /` | Server tagastab juhtimislehe HTML-i. |
| Brauser → server | `POST /api/images`, PNG fail väljal `file` | Pildi üleslaadimine; server tagastab pildi ID. |
| Brauser → server | `GET /api/images` ja `GET /api/images/<id>/preview` | Piltide valik ja valitud pildi eelvaade. |
| Brauser → server | `POST /api/jobs`, `{job, arg}` | Kasutaja tellib töö; server tagastab `job_id`. |
| Atom → server | `POST /api/poll`, API võti päises | Atom teatab oma kohalolekust ja küsib järgmist tööd. |
| Server → Atom | Polli HTTP-vastus `{msg, job, arg}` või `{msg:null}` | Üks ootel töö või teade, et tööd pole. Server ei algata ühendust. |
| Atom → jaam | Tähetöö kohalikule `/api/letter` liidesele | Jaam võtab tähe vastu ja käivitab roboti töö. Täpne kohalik leping on allpool. |
| Jaam → MG400 | Tähe joonistamiseks vajalikud liikumiskäsud | Jaam teisendab tähe punktideks ja juhib robotit kohalikus võrgus. |
| Jaam → Atom | Kohalik `POST /api/result`, `{id, result}` | Jaam teatab tegeliku töö lõppemisest või veast. |
| Atom → server | `POST /api/result`, `{id, result}`, API võti päises | Atom vahendab tulemuse avalikku serverisse. Pilditöö täidab Atom ise. |
| Brauser → server | `GET /api/status` iga 2 sekundi järel | Server tagastab Atomi kohaloleku, viimase postilkäigu aja ja tööde tulemused. |

Droplet ei saada robotile otse koordinaate, kiirusi ega pumba juhtimiskäske. Lubatud on ainult `letter` ja `show_image`. Kaameravood ei kuulu sellesse API-sse ning jäävad labori võrku.

## Autentimine ja vorming

JSON-päringud kasutavad `Content-Type: application/json`. PNG üleslaadimine kasutab `multipart/form-data` vormingut.

Atom saadab `POST /api/poll`, `POST /api/result` ja `GET /api/images/<id>/png` päringutel päise:

```text
X-API-Key: <Atomi ja serveri ühine salajane võti>
```

Server loeb võtme keskkonnamuutujast `ATOM_API_KEY` (ka `.env` kaudu) ning keeldub käivitumast, kui võti puudub. Võtme tegelikku väärtust dokumenti, URL-i ega brauseri JavaScripti ei lisata. Puuduva või vale võtme vastus on HTTP 401 `{"error":"unauthorized"}`.

Brauseri liidestel pole Flaski koodis API võtme kontrolli. Võimalik kasutaja sisselogimine tuleb seadistada pöördproksis; Atomi võti ei ole kasutaja parool. HTTPS-i avalikustamine on kirjeldatud [paigaldusjuhendis](deployment-and-verification.md).

## Kasutaja tellib töö: POST /api/jobs

Brauser saadab näiteks:

```json
{"job":"letter","arg":"A"}
```

| Töö | `arg` | Täitja |
|---|---|---|
| `letter` | Üks täht A–Z; väiketäht teisendatakse suurtäheks. Numbrid (nii JSON arv `7` kui tekst `"7"`), mitu tähte, tühikud, kirjavahemärgid ja täpitähed ei sobi. Kontrollitakse algset ASCII sisendit enne suurtäheks teisendamist; `ı` ja `ſ` on samuti keelatud. | Jaam koos MG400-ga, Atomi vahendusel. |
| `show_image` | Varem üles laaditud PNG 64 märgiga SHA-256 ID. | Atom kuvab pildi oma ekraanil. |

Edukas vastus on HTTP 201:

```json
{"job_id":1,"status":"accepted"}
```

`accepted` kinnitab järjekorda lisamist. Töö salvestatud olek on `waiting`; see vastus ei kinnita roboti liikumist ega töö lõpetamist. Järjekord on FIFO ning igal tööl on oma ID.

HTTP 400 keeldumised:

| Olukord | Vastuse sisu |
|---|---|
| JSON ei ole objekt | `{"status":"refused","reason":"JSON object required"}` |
| Tundmatu või keelatud töö | `{"status":"refused","reason":"Unknown or forbidden job"}` |
| Vigane täht | `{"status":"refused","reason":"Letter must be A-Z"}` |
| Tundmatu või vigane pildi ID | `{"status":"refused","reason":"Select an uploaded image"}` |

Veebilehel on tähe jaoks A–Z rippmenüü. JavaScript kontrollib enne saatmist nii töö nime kui ka tähe väärtust; server teeb sõltumatu kontrolli ka otse API-sse saadetud päringutele.

Keeldutud päring ei lisa järjekorda tööd ega saa töö ID-d. See ei muuda olemasolevat tööd, järjekorda ega järgmise töö ID loendurit. Poll ei väljasta keelatud sisendit. Varem vastu võetud lubatud töö võib endiselt täituda.

Automaattestid katavad kõik 52 ASCII suur- ja väiketähte, kõik kümme numbrimärki, JSON arve ja muid tüüpe, vigaseid töö nimesid ning Unicode erijuhte. Tulemused ja füüsilise seadmekatse piir on kirjas [kontrollijuhendis](verification-and-latency.md).

## Atom küsib tööd: POST /api/poll

Atom algatab päringu oma seadistatud küsimisvahega ning lisab API võtme päise. Keha võib olla `{}`: server ei loe polli keha ega salvesta sealt näiteks `device` või `robot` välju. Praegu tähendab oleku saatmine autentitud kohalolekuteadet, mitte roboti valmisoleku või andurinäitude edastamist.

Iga õige võtmega poll uuendab `last_seen` aega. Vale võtmega poll seda ei uuenda ega võta tööd järjekorrast.

HTTP 200 vastus tähetööga:

```json
{"msg":1,"job":"letter","arg":"A"}
```

Pilditööga:

```json
{"msg":2,"job":"show_image","arg":"<pildi ID>","image_url":"/api/images/<pildi ID>/png"}
```

Töö puudumisel:

```json
{"msg":null}
```

`msg` on sama töö ID, mille brauser sai väljal `job_id`. Polliga väljastatud töö saab oleku `sent` ning eemaldatakse ootejärjekorrast. Server ei saada seda järgmisel pollil automaatselt uuesti, ka juhul, kui eelmine HTTP-vastus võrgus kaotsi läks.

## Pildi üleslaadimine ja allalaadimine

| Saatja | Päring | Edukas vastus |
|---|---|---|
| Brauser | `POST /api/images`, multipart-väli `file` | HTTP 201 `{"id":"<64 märgiga ID>","name":"<ID esimesed 12 märki>.png","width":128,"height":128}` |
| Brauser | `GET /api/images` | HTTP 200 `{"images":[{"id":"<ID>","name":"<nimi>.png"}]}`; tühjal valikul `images:[]`. |
| Brauser | `GET /api/images/<id>/preview` | HTTP 200, `image/png`. |
| Atom, API võtmega | `GET /api/images/<id>/png` | HTTP 200, `image/png`. |

Üleslaaditav pilt peab olema staatiline PNG kuni 1 MiB, mõõtmetega 1–2048 pikslit kummaski suunas. Server mahutab pildi proportsioone säilitades 128 × 128 mustale RGB taustale. ID on salvestatud PNG SHA-256 räsi. Pildid säilivad `Server/instance/images` all või `IMAGE_DIR` määratud kaustas.

Puuduv fail saab HTTP 400 `{"status":"refused","reason":"PNG file required in field file"}`. Vigane formaat või mõõtmed annavad HTTP 400 `{"status":"refused","reason":"Invalid PNG; use a static PNG up to 2048 x 2048"}`. Liiga suur fail või päring annab HTTP 413 `{"status":"refused","reason":"PNG upload limit is 1 MiB"}`. Tundmatu eelvaate või allalaadimise ID vastus on HTTP 404 `{"error":"Unknown image"}`. Allalaadimisel kontrollitakse esmalt API võtit.

Atom peab liitma polli `image_url` tee avaliku serveri baas-URL-iga, kasutama HTTPS-i ja saatma API võtme päises. `done` tuleb saata alles pärast pildi edukat kuvamist. See kirjeldab püsivarale vajalikku lepingut; pildi kuvamise teostus ja seadmekatse pole selles repos kinnitatud.

## Atom saadab tulemuse: POST /api/result

Atom lisab API võtme päise ning saadab:

```json
{"id":1,"result":"done"}
```

`id` peab olema JSON täisarv ja vastama serveris teadaolevale, juba väljastatud tööle. See võib olla ka varasem töö, mitte ainult viimane töö.

| `result` | Tähendus |
|---|---|
| `Atom Accepted` | Vahekinnitus: Atom on töö vastu võtnud või edasi andnud; töö pole veel lõpetatud. |
| `done` | Täitja teatab õnnestumisest: täht on joonistatud või pilt kuvatud. |
| `refused` | Täitja keeldus tööst. |
| `error` | Täitja teatab töö veast. |

HTTP 200 vastus on `{"status":"ok"}`. Server talletab saadetud tulemuse ega kontrolli ise roboti füüsilist tegevust.

| HTTP | `error` | Põhjus |
|---|---|---|
| 400 | `Invalid job ID` | Keha pole JSON-objekt või `id` pole täisarv. |
| 400 | `Invalid result` | Tulemus pole üks ülaltoodud neljast väärtusest. |
| 400 | `Unknown job` | ID-d pole serveri töömälus. |
| 409 | `Job has not been dispatched` | Töö on veel `waiting`. |
| 409 | `Conflicting final result` | Lõppenud tööle saadeti varasemast erinev lõpptulemus. |

Sama lõpptulemuse kordussaatmine saab HTTP 200. Hiline `Atom Accepted` saab samuti HTTP 200 ning ei kirjuta lõpptulemust üle. `expired` on serveri määratud olek: Atom ei saa seda tulemuse väärtusena saata.

## Brauser loeb olekut: GET /api/status

Brauser saadab kehata GET-päringu iga 2 sekundi järel. HTTP 200 näide:

```json
{
  "robot_status":"ONLINE",
  "last_seen":"2026-10-24T14:00:00+03:00",
  "last_job":{"id":1,"job":"letter","arg":"A","status":"done"},
  "queue_length":0,
  "jobs":[{"id":1,"job":"letter","arg":"A","status":"done"}]
}
```

- `robot_status` näitab nimele vaatamata **Atomi pollimise värskust**, mitte MG400 ühendust või liikumisvalmidust. `ONLINE` tähendab, et autentitud pollist on möödas kuni 10 sekundit; muidu `OFFLINE`.
- `last_seen` on viimase autentitud polli ISO 8601 ajatempel koos serveri ajavööndi nihkega. Veebileht kuvab selle Tallinna ajas. Enne esimest polli on väärtus `null`; Atomi vaikimisel säilib viimane aeg.
- `last_job` on viimati loodud töö või `null`, kui töid pole loodud.
- `queue_length` on ootel, veel väljastamata tööde arv.
- `jobs` sisaldab kuni 50 viimati loodud töö ID-d, tüüpi, argumenti ja olekut. Enne esimest tööd on see `[]`.

Töö olekud on `waiting`, `sent`, `Atom Accepted`, `done`, `refused`, `error` ja `expired`. Brauseri `SERVER ERROR` on lehe enda teade ebaõnnestunud staatusepäringu kohta, mitte serveri tagastatav tööolek.

## Aegumine ja ühenduse katkestus

Server kontrollib ootel tööde vanust töö loomisel, pollimisel ja staatusepäringul. Vähemalt 30 sekundit vana ootel töö saab `expired` oleku ning seda Atomile ei anta. Kui järjekorras on ka värskem töö, võib poll tagastada selle; ainult aegunud tööde korral tagastatakse `msg:null`.

Juba väljastatud töö serveris ei aegu. Poll-vastus ei sisalda loomisaega ega aegumistähtaega, mistõttu serveri kontroll üksi ei taga, et jaama järjekorras kaua seisnud töö ei alusta hiljem liikumist.

Tulemuse saatja peab katkenud ühenduse korral hoidma saatmata lõpptulemust koos sama ID-ga ja proovima uuesti kuni HTTP 200 vastuseni. Server lubab väljastatud töö hilise ja korduva tulemuse. Atomi kordussaatmist kirjeldab [kontrollijuhend](verification-and-latency.md); selle tegelik toimimine kogu ahelas vajab seadmekatset.

Tööd, ID loendur ja `last_seen` on serveri RAM-is. Serveri restart kustutab need ning alustab ID-de loendamist uuesti. Restartide ülene tööde taastamine ja vanade tulemuste eristamine uutest sama ID-ga töödest pole teostatud. Kettale salvestatud PNG pildid säilivad.

## Kohalik Atom–jaam–robot leping

Selle repo serverikood katab brauseri ja Atomi avaliku API. Atomi ja MG400 jaama lähtekood asub eraldi projektides: [Atomi projekt](../firmware/README.md) ning [jaama kirjeldus](../../Lab1/docs/letter_writer.md). Järgnev on integratsioonile vajalik leping, mitte siin kontrollitud kohaliku API täielik spetsifikatsioon.

1. Atom annab `letter` töö kohalikule jaama `POST /api/letter` liidesele. Täht on `letter` väljal, näiteks `{"letter":"A"}`. Avaliku töö ID peab jõudma jaamani ja sealt lõpetamise teates muutumatult tagasi; ID täpne väli jaamasuunalises päringus vajab jaama lähtekoodiga kinnitamist.
2. Jaam peab tagastama kiiresti vastuvõtukinnituse ning täitma töö iseseisvalt. Vastuvõtukinnitus ei tähenda joonistamise lõppu. Kontrollijuhendi järgi ootab Atom jaama HTTP-vastust kuni 3 sekundit.
3. Jaam saadab robotile tähe punktidest arvutatud liikumiskäsud ja jälgib töö lõppemist. MG400 ei kutsu avalikku serveri API-t.
4. Jaam saadab Atomi kohalikule `POST /api/result` liidesele `{"id":1,"result":"done"}` või `error`. Atom vahendab sama ID ja tulemuse avaliku serveri `/api/result` liidesele.
5. Kontrollijuhendis nõutakse, et jaam kordaks lõpptulemust kuni Atomi HTTP 200 vastuseni; Atom peaks vastama 503, kuni avalik server on tulemuse kinnitanud. Kohaliku autentimise ja muude vastuste täpne teostus vajab püsivara ja jaama koodist kinnitamist.

`show_image` töö jääb Atomile ega vaja MG400 liigutamist. Nõutud tööde ID sidumine, roboti tegelik lõpetamine ja katkestusest taastumine tuleb üle kontrollida [seadmekatsetega](verification-and-latency.md).
