## Nutikad Lahendused: Labor 2 — Server internetis ja kaks kaamerat

**Töömaht:** 28 tundi | **Hindamine:** 20 punkti | **Meeskond:** 3 tudengit | **Välja antud:** 07.10.26 | **Tellimise kuupäev:** 16.10.26 | **Esimene kaitsmine:** 27.10.26, veebis

### Kuidas see dokument töötab

* Repo ja töökord on Laborist 1 olemas ja samad.
* Too sellest dokumendist oma projekti repo juurde see, mida vaja: selle labori kaust, `README.md`, kuhu lähevad su enda numbrid, otsused ja KAARDISTA ISE vastused, ja failid, mida kontrollnimekiri nimetab. Tervet dokumenti üle kopeerida ei ole vaja.
* Skeemid ja simulatsioonid lähevad dokumenti pildina, pildi juurde link elavale failile, et teine saaks selle lahti teha ja edasi muuta.

### Eesmärk

Laboris 1 sai jaam robotiga rääkima ja Atom sai oma lehe. Kõik see töötab ainult siis, kui sa oled laboris.

Su sülearvutil ja Atomil ei ole aadressi, mille peale keegi väljastpoolt saaks ühendust võtta. Labori võrk annab neile privaatse aadressi — samasuguseid aadresse on internetis miljoneid ja ükski marsruuter ei tea, milline neist sinu oma on. Sisse ei saa. Aga välja saab: seade võtab ise ühendust ja vastus tuleb tagasi sama teed. Kogu see labor on ehitatud selle asümmeetria peale.

Vahele tuleb **droplet**: väike Linuxi server, millel on päris avalik aadress ja päris nimi. Seal jookseb tavaline veebiserver, ja ta töötab nagu **postkontor**. Tema juurde tuleb kaks poolt, kes teineteise aadressi ei tea:

* **Kasutaja jätab sõnumi.** Brauser või telefon ükskõik kust. Sõnum on töö robotile: joonista see täht, näita seda pilti.
* **Roboti Atom tuleb ja küsib, kas talle on sõnumeid.** Ta võtab ise serveriga ühendust, kindla vahe tagant. Kui sõnum on, viib ta selle jaama, robot teeb töö ära, ja Atom jätab postkontorisse vastuse: tehtud või ei õnnestunud.

Robotini ei pääse väljast keegi. Postkontor ei tea, kus robot on, ja ei helista talle kunagi. Robot käib ise postil.

See on **kaugjuhtimine läbi postkontori**, ja tal on postkontori omadused. Ta on aeglane: sõnum ootab, kuni Atom järgmine kord tuleb. Ta ei ole otsejuhtimine: sõnumiga ei saa kätt millimeetri kaupa liigutada, saab tellida terve töö. Ja ta on vastupidav: kui ühendus kaob keset tööd, teeb robot töö lõpuni, sest kõik vajalik on tal juba käes. Otsejuhtimine, kus sa näed ja liigutad korraga, tuleb Laboris 3 ruuteri ja VPN-iga.

Ja laua juurde tuleb **kaks kaamerat**, sest robotit, mida sa ei näe, sa ei käsuta. Üks kaamera ei näe mõlemat asja korraga. Kaamera, mis näeb kogu lauda, ei näe, kas napp on klaasi keskel. Kaamera, mis näeb nappa, ei näe, kuhu käsi läks. Seepärast on neid kaks: **veebikaamera laua kohal**, robotist kõrgemal, näeb kogu lauda, ja **kaamera tööriista küljes** näeb ainult otsikut ja seda, mis otse selle all on. Selles laboris jõuavad mõlemad pildid jaama lehele labori võrgus. Laboris 3 lähevad nad sealt läbi VPN-i edasi.

Labori 1 lubadus kehtib edasi: **iga riistvara, mis Atomi külge tuleb, saab oma seaded ja testinupu sellele samale lehele.** Andmehõive Labor 2 paneb Atomi külge rõhuanduri koos astmega. Selle seaded ja test lähevad Atomi lehele, mitte uude kohta. Sinna lähevad ka postkontori aadress ja Atomi võti.

Selles laboris on kolm asja:

1. **Droplet.** SSH võtmed, tühi server, tulemüür, HTTPS.
2. **Postkontor.** Kasutaja jätab sõnumi, roboti Atom tuleb ja küsib. Robot teeb töö ära ja vastus läheb tagasi. Leht ütleb ausalt, kui Atom on vait.
3. **Kaamerad ja Atomi leht.** Üks kaamera näeb kogu lauda, teine otsikut. Rõhuandur saab Atomi lehele oma seaded ja testinupu.

Esimesel päeval uusi osi ei ole. Ehita sellest, mis riiulil on, ja kirjuta puuduv tellimuseks, mis läheb välja 16.10.

*See on elav dokument. Uuenda eesmärke, kui need töö käigus muutuvad — uued teadmised teevad vanad eesmärgid vahel mõttetuks. Mõte on hoida meeskond kogu aeg sihil, et ei eksitaks detailide metsa ja põhiprobleem ei jääks lahendamata.*

**KAARDISTA ISE — eesmärk nii, nagu ta tegelikult välja tuli.**

### Kontrollnimekiri

**Peab olema tehtud**

- [ ] Iga arvuti kohta, millega dropletisse minnakse, oma SSH võti; avalikud pooled saadetud õppejõule, vastuseks saadud dropleti aadress ja link.
- [ ] Droplet töötab. Igast neist arvutitest saab oma võtmega sisse, paroolisisselogimine keelatud, tulemüür lahti ainult nendel portidel, mida sa päriselt kasutad.
- [ ] Leht käib õppejõult saadud lingi peal ja HTTPS-iga.
- [ ] Veebiserver dropletis: kasutaja leht avaneb telefonist, mille WiFi on välja lülitatud.
- [ ] Atom käib postil: saadab oma oleku ja küsib, kas talle on sõnumeid. Oma võtmega.
- [ ] Kasutaja jätab lehel sõnumi, robot teeb töö ära, ja leht näitab vastust. Vähemalt kaks eri tööd, üks neist täht Laborist 1.
- [ ] Lubatud tööde nimekiri on kirjas. Sõnum, mida nimekirjas ei ole, ei liiguta midagi.
- [ ] Sõnum aegub: vana sõnum ei pane robotit liikuma. Läbi proovitud.
- [ ] Latentsus mõõdetud: 30 sõnumit kasutaja vajutusest roboti esimese liigutuseni, kahe erineva küsimisvahega.
- [ ] Ühendus katkestatud keset tööd: robot teeb töö lõpuni ja vastus jõuab kohale, kui ühendus tagasi tuleb.
- [ ] Atom on vait: leht näitab, millal ta viimati postil käis. Läbi proovitud Atomi vooluta jätmisega.
- [ ] Kes mida saadab, kirjas failis `docs/server_api.md`.
- [ ] Ohutuskokkulepe kirjas ja kõigil meeskonnaliikmetel loetud.
- [ ] Laua kaamera näitab kogu lauda: ruudustik servast servani ja robot.
- [ ] Tööriista kaamera näitab otsikut ja detaili selle all.
- [ ] Mõlemad pildid on jaama lehel, labori võrgus.
- [ ] Mõlema kaamera viide, kaadrisagedus ja ribalaius mõõdetud; roboti juhtimise latentsus mõõdetud uuesti, mõlema kaamera töötamise ajal.
- [ ] Rõhuanduri seaded ja testinupp Atomi lehel, `docs/atom_page.md` uuendatud.
- [ ] Tellimus 16.10 failis `docs/bom.md`.
- [ ] Repo ja arenduspäevik täidetud, tag `smart-solutions-lab2`.

**KAARDISTA ISE — kuupäevad ja sinu enda sammud.**

### Sisendid

* Laborist 1: jaam, MG400 baaspakett, `data/positions.json`, Atomi püsivara ja leht, aadressiplaan.
* Õppejõult: droplet meeskonna kohta, õppejõu konto pealt. See on tühi server: Ubuntu ja ei midagi muud. Sina saadad oma avaliku SSH võtme, õppejõud paneb selle dropletisse ja saadab vastu dropleti aadressi ja lingi.
* Riiulilt: USB veebikaamera (UHD), USB pikenduskaabel, Seeed Studio XIAO ESP32S3 Sense kaameramoodul (tootekood 113991115).
* Andmehõive L2-st: rõhuandur koos astmega ja kalibratsioonikonstandid, mis Atomi lehele lähevad.
* 3D printimise L2-st: mõlema kaamera kinnitused — post, mis hoiab veebikaamerat robotist kõrgemal, ja kinnitus, mis hoiab kaameramoodulit iminapa tööriistahoidiku küljes koos toitega; ja laud, mida nad näevad: Gridfinity ruudustik, kus iga hoidiku koht on ruudu nimi.

### Vahendid

1. Labori 1 jaam ja Atom
2. Digital Ocean droplet õppejõult: tühi Ubuntu
3. Link (nimi), mis dropletile viitab, õppejõult
4. SSH ja SSH võtmed
5. Veebiserver dropletis: Python 3, Flask
6. Pöördproksi, mis oskab sertifikaadi ise võtta ja ise uuendada
7. USB veebikaamera (UHD) ja USB pikenduskaabel; Seeed Studio XIAO ESP32S3 Sense kaameramoodul
8. Telefon mobiilse andmesidega, millega väljastpoolt testida
9. VS Code ja PlatformIO Atomi püsivara jaoks; git; draw.io

*Kui plaan muutub, uuenda ka vahendeid, või tee draw.io skeem, mis näitab, kuidas asjad omavahel töötavad.*

**KAARDISTA ISE — mida sa päriselt kasutasid.**

### Taustainfo

* **Droplet** — mis see on ja kuidas üks püsti panna
  [https://docs.digitalocean.com/products/droplets/](https://docs.digitalocean.com/products/droplets/)
* **Kuidas droplet turvaliselt seadistada**
  [https://www.youtube.com/watch?v=L8e_eAm4fFM](https://www.youtube.com/watch?v=L8e_eAm4fFM)
* **SSH võtmed.** Parool internetis olevale serverile on halb mõte: seda proovitakse ära arvata pidevalt ja automaatselt, mitte sellepärast, et keegi sind otsib, vaid sellepärast, et proovitakse kõiki. Võti on nii pikk, et seda ei arvata. Kuidas võti teha Windowsis ja Macis, on osas 1.
* **Caddy** — pöördproksi, mis võtab HTTPS-sertifikaadi ise ja uuendab seda ise
  [https://caddyserver.com/](https://caddyserver.com/)
* **Let's Encrypt** — tasuta sertifikaadid, mille peale eelmine punkt ehitatud on
  [https://letsencrypt.org/](https://letsencrypt.org/)
* **Flask**
  [https://www.youtube.com/watch?v=mqhxxeeTbu0&list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX](https://www.youtube.com/watch?v=mqhxxeeTbu0&list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX)
* **HTTPS ja Flask**
  [https://www.youtube.com/watch?v=VqnSenJAheU](https://www.youtube.com/watch?v=VqnSenJAheU)
* **ESP32 kui klient** — kuidas ESP32 ise serverile päringu teeb, GET ja POST
  [https://randomnerdtutorials.com/esp32-http-get-post-arduino/](https://randomnerdtutorials.com/esp32-http-get-post-arduino/)
* **Flask ja voogedastus** — kuidas üks marsruut saadab pilti lõputult, ühe vastuse sees
  [https://flask.palletsprojects.com/en/stable/patterns/streaming/](https://flask.palletsprojects.com/en/stable/patterns/streaming/)
* **MJPEG.** Lihtsaim videovoog, mis brauseris ilma midagi installimata töötab: järjest JPEG pilte ühes ja samas vastuses. Kliendi pool on üks `<img>` silt. Kvaliteedi ja kaadrisageduse eest maksad ribalaiusega, ja seda ribalaiust jagad sa juhtimisega.
* **ESP32-Image-Server** — Atomi leht, mille peale Laboris 1 ehitasid
  [https://github.com/KKallas/ESP32-Image-Server](https://github.com/KKallas/ESP32-Image-Server)
* **NAT ja privaatsed aadressid.** Võta Labori 1 aadressiplaan lahti ja võrdle seda dropleti aadressiga. Üks neist on selline, mida on internetis üks; teisi on miljoneid.

*Lisa siia oma allikaid ja kasulikku infot, mis aitaks sul projektist aru saada ka aastaid hiljem, kui selle uuesti lahti teed.*

**KAARDISTA ISE — sinu allikad.**

### Osad

#### 1. Droplet

Dropleti annab õppejõud. See on tühi server: Ubuntu, ja mitte midagi peal. Parooli tal ei ole. Sisse saab ainult SSH võtmega, ja seepärast on esimene samm sinu arvutis, mitte serveris.

**Tee võtmepaar.** Võtmel on kaks poolt. Privaatne pool jääb sinu arvutisse ja ei lahku sealt kunagi. Avalik pool läheb serverisse; seda võib igaühele näidata. Võti käib arvuti, mitte meeskonna kohta: **iga arvuti, millega sa kavatsed dropletisse minna, saab oma võtme**, tehtud selles arvutis. Meeskonnal võib neid olla rohkem kui üks — iga liikme sülearvuti, ja jaam, kui ka sealt on vaja sisse saada. Privaatset poolt ei kopeerita ühest arvutist teise.

Windowsis ava PowerShell, Macis Terminal. Käsk on mõlemas sama:

```
ssh-keygen -t ed25519 -C "meeskond-N kelle-arvuti"
```

Küsimusele, kuhu fail salvestada, vajuta Enter. Siis küsitakse võtme parooli; pane see, sest sülearvuti võib kaduda. Tekib kaks faili kaustas `.ssh` sinu kodukaustas: `id_ed25519` on privaatne ja `id_ed25519.pub` on avalik.

Näita avalikku poolt:

```
Mac:       cat ~/.ssh/id_ed25519.pub
Windows:   type $env:USERPROFILE\.ssh\id_ed25519.pub
```

Välja tuleb üks rida, mis algab sõnaga `ssh-ed25519`. See rida ongi avalik võti.

**Saada avalik võti õppejõule:** kaspar.kallas@ut.ee. Üks kiri meeskonna kohta, kõigi arvutite read sees, iga rea juures, kelle või mis arvuti see on, ja meeskonna number. Kui hiljem tuleb arvuti juurde, saada tema võti samamoodi järele. Kontrolli enne saatmist, et failinimi lõppeb `.pub`: kui saatsid kogemata privaatse poole, on see võti läbi ja tuleb teha uus.

Õppejõud paneb võtmed dropletisse ja saadab vastu **dropleti aadressi ja lingi**: nime, mis sellele aadressile viitab ja mille peal su leht käima hakkab. Vastuses on ka kasutajanimi. Siis:

```
ssh kasutajanimi@aadress
```

Esimesel korral küsib su arvuti, kas sa seda serverit usaldad. Vasta jah; edaspidi tunneb ta serveri ise ära ja ütleb, kui see on vahetunud.

Nüüd oled tühjas serveris. Kolm asja tehakse enne kõike muud, mitte pärast:

* Kontrolli, et paroolisisselogimine on keelatud ja igast arvutist, mille võtme sa saatsid, saab sisse.
* Tulemüür püsti nii, et lahti on ainult need pordid, mida sa päriselt kasutad. Iga lahtise pordi kohta pead oskama öelda, mis seal taga on. Jäta SSH port lahti, enne kui tulemüüri sisse lülitad, muidu sulged ukse enda järel.
* Uuendused peale.

Link viitab juba dropletile; seda sa ise seadistama ei pea. Kontrolli, et ta viitab sinna, kuhu peab: nimi ja aadress peavad kokku minema.

Siis HTTPS. Pöördproksi, mis võtab sertifikaadi ise. Ilma selleta käib su parool üle interneti lugemiskõlblikult, ja "aadressi ei tea keegi" ei ole parool.

Ja üks asi, mida teha kohe, mitte hiljem: **tee oma seadistus üks kord meelega uuesti**, ainult oma märkmete järgi. Kui märkmetest ei piisa, said sa just teada, mis neist puudu on — ja said selle teada praegu, kell kaks päeval, mitte siis, kui midagi päriselt katki läheb.

Kirjuta üles: dropleti aadress ja link; mis arvutite võtmed on sees ja mis kuupäeval lisatud; millised pordid on lahti ja mis iga ühe taga on; kuidas sa sisse saad; kaua võttis uuesti ehitamine ja mis märkmetest puudu oli.

#### 2. Postkontor

Dropletisse tuleb tavaline veebiserver. Tal on kaks külastajat ja kumbki tuleb ise.

**Kasutaja** avab lehe brauseris. Ta näeb, kas robot on kohal ja mis tema eelmisest sõnumist sai, ja saab jätta uue sõnumi. Sõnum on töö: joonista täht, näita pilti Atomi ekraanil, tõsta proovitükk allikast valmis pessa. Mis tööd nimekirjas on, otsustad sina.

**Roboti Atom** liitub labori WiFi-ga (seaded on Labori 1 lehel olemas) ja käib postil kindla vahe tagant. Iga korraga ütleb ta oma oleku ja küsib, kas talle on sõnumeid. Kui on, annab ta sõnumi jaamale edasi. Tee on sul Laborist 1 olemas: seesama kanal, mida mööda täht Atomist jaama läks. Jaam paneb roboti liikuma, ja kui töö on tehtud, viib Atom vastuse postkontorisse tagasi.

```
kasutaja → server:   {"job":"letter","arg":"K"}
Atom → server:       {"device":"team-2-atom","robot":"ready","p":-52.3}
server → Atom:       {"msg":17,"job":"letter","arg":"K","left":"14:02:10"}     või     {"msg":null}
Atom → jaam:         sama kanal, mis Laboris 1
Atom → server:       {"msg":17,"result":"done"}     või     {"msg":17,"result":"refused","why":"robot not enabled"}
```
```
iga N sekundi tagant: Atom → server: olek; vastuses on sõnum või ei ole midagi
kui sõnum: kas töö on nimekirjas? kas sõnum on piisavalt värske? kas robot on lubatud?
           kui jah → jaamale edasi → oota, kuni töö on tehtud → vastus serverile
           kui ei  → vastus serverile koos põhjusega, midagi ei liigu
kui server ei vasta: proovi uuesti pikema vahega, ekraanil märk, et ühendust ei ole
```

See on näide, mitte ettekirjutus. Formaadi lepid ise kokku ja kirjutad faili `docs/server_api.md`: iga aadress, kes seda kutsub, mis sisse läheb ja mis välja tuleb.

Neli asja ei ole vabatahtlikud.

**Sõnum on töö nimekirjast, mitte liigutus.** Postkontori kaudu ei saadeta koordinaate ega "liigu 10 mm vasakule". Kasutaja ei näe robotit ja tema sõnum jõuab kohale sekundeid hiljem; sellise viivitusega pimesi juhtida ei saa. Saab tellida töö, mille jaam oskab algusest lõpuni ise teha. Kõik muu lükatakse tagasi, ja vastus ütleb, miks.

**Sõnum aegub.** Kiri, mis jäeti postkontorisse eile õhtul, ei tohi täna hommikul robotit liikuma panna, kui keegi Atomi sisse lülitab. Otsusta, kui vana sõnum on veel kehtiv, ja mis vanaga juhtub. Proovi läbi: jäta sõnum, kui Atom on vooluta, oota üle piiri, lülita Atom sisse.

**Atom tõendab, kes ta on.** Server on avalik, ja igaüks, kes aadressi teab, võib öelda "mina olen robot" ja sõnumid ära viia. Atom saab võtme, mille ta iga kord kaasa annab. Võti elab Atomi lehe seadetes, mitte repos. HTTPS kehtib ka Atomi kohta: ta peab teadma, et räägib õige serveriga, mitte esimesega, kes vastab. Ja kasutaja leht on parooli taga, sest see leht paneb roboti liikuma.

**Test käib väljast.** Võta telefon, **lülita WiFi välja**, ava leht mobiilse andmesidega ja jäta sõnum. Kui robot teeb töö ära ja vastus ilmub lehele, on ahel olemas. Kui sa testid labori WiFi pealt, ei ole sa midagi testinud.

Siis mõõda. 30 sõnumit, iga kohta aeg kasutaja vajutusest roboti esimese liigutuseni. Tee seda kahe erineva küsimisvahega, näiteks 1 sekund ja 10 sekundit. Keskmine ja maksimum mõlemas, ja kõrvale see, mitu korda Atom tunnis postil käib. Lühem vahe on kiirem ja lärmakam; pikem on vaiksem ja aeglasem. Vali üks ja kirjuta põhjus välja. Pane kõrvale Labori 1 number, kus täht tuli otse Atomi nupult: vahe on postkontori hind.

Siis kaks katkestust, ja nad on erinevad.

**Ühendus kaob keset tööd.** Lülita ruuteri WiFi välja või tõmba dropleti kaabel, kui robot juba joonistab. Robot peab töö lõpuni tegema: kõik, mida ta vajab, on tal käes, ja pooleli jäänud täht ei ole ohutum kui valmis täht. Vastus ootab Atomis ja läheb teele, kui ühendus tagasi tuleb. Kolm korda, sest esimene kord võib vedada.

**Atom jääb vait.** WiFi kukub, keegi tõmbab kaabli välja. Postkontor ei saa sellest teada — keegi ei ütle talle. Ta saab ainult märgata, et keegi ei käi enam postil. Otsusta, kui kaua on "liiga kaua", ja mida kasutaja siis lehel näeb. Leht, mis võtab sõnumi vastu ja vaikib, kuigi robot ei ole kümme minutit kohal käinud, valetab. Tõmba Atom vooluta ja vaata, kas leht läks ausaks.

Kirjuta üles: lehe aadress; `docs/server_api.md`; lubatud tööde nimekiri ja mis juhtub sõnumiga, mida seal ei ole; kui vana sõnum veel kehtib ja mis juhtus aegunud sõnumiga; ekraanipilt telefonist, kus on näha, et WiFi on väljas; latentsuse tabel kahe küsimisvahega, keskmine ja maksimum, postilkäike tunnis, Labori 1 number kõrval; mis juhtus, kui ühendus kadus keset tööd; mida leht näitab, kui Atom on vait, ja mitme sekundi pärast.

#### 3. Kaamerad ja Atomi leht

Kaameraid on kaks ja neil on eri töö.

**Laua kaamera** on tavaline USB veebikaamera, UHD, posti otsas robotist kõrgemal. Ta käib USB-ga jaama külge. Kaadris on kogu laud: ruudustik servast servani, robot ja kõik hoidikud. Tema vastab küsimusele "mis seal päriselt juhtus" — kus käsi on, milline hoidik on tühi, kas midagi kukkus.

**Tööriista kaamera** on ESP32 kaameramoodul iminapa kõrval. Ta liigub käega kaasa ja näeb ainult otsikut ja seda, mis otse selle all on. Tema vastab küsimusele, millele laua kaamera ei vasta: kas napp on detaili keskel või serva peal. Ta ei ole USB-ga jaama küljes, vaid on omaette väike arvuti WiFi-s, nagu Atom. Vii ta samasse aadressiplaani, kuhu Atom Laboris 1 läks.

Mõlemad pildid tulevad jaama lehele kõrvuti. Jaama leht on labori võrgus ja sinna jäävad ka pildid: dropletisse kaamerapilti selles laboris ei saadeta. Tööriista kaamera oskab oma pilti ise välja anda, ja just seepärast on lihtne ta kogemata lahti jätta. Pildi toob jaam. Kaamera, mis on lahti kõigile, on kaamera sinu klassiruumis, mis on lahti kõigile.

UHD on rohkem, kui WiFi ja sülearvuti mugavalt kannavad. Laua kaamera täislahutus on mõeldud selleks, et pildi pealt midagi mõõta; vaatamiseks saadad sa väiksema pildi. Laboris 3 läheb seesama pilt läbi VPN-i ja seal on toru veel kitsam. Otsusta juba nüüd, kui väikeseks võib pilt minna, nii et ruudu nimi on pildilt veel loetav.

Mõõda kummagi kaamera kohta kolm asja: kui palju aega jääb sündmuse ja selle nägemise vahele, mitu kaadrit sekundis tuleb, ja kui palju ribalaiust see sööb. Siis mõõda **roboti juhtimise latentsus uuesti, mõlema kaamera töötamise ajal.** Kaamerad ja juhtimine käivad sama jaama ja sama võrgu kaudu ja kaamerad on neist kaugelt ahnemad. Kui latentsus kasvas, on sul valida: väiksem pilt, vähem kaadreid, üks kaamera korraga, või aeglasem juhtimine. Vali ja kirjuta põhjus välja.

Atomi leht: Labori 1 lubadus. Andmehõive Labor 2 pani Atomi külge rõhuanduri koos astmega. Sellele lehele tulevad nüüd juurde anduri seaded — kalibratsioonikonstandid, mis Andmehõives välja tulid — ja testinupp, mis näitab korraga toorest ADC lugemit, pinget ja kPa. Kolm numbrit kõrvuti sellepärast, et kui üks neist on vale, näed sa kohe, kumb pool valesti on: andur või valem. Samale lehele lähevad serveri aadress, Atomi võti ja küsimisvahe, ja testinupp, mis teeb ühe kõne ja näitab, mida server vastas. Uut lehte ei tehta.

Kirjuta üles: üks pilt kummastki kaamerast samal hetkel; kummagi lahutus, viide millisekundites, kaadreid sekundis, ribalaius; juhtimise latentsus ilma kaamerateta, ühega ja kahega; kuidas tööriista kaamera pilt jaamani jõuab; Atomi lehe seadete ja testide nimekiri failis `docs/atom_page.md`.

**KAARDISTA ISE — vastused.** Iga osa kohta: numbrid, ühikud, kus fail on. Tegemata asja kohta üks rida, miks.

### Ohutus

Selles laboris muutub ohutus teistsuguseks, kui ta seni oli. Seni pani roboti liikuma inimene, kes oli samas ruumis. Nüüd võib seda teha sõnum, mille jättis keegi, keda ruumis ei ole ja kes robotit ei näe.

* **Enne, kui postkontor esimest korda robotit liigutab, lepite meeskonnas kokku ja kirjutate faili:** kes tohib sõnumeid jätta, ja mida ta peab enne seda tegema.
* **Hädastopp on roboti alusel.** Kodus seda nuppu ei ole. Seega: robot võtab sõnumeid vastu ainult siis, kui ruumis on inimene, kes hädastoppi ulatub ja kes on roboti ise lubanud. Kui ruumis ei ole kedagi, on robot välja lülitatud, mitte ainult keelatud. Lubamist postkontori kaudu ei tehta.
* **Sõnum on töö nimekirjast.** Koordinaate, kiirust ega pumba otsejuhtimist postkontori kaudu ei saadeta. Iga töö nimekirjas on enne laboris kohapeal läbi proovitud, 20 % kiirusel.
* **Aegunud sõnum ei liiguta midagi.** Robot, mis hakkab sisselülitamisel eilset kirja täitma, liigub siis, kui keegi seda ei oota.
* **Avalik server on avalik.** Aadress, mida keegi ei tea, ei ole parool — aadresse skaneeritakse pidevalt ja automaatselt. Parool, HTTPS, ja lahti ainult need pordid, mida sa kasutad.
* **Postkontor ei helista robotile.** Server ei tea roboti aadressi ja tal ei ole teed labori võrku. Ainus suund on see, et Atom tuleb ise.
* **Sõnum on võõra käest tulnud sisend.** Pildil on suuruse ülempiir ja ta on pildifail; tähel on üks täht; server ega jaam ei käivita midagi, mis sisse tuli.
* **Atomi võti ei ole repos.** Kui ta sinna sattus, on ta avalik: tee uus.
* **Privaatne SSH võti ei lahku sinu arvutist.** Ei meili, ei vestlusse, ei reposse. Õppejõule läheb ainult fail, mille nimi lõppeb `.pub`.
* Kaamerapildid jäävad labori võrku. Kaamera, mis näitab klassiruumi avalikul lehel, näitab inimesi, kes ei ole selleks luba andnud.
* MG400 reeglid Laborist 1 kehtivad edasi: käed ei ole laual, kui robot on sisse lülitatud; uue jada esimene jooks 20 % kiirusel; käsklusi saadab robotile korraga ainult üks programm.
* Kui Atom laborist välja läheb, vaheta WiFi parool vaikimisi omast ära.

### Komponendid selle labori jaoks

Droplet ja link tulevad õppejõult. Neid sa oma tellimusse ei pane.

Sinu tellimusse läheb see, mis laua juures puudu on. Tellimus läheb välja 16.10.26, faili `docs/bom.md`, iga rea juures üks lause, milline osa seda küsib.

Tellimine käib ühisest tellimistabelist: [https://moodle.ut.ee/mod/url/view.php?id=1535601](https://moodle.ut.ee/mod/url/view.php?id=1535601). Kanna oma read sinna enne tellimise kuupäeva; mida tabelis ei ole, seda ei tellita. Fail `docs/bom.md` jääb sinu reposse põhjenduseks, miks sa just neid asju küsisid.

Mõtle näiteks: kas veebikaamera näeb piisavalt laia kaadrit sellelt kõrguselt, kuhu post ta viib; kas USB kaabel ulatub posti otsast jaamani; ja kas kaameramoodul on olemas ning kas labori WiFi ulatub temani ja Atomini, kui nad on laua peal ja käe otsas.

### Hindamiskriteeriumid

| Kategooria | Punktid |
| :--- | :--- |
| Tööfailid — dropleti seadistus kirjas ja korratav, serveri kood, Atomi püsivara postilkäimisega, jaama kood, kahe kaamera vood, Atomi lehe uued osad | 5 p |
| Analüüs — latentsus sõnumist liigutuseni kahe küsimisvahega ja Labori 1 numbri kõrval, kummagi kaamera viide, kaadrisagedus ja ribalaius, juhtimise latentsus kaameratega ja ilma | 5 p |
| Prototüüp — leht avaneb telefonist mobiilse andmesidega HTTPS-i peal, sõnum paneb roboti tööd tegema ja vastus tuleb tagasi, aegunud ja lubamata sõnum ei liiguta midagi, leht näitab ausalt, kui Atom on vait, üks kaamera näitab kogu lauda ja teine otsikut | 5 p |
| Dokumentatsioon — README, arenduspäevik, `server_api.md`, `atom_page.md`, ohutuskokkulepe, `bom.md`, AGENTS.md | 5 p |
| **Kokku** | **20 p** |

### Kaitsmine

Link git repole, tag `smart-solutions-lab2`.

Kaitsmine on lihtne suuline 15 minuti jutuajamine. Avad oma telefonist mobiilse andmesidega lehe, jätad sõnumi, robot joonistab tähe ja vastus ilmub lehele. Jätad sõnumi, mida nimekirjas ei ole, ja näitad, mis sellest sai. Tõmbad Atomi vooluta ja näitad, mida leht siis ütleb. Näitad jaama lehel mõlemat kaamerat — kogu lauda ühes ja otsikut teises. Avad oma arenduspäeviku. Õppejõud küsib umbes viis küsimust selle kohta, kuidas sa selle tegid. Kui esimesel korral ei õnnestu, tuled uuesti.

Repos on kaustas `smart-solutions/lab2/`:

* `server/` dropletis jooksev veebiserver
* `src/` jaama kood koos kaamerate voogudega
* `firmware/` Atomi PlatformIO projekt postilkäimise ja uuendatud lehega
* `docs/`: dropleti ehitus samm-sammult, ahela skeem draw.io-s, `server_api.md`, `atom_page.md`, ohutuskokkulepe, latentsuse CSV-d, ekraanipildid ja fotod, `bom.md`
* `README.md` selle labori kohta
* `AGENTS.md` uuendatud

### Arenduspäevik

**KAARDISTA ISE — päevik.** Üks sissekanne iga töösessiooni kohta, kirjutatud iseendale, nii et inimene, kes seal ei olnud, saab aru. Sissekandeid lisatakse, mitte ei muudeta.

**PP.KK.AA — kes olid kohal**
* Tegime:
* Juhtus (numbrid):
* Otsustasime, ja miks:
* Lahti järgmiseks korraks:

### Väljundid ja tulemused

**Väljundid**
* Andmehõive L2: Atomi leht, kust anduri lugemit, seadeid ja testi näeb.
* 3D printimine L2: kaks pilti — üks, mille pealt näeb, kus käsi laual on, ja teine, mille pealt näeb, kas napp tabab pesa.
* Nutikad Lahendused L3: droplet, mille külge tuleb VPN, ja kaks kaamerapilti, mis lähevad sealt läbi. Postkontor on valmis; otsetee tuleb järgmisena.

**KAARDISTA ISE, lõpus.**
* Git repo ja tag:
* Numbrid, mille see labor andis, ühikutega:
* Mida me teeksime teisiti:
* Mida järgmine labor peaks enne alustamist teadma:

### Tagasiside