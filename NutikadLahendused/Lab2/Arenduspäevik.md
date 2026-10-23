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

