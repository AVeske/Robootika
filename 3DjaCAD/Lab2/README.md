## 3D printimine ja CAD: Labor 2 — Sisend, töökoht, väljund

**Töömaht:** 30 tundi | **Hindamine:** 20 punkti | **Meeskond:** 3 tudengit | **Välja antud:** 06.10.26 | **Tellimise kuupäev:** 16.10.26 | **Esimene kaitsmine:** 27.10.26, veebis

### Kuidas see dokument töötab

* Repo ja töökord on Laborist 1 olemas ja samad.
* Too sellest dokumendist oma projekti repo juurde see, mida vaja: selle labori kaust, `README.md`, kuhu lähevad su enda numbrid, otsused ja KAARDISTA ISE vastused, ja failid, mida kontrollnimekiri nimetab. Tervet dokumenti üle kopeerida ei ole vaja.

### Eesmärk

Töölaua annab õppejõud ja selle disain on olemas: Fusioni fail [MG 400 rakis.f3z](MG%20400%20rakis.f3z) ja selle kirjeldus [MG 400 rakis.md](MG%20400%20rakis.md). Laud on PLA-st prinditud. Robot seisab oma aluses ja tema ees on **Gridfinity ruudustik**, 7 × 10 ruutu, samm 42 mm. Kõik, mis laua peal elab, on Gridfinity hoidik, mis kukub ruudustikku. See ruudustik on ainus liides, mille vastu sa disainid.

Aasta lõpuks paneb MG400 kokku sildi: AtomS3 (ESP32), mille ekraani peale on liimitud polükarbonaatklaas ja mille all on akumoodul. See on väike tootmisliin, ja tootmisliinil on alati sama kuju:

* **Sisend.** Mitu objekti ja igaühte mitu ühikut. Meil on objekte kolm: AtomS3, polükarbonaatklaas ja akumoodul.
* **Töökohad.** Neid on nii palju, kui protsessis on samme, mida üks robot korraga teeb.
* **Väljund.** Tavaliselt kaks: põhiväljund ja praak. Võib olla ka rohkem, kui valmis asju sorteeritakse eraldi kastidesse.

See labor teeb hoidikud kõigi kolme jaoks. Ja neid kohti ei õpetata robotile iga kord uuesti: hoidik tuleb ruudustikust välja ja läheb tagasi, ning detail on ikka samas kohas.

Laboris 1 mõõtsid sa ära, mis lõtk sellel printeril päriselt on. Nüüd läheb see number käiku kaks korda: hoidiku jalg ruudustikus ja detail pesas.

Selles laboris on viis asja:

1. **Protsess ja paigutus.** Mis on sisendid, mitu töökohta, mitu väljundit ja millises ruudus igaüks on.
2. **Hoidikud.** Sisendhoidikud, töökoha hoidik, väljundhoidikud. Kõik Gridfinity jalaga.
3. **Test.** Ainult klaas: sisendist töökohale ja töökohalt valmis asjade väljundisse. Siis hoidikud välja ja tagasi, ja uuesti.
4. **Kaamera tööriistahoidikul.** Iminapa kõrvale käib ESP32 kaameramoodul, ja ta peab kuskilt toite saama.
5. **Kaamera laua kohal.** Tavaline USB veebikaamera robotist kõrgemal, nii et ta näeb kogu lauda.

Esimesel päeval uusi osi ei ole. Ehita sellest, mis riiulil on, ja kirjuta puuduv tellimuseks, mis läheb välja 16.10.

*See on elav dokument. Uuenda eesmärke, kui need töö käigus muutuvad — uued teadmised teevad vanad eesmärgid vahel mõttetuks. Mõte on hoida meeskond kogu aeg sihil, et ei eksitaks detailide metsa ja põhiprobleem ei jääks lahendamata.*

**KAARDISTA ISE — eesmärk nii, nagu ta tegelikult välja tuli.**

### Kontrollnimekiri

**Peab olema tehtud**

- [ ] Detailid mõõdetud nihikuga: AtomS3, klaas, akumoodul. Fusionis parameetritena.
- [ ] Protsess ja paigutus kirjas: sisendid, töökohad, väljundid, iga hoidiku ruut (näiteks B-2). Failis `docs/layout.md` koos joonisega.
- [ ] Kalibreerimishoidik 1 × 1 prinditud, istub ruudustikus ja ei loksu.
- [ ] Sisendhoidikud valmis: AtomS3, klaas, akumoodul. Igaühes vähemalt neli ühikut.
- [ ] Töökoha hoidik valmis: Atom saab seal olla ainult ühte moodi ja klaasil on tema peal kindel koht.
- [ ] Väljundhoidikud valmis: põhiväljund neljale ja praak.
- [ ] Test tehtud: neli klaasi sisendist töökohale ja töökohalt väljundisse, hoidikud vahepeal välja ja tagasi. Tulemus failis `docs/refit_test.csv`.
- [ ] Kaamera kinnitus valmis: kaameramoodul istub olemasoleva iminapa tööriistahoidiku küljes, näeb töökohta ja ei jää napale ette.
- [ ] Kaamera toide otsustatud ja läbi proovitud: käsi käib oma liikumise läbi ja juhe ei jää kuhugi kinni.
- [ ] Veebikaamera kinnitus valmis: kaamera on robotist kõrgemal, näeb kogu lauda ja käsi ei ulatu temani.
- [ ] Tellimus 16.10: mis selle labori jaoks puudu jäi, failis `docs/bom.md`.
- [ ] Repo ja arenduspäevik täidetud, tag `3d-print-lab2`.

**KAARDISTA ISE — kuupäevad ja sinu enda sammud.**

### Sisendid

* Õppejõult: töölaud koos disainiga. Fusioni fail [MG 400 rakis.f3z](MG%20400%20rakis.f3z) ja kirjeldus [MG 400 rakis.md](MG%20400%20rakis.md). Lühikokkuvõte allpool, osas "Töölaud".
* Riiulilt: printerid, PLA, nihik.
* 3D printimise L1-st: lõtk, paindumise ja murdumise numbrid, pastakahoidik.
* Nutikate Lahenduste L1-st: jaam, millega punkte õpetada ja üle mängida, ja `data/positions.json`.
* Andmehõive L1-st: iminapp ja pumba juhtimine käsurealt — sellega käib tõstmise test.
* Olemasolev iminapa tööriistahoidik roboti flantsi küljes. Kaamera käib selle külge.

### Vahendid

1. Fusion 360, hariduslitsents
2. PrusaSlicer, labori printerid, PLA
3. Nihik, 300 mm joonlaud
4. MG400 koos baaspaketi, pumbakasti ja iminapaga
5. Töölaud Gridfinity ruudustikuga
6. Polükarbonaatklaasid 24 × 24 × 2 mm, vähemalt neli; prinditud Atomi mannekeen 24 × 24 × 13 mm töökohale; AtomS3 ja akumoodul mõõtmiseks
7. Seeed Studio XIAO ESP32S3 Sense kaameramoodul (tootekood 113991115)
8. USB veebikaamera (UHD), USB pikenduskaabel
9. Git, üks repo meeskonna kohta, `AGENTS.md` juurkaustas

*Kui plaan muutub, uuenda ka vahendeid, või tee draw.io skeem, mis näitab, kuidas asjad omavahel töötavad.*

**KAARDISTA ISE — mida sa päriselt kasutasid.**

### Taustainfo

* **Gridfinity: mis see on**
  [https://www.youtube.com/watch?v=ra_9zU-mnl8](https://www.youtube.com/watch?v=ra_9zU-mnl8)
* **Gridfinity hoidik Fusionis, parameetritega**
  [https://www.youtube.com/watch?v=h8Asgw8fsVE](https://www.youtube.com/watch?v=h8Asgw8fsVE)
* **Parameetrid Fusionis**
  [https://www.youtube.com/watch?v=tx89UXMeqwQ](https://www.youtube.com/watch?v=tx89UXMeqwQ)
* **Komponent vs keha**
  [https://www.youtube.com/watch?v=L6MMw-dfS8s](https://www.youtube.com/watch?v=L6MMw-dfS8s)
* **Kas detailid lähevad üksteisest läbi (Interference)**
  [https://www.youtube.com/watch?v=wy6chd2hP24](https://www.youtube.com/watch?v=wy6chd2hP24)
* **Kuidas detail paika panna: 3-2-1 reegel**
  [https://www.youtube.com/watch?v=pwSnycGvHAg](https://www.youtube.com/watch?v=pwSnycGvHAg)
* **Karp ümber plaadi (Fusioni projekt RPI Pico Box)**
  [https://www.youtube.com/watch?v=wt1nlLSl8TQ](https://www.youtube.com/watch?v=wt1nlLSl8TQ)
* **Suur detail tükkideks ja tükid kokku**
  [https://www.youtube.com/watch?v=-PtARBZEu5g](https://www.youtube.com/watch?v=-PtARBZEu5g)
* **Tugevus risti kihtidega**
  [https://www.youtube.com/watch?v=cC5KlelZlx4](https://www.youtube.com/watch?v=cC5KlelZlx4)
* **Infill**
  [https://www.youtube.com/watch?v=nV3GbN6hLjg](https://www.youtube.com/watch?v=nV3GbN6hLjg)
* **MG400 flants**
  [https://a360.co/4nruicX](https://a360.co/4nruicX)

*Lisa siia oma allikaid ja kasulikku infot, mis aitaks sul projektist aru saada ka aastaid hiljem, kui selle uuesti lahti teed.*

**KAARDISTA ISE — sinu allikad.**

### Töölaud

Siin on see, mida sul hoidiku disainimiseks vaja on. Kõik ülejäänu, ka iga ruudu koordinaadid tabelina, on failis [MG 400 rakis.md](MG%20400%20rakis.md).

Seda kirjeldust on hea kasutada oma AI agendile seletamiseks, mis Fusionis praegu juba tehtud on. Agent ei näe Fusioni faili sisse; kirjeldus ütleb talle sõnade ja numbritega sama, mida [MG 400 rakis.f3z](MG%20400%20rakis.f3z) ütleb sulle pildina: kus on robot, kus on ruudustik, mis mõõdud ja mis koordinaadid. Pane see oma repo juurde ja viita sellele `AGENTS.md`-st, siis ei pea sa lauda igas vestluses uuesti kirjeldama.

**Miks Gridfinity**

Laua liides oleks võinud olla ka midagi muud: alumiiniumprofiil, augurida, oma välja mõeldud tapid. Gridfinity sai valitud kolmel põhjusel.

* **Ta on algusest peale mõeldud 3D printimiseks.** Jala kuju on 45° kalded ja püstsein, mis prinditakse ilma tugedeta ja mis juhivad hoidiku ise oma kohale. Seda ei ole metallitööst printerile ümber tõlgitud.
* **Tal on suur kogukond.** See tähendab palju valmis näiteid, generaatoreid ja teeke, ja see tähendab ka, et sinu agent tunneb seda standardit hästi ja oskab aidata. Oma välja mõeldud liidese kohta ei tea ta midagi.
* **Tema täpsusest piisab selle roboti jaoks.** Hoidik tuleb ruudustikus tagasi mõne kümnendiku millimeetri sisse. Iminapa ja 24 mm klaasi jaoks on seda küllalt, kui pesal on kaldserv. Kui palju täpselt, mõõdad sa osas 3 ise üle.

**Kolm tsooni, kõik ühel tasasel pinnal**

* **Roboti alus.** Süvend, mille sein on 20° kaldega. Kui robotit lükata, ronib ta kallakust üles ja libiseb välja; tagasi lükates kukutab raskusjõud ta täpselt samasse kohta. Siia ei disaini sa midagi: ei süvendisse ega kallaku peale.
* **Ruudustik.** Gridfinity alusplaat roboti ees, 7 ruutu sügav × 10 ruutu lai, samm 42 mm, kokku 294 × 420 mm.
* **Kaabliruum ruudustiku all.** Ruudud on alt lahti ja iga seina all on kaar 24 × 12 mm. Selles laboris sul kaableid ei ole, aga järgmistes on, nii et ära ehita hoidiku põhja kinni, kui selleks põhjust ei ole.

**Ruutude nimed**

Ruudu nimi on täht ja märgiga number, näiteks `B-2` või `E+3`.

* **Täht on kaugus robotist.** A on robotile kõige lähemal, G kõige kaugemal.
* **Number on külg.** Nulljoon jookseb laua keskelt, roboti J1 teljest otse ette, ja jääb kahe ruudu vahele: ruutu 0 ei ole. +1 … +5 on robotist vaadates paremal, −1 … −5 vasakul. Kui seisad laua ees näoga roboti poole, on pluss sinu vasakul käel.
* Nii saab lauda hiljem suuremaks teha, ilma et ükski nimi muutuks: laiem laud saab ±6, sügavam saab H, ja kui ruute tuleb A-st roboti poole, saavad need miinusega tähe.
* Ruudu keskpunkt, mudeli koordinaatides, nullpunkt roboti J1 teljel:
  `x = −139,5 − 42 · täht`, kus A = 0 … G = 6
  `y = 42 · number − 21`, kui number on plussiga, ja `y = 42 · number + 21`, kui miinusega
* Roboti enda koordinaadid on eeldatavasti samad, pööratud 180° ümber Z. Seda ei ole kontrollitud, nii et kalibreeri (vaata osa 2).

**Kuhu robot ulatub**

| Kaugus J1 teljest | Ruudud | Milleks |
| :--- | :--- | :--- |
| kuni 300 mm | tähed A–C, numbrid −3 … +3 | kõige täpsem; siia käib töökoht |
| 300–400 mm | ülejäänud | sisend ja väljund |
| üle 400 mm | G-5, G-4, G-3, G+3, G+4, G+5 | väldi |

Tavaline paigutus: sisend ühel pool (numbrid −5 … −3), töökoht keskel (numbrid −2 … +2, tähed A–C), väljund teisel pool (numbrid +3 … +5). Käsi liigub siis läbi protsessi ühes suunas.

**Hoidik on Gridfinity kast**

* Välismõõt 42 · n − 0,5 mm, ehk ühe ruudu hoidik on 41,5 mm. Välisnurga raadius 3,75 mm.
* Jalg on standardne Gridfinity jalg, 4,75 mm kõrge. Võta see valmis generaatorist või teegist; ära joonista seda silma järgi.
* Mitme ruudu hoidik (2 × 1, 2 × 2, 3 × 2) on lubatud ja jäigem. Üks prinditud tükk kuni 250 × 250 mm.
* Soovi korral 6 × 2 mm magnetid jala sisse.
* Ruudustiku pealispind on 24 mm laua pinnast ja 7,28 mm roboti talla tasapinnast kõrgemal. Hoidiku jala ülaserv jääb umbes 0,1 mm ruudustiku pinnast kõrgemale. Mõõda päris laua peal üle, enne kui Z-i usaldad.
* Kõrged osad (üle 60 mm) ei käi sinna, kust käsi üle liigub. Roboti poolses küljes kõrget seina ei ole.

**Numbrid, mis disaini piiravad**

* Robot kordab oma asendit ±0,05 mm. Laud tervikuna (alus, prinditud osad, Gridfinity istuvus) kordab umbes ±0,3–0,5 mm. Nulllõtkuga pesa ei tööta: detail juhitakse sisse kaldservaga.
* Robot tõstab 500 g koos tööriistaga.
* Kokkupõrke tuvastus peatab käe umbes 12 N juures.
* Laua õppetund: suured täis PLA-klotsid kaarduvad. Hoidik on õõnes või ribidega, üle 20 mm paksust täismassi ei ole, ja üle 150 mm tükil on äär (brim).

### Osad

#### 1. Protsess ja paigutus

Enne kui Fusioni avad, joonista protsess paberile. Kolm küsimust.

**Mis tuleb sisse?** Sisend on mitu objekti ja igaühte mitu ühikut. Meil: AtomS3, polükarbonaatklaas, akumoodul. Iga objekt saab oma sisendhoidiku ja igas on mitu ühikut — selles laboris vähemalt neli. Mõõda kõik kolm nihikuga. Testis käib läbi ainult klaas, aga hoidikud teed sa kõigile kolmele. Akumooduli mõõte see dokument sulle ei anna.

**Mitu töökohta?** Töökohti on nii palju, kui protsessis on samme, mida üks robot korraga teeb. Kirjuta sildi kokkupanek sammudena välja ja otsusta iga sammu kohta, kas ta vajab oma kohta või saab eelmisega sama kohta jagada. Selle labori testi jaoks piisab ühest töökohast. Aga paigutus peab näitama, kuhu ülejäänud tulevad.

**Kuhu läheb välja?** Väljundeid on tavaliselt kaks: põhiväljund ja praak. Kui valmis asju sorteeritakse (näiteks eri tellimused eri kasti), on neid rohkem. Praak ei ole erand, millele hiljem mõelda: kui praagil kohta ei ole, jääb ta töökohale ja liin seisab.

Siis pane igaüks ruutu. Töökoht käib sinna, kus robot on kõige täpsem. Sisend ja väljund võivad olla kaugemal. Mõtle roboti tee läbi: kaks hoidikut, mille vahel käsi risti üle kolmanda käib, ei ole hea paigutus. Ja vaata, kas kogu asi mahub 70 ruutu ära nii, et järgmiste laborite moodulitele jääb ruumi.

Kirjuta üles: protsessi sammud; mitu töökohta ja miks; mitu väljundit ja mis kuhu läheb; iga hoidiku ruut ja suurus ruutudes; iga detaili mõõdud nihikuga; joonis ülaltvaates. Fail `docs/layout.md`.

#### 2. Hoidikud

Esimene print on kõige väiksem: **kalibreerimishoidik**, 1 × 1, keskel terav tipp või rist. Ta teeb kaks tööd. Esiteks näitab ta, kas sinu Gridfinity jalg istub selles ruudustikus sinu printeri ja Labori 1 lõtkuga — enne kui prindid midagi suurt. Teiseks kalibreerid sa temaga roboti:

1. Pane ta ruutu B-2.
2. Vii tööriista tipp jaamaga tema keskpunkti ja kirjuta roboti koordinaadid üles.
3. Nihe = mõõdetud − arvutatud (valem osas "Töölaud").
4. Kontrolli ühte kauget ruutu, näiteks E+3. Kui viga on üle 1 mm, on telgede suund valesti eeldatud, mitte sinu hoidik vale.
5. Z: puuduta ühe korra ruudustiku pealispinda.

Sealt edasi kirjutad iga koha üles kujul **ruut + nihe**, mitte paljaste koordinaatidena.

Siis kolm hoidikutüüpi. Igaühel on teine töö.

* **Sisendhoidik** annab detaili robotile kätte kohas, mis on teada ja ei muutu. Pesa lõtkuga 1–2 mm ja 45° kaldservaga ülal. Üks kindel baas (nurk või keskpunkt), mille järgi robot võtab. Võib olla ka virn või kallak, kust detailid ise ette libisevad, nii et võtmise punkt on alati sama.
* **Töökoha hoidik** hoiab detaili paigal, kui robot temaga midagi teeb. Detail toetub kolmele punktile või kahele servale ja põhjale, nii et ta saab olla ainult ühte moodi. Hoidik peab roboti survele vastu, paar njuutonit. Ülevalt on tööriistale vaba tee. Ja hoidiku baas on selline, mida on lihtne robotiga puudutada.
* **Väljundhoidik** võtab valmis detaili vastu. Robot paneb ebatäpsemalt, kui võtab, nii et kaldservad on siin suuremad. Praagi jaoks võib see olla lihtsalt kast või renn, kuhu detail kukub.

Pesa lõtk tuleb Labori 1 kuubist. Kirjuta üles, millise numbri sa võtsid ja miks just selle. Pane tähele, et sisendi, töökoha ja väljundi lõtk ei pea olema sama number: mida täpsemalt koht peab detaili hoidma, seda väiksem lõtk ja seda suurem kaldserv.

Igal pesal on kolm nõuet:

* **Sissejuhtiv kaldserv.** Robot ei pane detaili täpselt keskele. Kaldserv parandab paari kümnendiku vea ise ära; ilma selleta jääb detail serva peale seisma.
* **Inimene saab ligi.** Sisendi laeb inimene ja väljundi tühjendab inimene. Kaks millimeetrit paks klaas siledas pesas on sõrmedega võimatu välja võtta. Väljalükkeauk põhjas, väljalõige servas või madalam pesa — sinu valik. Proovi ise järele, enne kui otsustad, et küll saab.
* **Peale midagi ei ulatu.** Iminapp tuleb otse alla. Kõik, mis detailist kõrgemale jääb, on tee peal.

Atom käib igas pesas ekraan ülespoole. Töökohal jäävad USB-C ja nupp ligipääsetavaks.

Kirjuta üles: kas Gridfinity jalg istus esimese korraga ja mida sa muutsid; kalibreerimise nihe ja kauge ruudu viga; iga pesa lõtk ja Labori 1 number, mille pealt see tuli; iga pesa mõõdetud nihikuga, nominaal kõrval; mis läks esimese prindi juures valesti ja mis selle parandas; foto hoidikutest ruudustikus ülevalt, joonlaud kaadris.

#### 3. Test

Enne kui oma hoidikuid testima hakkad, vaata ära, kuidas laud ise sama probleemi lahendab. Robot seisab kaldseinaga aluses: sinna on täpselt üks viis istuda, ja seetõttu tuleb roboti asend ruudustiku suhtes iseenesest tagasi — mitte tarkvarast, vaid geomeetriast. Gridfinity jalg teeb hoidikuga sama asja väiksemalt. Selle labori küsimus on, kui hästi.

Test käib ainult klaasiga. Klaas on kolmest detailist kõige raskem tõsta: õhuke, sile ja kerge. Kui klaas käib läbi, käivad ülejäänud ka.

**Läbijooks.** Lae klaasi sisendhoidikusse neli klaasi. Töökohal istub Atomi mannekeen. Õpeta jaamaga punktid. Robot võtab klaasi sisendist, paneb töökohale mannekeeni peale, võtab sealt uuesti ja viib valmis asjade väljundisse. Neli tükki järjest, inimene vahepeal midagi ei puuduta. Liimi selles laboris ei ole, nii et klaas ei ole mannekeeni küljes kinni: edasi tõstetakse ainult klaas ja mannekeen jääb töökohale.

**Välja ja tagasi.** Võta kõik hoidikud ruudustikust välja, pane tagasi, lae klaasid uuesti sisendisse ja mängi sama jooks üle. Punkte vahepeal ei muudeta. Viis ringi, kokku kakskümmend klaasi.

Kui mõni kord ei õnnestu, on see kõige kasulikum rida terves tabelis. Kirjuta üles, mis juhtus: kas napp võttis servast, kas klaas jäi kaldserva peale või nihkus töökohal paigast, kas hoidik loksus ruudus. Viimane ütleb sulle, et jala lõtk on liiga suur või et sul on magneteid vaja.

Siis teine küsimus: kas samad õpetatud punktid töötavad ka siis, kui hoidik on teises ruudus ja punktile on liidetud täisarv samme, 42 mm korda ruutude arv? Kui töötavad, on sul standard: hoidiku võib panna ükskõik kuhu ja robot teab, kus detail on. Kui ei tööta, kirjuta üles, kui palju mööda läks.

Kirjuta üles: read failis `docs/refit_test.csv` (ring, klaasi number, kas võttis sisendist, kas pani töökohale, kas võttis töökohalt, kas pani väljundisse, märkus); mitu kahekümnest läks läbi; kui palju detail nihkus, kui sa seda nihikuga või kaameraga mõõta saad; kas teise ruutu tõstetud hoidik töötas arvutatud punktiga. See viimane number ütleb, kui palju lõtku järgmised laborid peavad taluma — kirjuta ta eraldi välja.

#### 4. Kaamera tööriistahoidikul

Järgmistes laborites peab robot nägema, mida ta tõstab. Selleks käib iminapa kõrvale kaamera: Seeed Studio XIAO ESP32S3 Sense, tootekood 113991115. See on pöidlaküüne suurune ESP32 plaat, mille peal on kaameralaiend ja USB-C pesa.

Uut tööriistahoidikut sa ei tee. **Kaamera käib olemasoleva iminapa tööriistahoidiku külge.** Flants, napp ja voolik jäävad sinna, kus nad on, ja jaamaga õpetatud punktid kehtivad edasi. Sinu osa on tükk, mis kinnitub olemasoleva hoidiku külge ja hoiab kaamerat.

Mõõda enne joonistamist kaks asja nihikuga: moodul ise (plaat, kaameralaiend, objektiiv, USB-C pesa asukoht, antenn) ja olemasolev hoidik — kust saab kinni haarata ja mis pinnad on vabad. MG400 flantsi mudel on Taustainfos.

Mida kinnitus peab tegema:

* **Kaamera näeb töökohta.** Otsusta, kas ta vaatab otse alla või nurga all, ja kui kõrgel napp peab olema, et terve klaas ja Atom tema all oleksid pildis ja terav. Proovi see käes hoides järele, enne kui nurga mudelisse lukku paned.
* **Napp jääb vabaks.** Kaamera ega tema kinnitus ei ulatu napa otsast allapoole ega lähe hoidiku seinte vastu, kui napp pesasse laskub. Osa 2 reegel "peale midagi ei ulatu" kehtib nüüd ka tööriista enda kohta.
* **Kaamera on iga kord samas kohas.** Kui moodul võetakse välja ja pannakse tagasi, vaatab ta sama punkti. See on sama küsimus, mis hoidikul ruudustikus, ja sama vastus: kuju, mis lubab ainult ühte asendit, mitte hõõrdumine.
* **Moodul tuleb kätte.** USB-C pesa on ligipääsetav ja mooduli saab välja ilma midagi murdmata. Plaat läheb soojaks; ära ehita teda PLA sisse kinni.
* **Kaal.** Robot tõstab 500 g koos tööriistaga. Kaalu tööriist enne ja pärast.

**Kust kaamera toite saab?** See on selle osa päris küsimus, sest kaamera on käe otsas ja käsi liigub. Kolm suunda, igaühel oma hind:

* **USB-C juhe mööda kätt.** Lihtsaim. Aga juhe peab kaasa tulema, kui käsi sirutub välja ja J4 pöörab. Kus ta on kinnitatud, kui palju on lõtku, ja mis juhtub pistikuga, kui juhe pingule läheb?
* **Aku kaamera juures.** Juhet ei ole. Aga aku on kaal käe otsas, ta saab tühjaks, ja ta peab kuhugi ära mahtuma.
* **Roboti enda toide käe otsast.** MG400 käe otsas on pistik tööriista jaoks. Vaata järele, mis pinge sealt tuleb ja mida moodul talub, enne kui midagi ühendad. Vale pinge on katkine moodul.

Vali üks, ehita see valmis ja proovi läbi: käsi käib sisendist töökohale ja väljundisse, J4 pöörab oma vahemiku läbi, ja juhe ei jää hoidikute ega käe enda taha kinni. Juhtme kinnitus ja tõmbetõke on osa sinu printidest, mitte kleeplint.

Kirjuta üles: mooduli ja olemasoleva hoidiku mõõdud; kuidas kinnitus hoidiku küljes kinni on; kaamera nurk ja kõrgus, mille pealt töökoht pildis on; tööriista kaal enne ja pärast; millise toite sa valisid ja miks, ning mis kahest ülejäänust loobuma pani; foto tööriistast küljelt ja üks kaamera enda pilt töökohast.

#### 5. Kaamera laua kohal

Tööriista kaamera näeb otsikut lähedalt ja mitte midagi muud. Selleks, et näha, kus käsi on ja mis laual toimub, on vaja teist kaamerat: tavaline USB veebikaamera, UHD, mis on **robotist kõrgemal ja näeb kogu lauda** — ruudustik ühest servast teiseni ja robot ise. Kaks kaamerat, kaks tööd: üks näeb kõike, teine näeb täpselt.

Sinu osa on kinnitus, mis ta sinna üles viib. Mõõda enne joonistamist kolm asja:

* **Kui kõrgele käsi käib.** Sõida jaamaga käsi kõige kõrgemasse ja kõige kaugemasse asendisse ja mõõda joonlauaga. Kaamera ja kõik, mis teda hoiab, on sellest väljas.
* **Kui kõrgel peab kaamera olema, et kogu laud kaadrisse mahuks.** Ruudustik on 294 × 420 mm ja selle taga on robot. Hoia kaamerat käes laua kohal ja vaata pilti, enne kui kõrguse mudelisse kirjutad. Kaamera vaatenurk otsustab selle, mitte sinu soov.
* **Kuidas kaamera kinni käib.** Statiivikeere, klamber või lihtsalt kuju. Mõõda oma kaamera pealt.

Siis otsusta, kus kinnitus seisab. Ta võib olla Gridfinity hoidik ruudustikus: nurgaruudud G-5 ja G+5 on roboti ulatuse piiril ja detailide jaoks nagunii halvad. Ta võib käia ka laua serva külge. Mida ta teha ei või: seista roboti aluse peal või selle vastas, ja olla seal, kust käsi läbi käib.

Kõrge ja peenike PLA-post on vedru. Kui robot liigub ja laud väriseb, väriseb ka pilt, ja Nutikate Lahenduste labor peab selle pildi pealt midagi mõõtma. Jäikus tuleb kujust, mitte täitest: lai jalg, ribid, kolmnurk. Ja post, mis on printeri lauast pikem, prinditakse tükkidena — mõtle läbi, kuidas tükid kokku käivad, nii et ühendus ei oleks kõige nõrgem ja kõige loksuvam koht. Labori 1 murdumise number ütleb sulle, mis suunas kihid käima peavad.

Kaks nõuet veel. Kaamera tuleb **samasse kohta tagasi**, kui kinnitus maha võetakse ja tagasi pannakse, sest pildi ja laua vaheline seos õpetatakse ühe korra. Ja USB juhe jookseb mööda posti alla ja on kinni; ta ei ripu üle laua.

Kirjuta üles: käe suurim kõrgus; kaamera kõrgus ja koht; mitu tükki ja kuidas need kokku käivad; kui palju pilt väriseb, kui robot täiskiirusel liigub (pikslites või millimeetrites laua peal); kas pilt on pärast maha-tagasi sama; üks kaamera pilt, kus kogu ruudustik ja robot on näha.

**KAARDISTA ISE — vastused.** Iga osa kohta: numbrid, ühikud, kus fail on. Tegemata asja kohta üks rida, miks.

### Ohutus

* **Roboti alus peab jääma vabaks.** Süvendisse ja kallaku peale ei käi midagi, aluse külge ei kinnitata midagi ja robotit ei hoita kinni. Kui robot millegi vastu läheb, peab ta saama kallakust üles ja välja libiseda. Hoidik, mis ulatub roboti aluse vastu, võtab selle võimaluse ära.
* Hoidik, mis ruudus loksub, liigub, ja robot leiab ta üles. Kontrolli enne iga jooksu, et kõik hoidikud istuvad põhjas.
* Hoidikuid tõstetakse ja laetakse siis, kui robot on keelatud.
* Robot: käed ei ole laua kohal, kui robot on sisse lülitatud. Esimene jooks aeglaselt, hädastopp käeulatuses.
* Uue hoidiku esimene tõstmine käib 20 % kiirusel ja iminapp jääb 20 mm kõrgemale, õhku.
* Printeri otsik on 200–230 °C. Detailid spaatliga, kui laud on jahtunud.
* Kaamerapost on kõrge ja käib roboti ulatusse, kui ta on vales kohas. Enne esimest jooksu sõida käsi aeglaselt postile kõige lähemale ja vaata, et vahe jääb.
* Kaamera juhe on käe küljes kinni ja tal on tõmbetõke. Lahtine juhe jääb hoidiku taha ja robot tõmbab pistiku moodulist välja.
* Roboti käe otsas olevasse pistikusse ei ühendata midagi enne, kui pinge on mõõdetud ja õppejõud on üle vaadanud.
* Küljelõikurid lõikavad näost eemale.

### Komponendid selle labori jaoks

Tellimus läheb välja 16.10.26 ja jõuab kohale enne kaitsmist. Valmis nimekirja ei ole: meeskond paneb tellimuse ise kokku faili `docs/bom.md`, iga rea juures üks lause, milline osa seda küsib.

Tellimine käib ühisest tellimistabelist: [https://moodle.ut.ee/mod/url/view.php?id=1535601](https://moodle.ut.ee/mod/url/view.php?id=1535601). Kanna oma read sinna enne tellimise kuupäeva; mida tabelis ei ole, seda ei tellita. Fail `docs/bom.md` jääb sinu reposse põhjenduseks, miks sa just neid asju küsisid.

Mõtle näiteks: kas PLA-d jätkub kõigi hoidikute ja paari ümbertegemise jaoks; kas töökohale on Atomi mannekeen prinditud; kas akumooduleid on käes piisavalt, et pesa päris asja peal proovida; kas 6 × 2 mm magnetid hoidiku jala sees on midagi, mida su test küsib; mida su valitud kaamera toide küsib — pikem ja pehmem USB-C juhe, väike aku või pingemuundur; kas veebikaamera USB juhe ulatub posti otsast jaamani; ja kas klaase on piisavalt, sest vähemalt üks läheb selle labori jooksul katki.

### Hindamiskriteeriumid

| Kategooria | Punktid |
| :--- | :--- |
| Tööfailid — parameetritega hoidikud Gridfinity jalaga ja kahe kaamera kinnitused, STL ja 3MF iga prindi kohta | 5 p |
| Analüüs — protsess ja paigutus, detailide mõõdud, kasutatud lõtk ja kust see tuli, kalibreerimise nihe, testi tabel, kaamera toite valik | 5 p |
| Prototüüp — neli klaasi liiguvad sisendist töökohale ja töökohalt väljundisse, hoidikud tulevad samasse kohta tagasi, praagil on koht, kaamera istub tööriistahoidikul ja saab toite, veebikaamera näeb kogu lauda | 5 p |
| Dokumentatsioon — README, arenduspäevik, `layout.md`, `refit_test.csv`, `bom.md`, AGENTS.md | 5 p |
| **Kokku** | **20 p** |

### Kaitsmine

Link git repole, tag `3d-print-lab2`.

Kaitsmine on lihtne suuline 15 minuti jutuajamine. Võtad hoidikud ruudustikust välja ja paned tagasi, ja robot viib neli klaasi sisendist töökohale ja töökohalt väljundisse, ilma et sa punkte uuesti õpetaksid. Tööriista kaamera on toite all ja veebikaamera näeb kogu lauda. Avad oma arenduspäeviku. Õppejõud küsib umbes viis küsimust selle kohta, kuidas sa selle tegid. Kui esimesel korral ei õnnestu, tuled uuesti.

Repos on kaustas `3d-print/lab2/`: lähtefailid, STL ja `.3mf` iga prindi kohta, `docs/` kaustas `layout.md`, `refit_test.csv`, `bom.md` ja fotod, `README.md` selle labori kohta, ja `AGENTS.md` uuendatud.

### Arenduspäevik

**KAARDISTA ISE — päevik.** Üks sissekanne iga töösessiooni kohta, kirjutatud iseendale, nii et inimene, kes seal ei olnud, saab aru. Sissekandeid lisatakse, mitte ei muudeta.

**PP.KK.AA — kes olid kohal**
* Tegime:
* Juhtus (numbrid):
* Otsustasime, ja miks:
* Lahti järgmiseks korraks:

### Väljundid ja tulemused

**Väljundid**
* Andmehõive L2: klaas ja Atom kindlas kohas, et rõhukõverat saaks päris tõstmise pealt mõõta.
* Nutikad Lahendused L2: kaks kaamerat oma kohal — veebikaamera, mis näeb kogu lauda, ja tööriista kaamera, mis näeb otsikut ja on toite all — ja hoidikud, mille asukoht on teada ruudu nimena.
* 3D printimine L3: hoidiku standard (Gridfinity jalg ja lõtk), mille peale järgmised moodulid käivad, ja korduvtäpsuse number.

**KAARDISTA ISE, lõpus.**
* Git repo ja tag:
* Numbrid, mille see labor andis, ühikutega:
* Mida me teeksime teisiti:
* Mida järgmine labor peaks enne alustamist teadma:

### Tagasiside