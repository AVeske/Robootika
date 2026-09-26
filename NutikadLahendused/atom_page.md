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
