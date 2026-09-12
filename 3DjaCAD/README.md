## 3D printimine ja CAD: Labor 1 — Printer, ja tööriist, mis annab järele

**Töömaht:** 30 tundi | **Hindamine:** 20 punkti | **Meeskond:** 3 tudengit | **Välja antud:** 11.09.26 | **Tellimise kuupäev:** 22.09.26 | **Esimene kaitsmine:** 06.10.26, veebis

### Kuidas see dokument töötab

* Kopeeri see fail esimesel päeval oma repo laborikausta `README.md`-ks ja täida seal, töö käigus.
* **ANTUD** on see, mida õppejõud teab. **KAARDISTA ISE** on tühi, sest vastust ei tea veel keegi. Sina mõõdad ja kirjutad numbri koos põhjusega siia.
* Midagi ei kustutata. Vale number jääb, kuupäevaga, parandus tuleb tema alla.
* Kirjuta nii, et meeskonnakaaslane, kes sel päeval ruumis ei olnud, saab aru: päris failinimed, päris numbrid, ühikud.
* Tähtaeg ei ole tähtis. Tähtis on, et asi saab tehtud ja sa saad aru. Ei tulnud esimesel korral välja, tule homme tagasi ja proovi uuesti. Kaitsta saab nii mitu korda, kui vaja.

### Eesmärk

Aasta lõpuks paneb MG400 kokku sildi: AtomS3, mille ekraani peale on liimitud polükarbonaatklaas. Iga detail, mis roboti külge kinnitub või elektroonikat hoiab, tuleb selles ruumis printerist välja. See labor räägib sellest printerist ja lõpeb esimese tööriistaga roboti küljes: pastakahoidikuga. Sama meeskond teeb kõiki kolme ainet: sina kirjutad programmi ja sina teed pastaka otsiku. Kolm ainet, üks demo: **vajuta tähte, robot joonistab selle.**

Selles laboris on kolm asja:

1. **Kuup.** 5 × 5 × 5 cm, sees silinder raadiusega 2 cm. Ütleb, kui suur lõtk sellel printeril päriselt on.
2. **Paindlik tükk.** Ütleb, kust ta murdub ja kuhu maani ta plastiliselt paindub.
3. **Pastakahoidik.** Roboti otsa läheb kuulpastakas, seega on ta Z vigade suhtes väga tundlik. Hoidik peab järele andma.

Esimesel päeval uusi osi ei ole. Ehita sellest, mis riiulil on, ja kirjuta puuduv tellimuseks, mis läheb välja 22.09.

*See on elav dokument. Uuenda eesmärke, kui need töö käigus muutuvad — uued teadmised teevad vanad eesmärgid vahel mõttetuks. Mõte on hoida meeskond kogu aeg sihil, et ei eksitaks detailide metsa ja põhiprobleem ei jääks lahendamata.*

**KAARDISTA ISE — eesmärk nii, nagu ta tegelikult välja tuli.**

### Kontrollnimekiri

**Peab olema tehtud**

- [ ] Kuup prinditud, lõtk teada.
- [ ] Paindlik tükk prinditud, murdumise koht ja plastilise paindumise piir teada.
- [ ] Pastakahoidik roboti küljes, annab järele. Robot joonistab sellega tähe, mida ESP32 näitab.
- [ ] Repo ja arenduspäevik täidetud, tag `3d-print-lab1`.

**KAARDISTA ISE — kuupäevad ja sinu enda sammud.**

### Sisendid

* Riiulilt: printerid, PLA, nihik, kuulpastakad, marker, maalriteip, paber.
* Vanade asjade kastist, kui see on: eelmise aasta hoidikud, et elu lihtsam oleks. Kui ei ole, ei ole midagi puudu.
* Õppejõult: MG400 baaspakett Pythonis.

### Vahendid

1. Fusion 360, hariduslitsents (aktiveeritakse tunnis)
2. Hoidiku jaoks tarkvara sinu valikul: Fusion, Blender või muu, mis annab STL-i
3. PrusaSlicer, labori printerid, PLA
4. Nihik, kuulpastakas, marker, maalriteip, paber
5. MG400 koos baaspaketiga
6. Git, üks repo meeskonna kohta, `AGENTS.md` juurkaustas

*Kui plaan muutub, uuenda ka vahendeid, või tee draw.io skeem, mis näitab, kuidas asjad omavahel töötavad.*

**KAARDISTA ISE — mida sa päriselt kasutasid.**

### Taustainfo

* **Fusion 360 mudeldamine FDM printimise jaoks**
  [https://www.youtube.com/watch?v=5hComh1hFzY](https://www.youtube.com/watch?v=5hComh1hFzY)
  Või print in place
  [https://www.youtube.com/watch?v=vHHMwpaIrco](https://www.youtube.com/watch?v=vHHMwpaIrco)
* **3D mudelite harjutused**
  Too Tall Toby
  [https://www.tootalltoby.com/](https://www.tootalltoby.com/)
* **3D prinditavad vedrud**
  [https://www.youtube.com/watch?v=wpriGP45Unw](https://www.youtube.com/watch?v=wpriGP45Unw)
  Või print-in-place hinged
  [https://www.youtube.com/watch?v=fYDJLdOV_zE](https://www.youtube.com/watch?v=fYDJLdOV_zE)
* **Prusa**
  Printer: [https://www.prusa3d.com/product/prusa-core-one/](https://www.prusa3d.com/product/prusa-core-one/)
  Slicer: [https://www.prusa3d.com/page/prusaslicer_424/](https://www.prusa3d.com/page/prusaslicer_424/)
* **MG400 mount**
  Fusion360: [https://a360.co/4nruicX](https://a360.co/4nruicX)

*Lisa siia oma allikaid ja kasulikku infot, mis aitaks sul projektist aru saada ka aastaid hiljem, kui selle uuesti lahti teed.*

**KAARDISTA ISE — sinu allikad.**

### Osad

#### 1. Kuup

Fusionis. 5 × 5 × 5 cm, sees silinder raadiusega 2 cm. Lõtk silindri ja seina vahel on parameeter. Kui print võtab liiga kaua aega, tee kuup madalamaks.

Kirjuta üles: mis lõtkuga silinder pöörleb ja mis lõtkuga on kinni sulanud. See number on iga hilisema detaili jaoks.

#### 2. Paindlik tükk

Sinu disain, sinu tarkvara. Prindi ja painuta.

Kirjuta üles: kuhu maani ta paindub ja tuleb tagasi, kust alates jääb plastiliselt kõveraks, kus murdub. Need numbrid lähevad hoidiku vedrutavasse ossa.

#### 3. Pastakahoidik

Tarkvaras, mille ise valid. Toru kuulpastaka jaoks ja kinnitus MG400 flantsi külge. Vedrutav osa nii, et kui õpetatud kõrgus on paar millimeetrit paigast ära, jääb pastakas terveks ja joon on ikka paberil.

Vedrutav osa võtab mõned proovimised. Iga print on uus versioon ja uus fail. Kirjuta iga versiooni juurde, mis muutus ja miks. Pane tähele, kui kaua muudatus tarkvaras võtab: see on koht, kus sa tunned, miks Fusionit kasutada.

Pane hoidik roboti külge. Robot joonistab tähe, mida ESP32 näitab.

**KAARDISTA ISE — vastused.** Iga osa kohta: numbrid, ühikud, kus fail on. Tegemata asja kohta üks rida, miks.

### Ohutus

* Printeri otsik on 200–230 °C. Detailid spaatliga, kui laud on jahtunud.
* Robot: käed ei ole laual, kui robot on sisse lülitatud. Esimene jooks aeglaselt, hädastopp käeulatuses.
* Küljelõikurid lõikavad näost eemale.

### Komponendid järgmiseks laboriks

Tellimuse paneb kokku meeskond ise, jagatud Google Sheetis. Tellimus läheb välja 22.09.26.

Mida võib vaja minna: PLA, PETG, M5 poldid ja mutrid (laua augud on 5 mm), M3 kuumsisestused, magnetid. Kirjuta sinna see, mida sul selle labori järgi päriselt puudu jäi.

### Hindamiskriteeriumid

| Kategooria | Punktid |
| :--- | :--- |
| Tööfailid — kuup, paindlik tükk, hoidiku versioonid, STL ja 3MF | 5 p |
| Analüüs — lõtk, paindumise ja murdumise numbrid | 5 p |
| Prototüüp — hoidik roboti küljes annab järele, robot joonistab tähe, mida ESP32 näitab | 5 p |
| Dokumentatsioon — README, arenduspäevik, AGENTS.md | 5 p |
| **Kokku** | **20 p** |

### Kaitsmine

Link git repole, tag `3d-print-lab1`.

Kaitsmine on lihtne suuline 15 minuti jutuajamine. Näitad, kuidas robot joonistab tähte, mida ESP32 näitab, ja avad oma arenduspäeviku. Õppejõud küsib umbes viis küsimust selle kohta, kuidas sa selle tegid. Kui esimesel korral ei õnnestu, tuled uuesti.

Repos on kaustas `3d-print/lab1/`: lähtefailid, STL ja `.3mf` iga prindi kohta, see fail kui `README.md`, ja `AGENTS.md` uuendatud.

### Arenduspäevik

**KAARDISTA ISE — päevik.** Üks sissekanne iga töösessiooni kohta, kirjutatud iseendale, nii et inimene, kes seal ei olnud, saab aru. Sissekandeid lisatakse, mitte ei muudeta.

**PP.KK.AA — kes olid kohal**
* Tegime:
* Juhtus (numbrid):
* Otsustasime, ja miks:
* Lahti järgmiseks korraks:

### Väljundid ja tulemused

**Väljundid**
* Nutikad Lahendused L1: pastakahoidik, mis demopäeval tähe joonistab.
* 3D printimine L2, L3, L4: lõtk ja paindumise numbrid iga hilisema detaili jaoks.

**KAARDISTA ISE, lõpus.**
* Git repo ja tag:
* Numbrid, mille see labor andis, ühikutega:
* Mida me teeksime teisiti:
* Mida järgmine labor peaks enne alustamist teadma:

### Tagasiside
