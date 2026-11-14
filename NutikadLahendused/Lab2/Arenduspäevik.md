# Nutikad Lahendused — Labor 2 arenduspäevik



## 03.10.2026

**Commit'ide autorid:** Ats Veske ja Serafima Amerhanova.

1. Lisatud Labor 2 README, mis määratleb labori eesmärgi ja kontrollnimekirja.
   - Töö keskmes on avalik droplet, kasutaja ja Atomi vaheline tööde postkontor ning kahe kaamera ja Atomi seadistuslehe arendamine.
2. Koostatud dropleti seadistamise juhend.
   - Juhend hõlmab SSH-võtmeid, Ubuntu uuendamist, vajalikke Python/Git/curl pakette, UFW tulemüüri ja Caddy pöördproksit.
   - Juhendis olemas serveri algseadistuse toimingud ning loetletud järgnevad Flaski, HTTPS-i ja Atomi ühendamise sammud.
3. Alustatud Flaski serveri ja veebiliidese arendust.
   - Lisatud `Server/app.py`, `Server/requirements.txt` Flaski sõltuvusega ja `Server/templates/index.html`.
   - Veebileht võimaldab saata tähetööd ning kuvab roboti ühenduse, viimase ühenduse aja ja viimase töö oleku.
   - Serveris Loodud tööde vastuvõtmise, Atomi pollimise, töö tulemuse vastuvõtmise ja oleku pärimise API: `POST /api/jobs`, `POST /api/poll`, `POST /api/result` ja `GET /api/status`.
   - Atomi päringut kaitseb `X-API-Key` päis. Server hoiab ootel ja viimast tööd ning Atomi viimase ühenduse aega RAM-is.
   - Koodis on määratud töö aegumiseks 30 sekundit ja Atomi offline-oleku piiriks 10 sekundit. Need on seadistatud väärtused, mitte mõõdetud latentsusnäitajad.
4. Atom algatab serveriga ühenduse ja küsib töid perioodiliselt; server ei algata ühendust labori seadmetega.
- Esmane tööde salvestus toimub serveri mälus. Püsivat andmebaasi veel ei lisatud, mis teeb algse prototüübi lihtsaks, kuid tähendab, et serveri taaskäivitamisel olek kaob.
- Serveri sõltuvused märgiti `requirements.txt` faili; vahecommit'ides korrastati selle failinime ja serveri algfailide asukohta.



## 04.10.2026


1. Täiendatud serveri API dokumentatsiooni failis `Docs/server_api.md`.
   - Kirjeldatud veebilehe ja Atomi kasutatavaid päringuid, sisend- ja väljundnäiteid, autentimist, veavastuseid, töö olekuid ja aegumist.
2. Täiendatud dropleti ja avalikustamise dokumentatsiooni.
   - Lisatud  `flask-caddy-deployment.md`, mis kirjeldab Flaski hoidmist lokaalsel liidesel ja Caddy kasutamist HTTPS-i pöördproksina.
   - Lisatud `job-storage-and-atom-polling_info.md`, mis selgitab tööde RAM-is hoidmist ning Atomi regulaarset pollimist.
   - `server_setup.md` täiendatud dropleti paigaldamise ja käivitamise juhendiks.

3. Caddy avalikustamise dokument kirjeldab domeeni `narva1.roboarena.org`, HTTPS-i ning päringute suunamist Flaskile aadressil `127.0.0.1:5000`.
- Caddy võtab vastu avalikud HTTPS-päringud ja vahendab need kohalikule Flaski rakendusele, et Flaski porti ei peaks internetti avama.

4. Listaud Flaski keskkonnamuutujate laadimine `.env` failist.
   - `Server/app.py` kasutab `python-dotenv` paketi `load_dotenv()` funktsiooni, et laadida rakenduse käivitamisel `.env` faili väärtused keskkonda.
   - Atomi API võti loetakse endiselt keskkonnamuutujast `ATOM_API_KEY`; kui seda pole määratud, jääb alles testimiseks mõeldud `CHANGE_ME` vaikeväärtus.
   - `python-dotenv` lisati serveri `requirements.txt` faili.
   - `.env` faili ennast muudatustes ei lisatud; saladusi ei kirjutata rakenduse lähtekoodi.


## 23.10.2026

Projektist saab kaugjuhtimisega ühendatud seade, mitte ainult lokaalne ekraani-/pildi server. 

Kokkuvõttes: salajased andmed ei satu reposse; seade saab serverist juhtnööre ja töid, mitte ainult lokaalseid käske; JSON ja polling on selge ja standardiseeritud lahendus; iga seade saab sama koodi, kuid oma lokaalse konfiguratsiooni.

Muudatused tehtud ESP32-Image-Server-Fork branchi atom-image-server kausta failides.

1. atom-image-server/platformio.ini
   - Lisati uus sõltuvus: ArduinoJson.
   - See tähendab, et firmware saab nüüd JSON-i mugavalt parseerida ja töödelda, ilma et oleks vaja käsitsi stringide lõhkumist teha.
   - Kasu: lihtsam ja turvalisem serveri-vastuse töötlemine; rohkem standardset JSON-töötlust ja vähem vigu.

2. atom-image-server/src/secrets.example.h
   - Lisati template salajaste väärtuste jaoks: WiFi SSID, parool, serveri URL ja API võti.
   - See on “näidis” fail, mitte tegelik salajane konfiguratsioon.
   - Kasu: projekt on nüüd sama koodiga kasutatav erinevates keskkondades, ilma et oleks vaja iga kord privaatseid väärtusi repo’sse kirjutada.

3. .gitignore
   - Lisati kirje src/secrets.h ignoreerimiseks.
   - See tähendab, et tegelikud konfiguratsiooniväärtused ei lähe Git’i versioonihaldusse.
   - Kasu: ei teki “salajased võtmed repos’i sisse” probleemi, vähem turvariske, lihtsam tootmisdeploy.

4. atom-image-server/src/server_client.h
   - Lisati väheima APIga klient, mis tegeleb serveriga suhtlemisega.
   - Kasu: koodi struktuur on selgem; serveri interaktsioon eraldub “peamisest” ekraani-/seadmekoodist.

5. atom-image-server/src/server_client.cpp
   - Lisati uus pollServer() funktsioon.
   - Seadme kood: kontrollib WiFi seisundit, logib võrgu staatust, teeb HTTPS POST päringu serveri /api/poll endpointi, lisab X-API-Key pealkirja, loeb JSON vastuse ja parseerib job’i/teate infot.
   - Kasu: seade ei ole enam ainult “lokaalne ekraani moodul”, vaid saab serverist automaatselt teateid ja töid.

6. atom-image-server/src/main.cpp
   - Integreeriti uus serveri-polling süsteem peamise firmware käivitus-/tsükli osasse.
   - Lisati ka signaalid ja logid, millega näha, kas WiFi on ühendatud ja mida server vastab.
   - Kasu: see teeb seadme palju rohkem “hallatavaks” ja “keskjuhtimisega” sobivaks; kood on valmis edasiseks serveripoolseks kontrolliks.




## 24.10.2026

- **PNG pilditöö (`e26cb9b`).** Serverisse ja juhtimislehele lisati piltide üleslaadimine, nimekiri ja Atomi allalaadimise liides. Server kontrollib staatilist PNG-d, 1 MiB suuruspiiri ja kuni 2048 × 2048 mõõtmeid ning salvestab proportsioone säilitava 128 × 128 pildi. Pildi ID põhineb räsi väärtusel ja pildid säilivad kettal. Täiendati sõltuvusi, API dokumentatsiooni ning teste; piltide salvestuskaust lisati ignoreeritavate hulka.
- **Eelvaade ja ajatemplid (`78522ce`).** Lisati valitud pildi eelvaade brauseris ning `GET /api/images/<id>/preview`. Viimase postilkäigu aega kuvatakse veebilehel Tallinna ajas; serveri ajatempel sisaldab ajavööndi nihet. 
- **Kontrollid ja mõõtmismallid (`36097a9`).** Lisati tööde keeldumise, aegumise, autentimise, kohaloleku ja katkestusest taastumise serveritestid ning seadmekatsete juhend. 
- **Serveri püsiv käivitamine (`b47ae12`).** Lisati `robot-postoffice.service` ja paigaldusjuhend. Gunicorn kuulab `127.0.0.1:5000`; systemd haldab protsessi ja võimaldab selle käivitada sõltumata SSH seansist. 
- **API ja sisendikontroll (`88e4d1b`).** `Docs/server_api.md` kirjutati vastavusse praeguse serveriga: brauseri, serveri, Atomi, jaama ja roboti rollid; päringud, vastused, võtmed, ID-d, järjekord, tulemused ja piirangud. Tähetöö veebiväli muudeti A–Z valikuks ning server kontrollib enne suurtäheks teisendamist algset ASCII tähte. Varasemas tänases sissekandes on kirjas 12 läbinud serveritesti; siin ei lisata uut katsesooritust.
- **ÜldResult (`cd4b5b8`, `88e4d1b`).** [Ühiskatse kirjeldus](../../ÜldResult/Lab1&2/Kirjeldus.md) ja kolm MOV-faili koondavad veebilehe, serveri, Atomi ning roboti demonstratsiooni. 


### Lubatud tööde ja tähe sisendi kontroll

- Tähe vabatekstiväli asendati A–Z valikuga ja brauserisse lisati saatmiseelne kontroll.
- Server kontrollib algset sisendit mustriga `[A-Za-z]` enne suurtäheks teisendamist. Nii ei pääse Unicode `ı` ja `ſ` teisendamise kaudu lubatud täheks. Numbrid ja tundmatud tööd annavad HTTP 400 / refused.
- Lubatud töödeks jäid `letter` ja `show_image`. Pildi ID numbreid ei keelatud.
- Laiendati teste: sobivad kõik 52 ASCII tähte; vigane sisend ei muuda lubatud ootel tööd ega jõua poll-vastusesse. Kõik 12 serveritesti läbisid.
- Uuendati API, kontrolli, paigalduse ja tööde salvestuse dokumentatsiooni. 



## 25.10.2026 — videokatsete filmimine

- Filmiti veebilehe, Flaski serveri, Atomi ja MG400 koostööd tähetöö edastamisel ja joonistamisel. [Tähtede joonistamise video](../../ÜldResult/Lab1&2/1_Tähtede_joonistamine/tahtede_joonistamine.mp4).
- Filmiti veebiliidese ja Atomi vahelist pildi edastamist ning ekraanil kuvamist. [Pildi edastamise video 1](../../ÜldResult/Lab1&2/2_Pildi_edastamine_ja_kuvamine/pildi_edastamine_1.mp4). [Pildi edastamise video 2](../../ÜldResult/Lab1&2/2_Pildi_edastamine_ja_kuvamine/pildi_edastamine_2.mp4).
- Filmiti ühenduse katkestamist tähetöö ajal: robot lõpetab joonistamise ning ühenduse taastumisel kuvatakse töö olekuks Done. [Ühenduse katkestamise video](../../ÜldResult/Lab1&2/3_Käitumine_ühenduse_katkestamisel/uhenduse_katkestamine.mp4).
- Filmiti USB-veebikaamera ja XIAO kaamera pildi kuvamist ühisel jälgimislehel roboti töötamise ajal. [Kaamerate video](../../ÜldResult/Lab1&2/5_Kaamerad/kaamerad.mp4).
