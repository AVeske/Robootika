# Nutikad Lahendused

## 26.09.2026

1. Loodi `atom_page.md`, mis kirjeldab AtomS3R-i veebiliidese ja tähevaliku arendust.
   - Dokumenteeritud on captive portal, ekraani testnupp ning Atomi nupuga tähtede A–Z valimine.
   - Kirjas on ka valitud tähe saatmine tööjaama üle WiFi või COM-pordi kaudu.

## 30.09.2026

1. Täiendati pildiserveri põhifunktsioone.
   - Lisati ekraanikuva ja tähe valimise ning saatmise loogika jaoks lähte- ja päisefailid.
   - Uuendati põhifailivara, et toetada pildi käsitlemist ja saatmise töövoogu.
2. Seadme põhifunktsionaalsus laienes märgatavalt ning projektist sai toimiv ESP-ekraaniserver.


## 03.10.2026

1. Loodi `letter_writer.md`, mis kirjeldab projekti käivitamist ja tähe robotiga kirjutamise töövoogu.
   - Juhend sisaldab MG400 ja AtomS3R-i seadistamist ning PlatformIO abil püsivara ehitamist ja üleslaadimist.
   - Dokumenteeritud on tähtede API kaudu vastuvõtmine, tähtede koordinaadid, roboti kirjutamisloogika ja järjekord.
   - Kirjas on ka COM-pordi kasutamine `letter_station.py` tööriistaga ning robotiga kirjutamise kõrguse katsetamine.
2. Ühendati saatmisloogika API-põhise ühendusteega.
3. Süsteemi saab kasutada välise API-ühenduse kaudu, mitte ainult kohaliku või sisemise käsitlusega.
4. Lisati COM-pordi tugi ja täiendati saatmisloogikat.
   - Lisati Pythoni abitööriist tähejaama juhtimiseks.
   - Uuendati uue funktsionaalsusega seotud Git ignore'i ja konfiguratsiooni.
5. Projekt toetab nüüd COM/serial-pordi kaudu suhtlust ning sisaldab hostarvutist jaama haldamise tööriistu.


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



