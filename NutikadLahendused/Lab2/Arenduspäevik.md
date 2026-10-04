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


