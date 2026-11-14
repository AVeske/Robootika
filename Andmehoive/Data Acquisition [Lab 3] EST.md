## Andmehõive: Labor 3 — Tilk ja IRQ

**Maht:** 30 tundi | **Hindamine:** 20 punkti | **Meeskonnatöö:** 3-liikmelised meeskonnad | **Välja antud:** 28.10.26 | **Tellimise kuupäev:** 06.11.26 | **Esimene kaitsmine:** 19.11.26, veebis

### Mida teete

Seni tegi pump ühte tööd: imes, ja napp hoidis klaasi. Nüüd puhub sama pump ka süstlasse, ja otsikust tuleb tilk liimi. Liim on 3D-printeri vaik, mis kõveneb UV-valguse käes: tilk läheb Atomi ekraani peale, klaas tilga peale, ja UV LED kõvendab liimi läbi klaasi. Millal tilk algab ja lõpeb, otsustab solenoidklapp süstla ees, ja klappi juhib sinu Atom.

Sellest tuleb kaks küsimust. Kui suur on tilk? Liiga väike ei hoia klaasi, liiga suur pressitakse servast välja; tulemus on retsept: otsik, rõhk, impulsi pikkus, kõvendamise aeg. Mis siis, kui midagi läheb valesti? Otsik kõveneb kinni või süstal saab tühjaks, ja siis peab klapp kohe tagasi minema. Seda ei otsusta programmi põhitsükkel, vaid katkestus (IRQ): riistvara ütleb protsessorile, et nüüd.

Laboris 2 lubatud rõhu muutumise kiirus (dP/dt) tuleb siin: just see eristab kinnist otsikut lahtisest ja poolikut haaret korralikust.

Neli osa:

1. **Klapp ja impulss** — klappi lülitab M5Stack Mini 3A Relay Unit, mähise peal on kaitsediood, ja vooluta laseb klapp süstla õhku. Impulsi pikkuse loeb riistvarataimer, ja ostsilloskoop kahe kanaliga näitab, kui pikk impulss viigul ja klapi mähisel päriselt oli. Sama osa mõõdab relee piirid: viivitus, põrge, kontakti eluiga. Tulemus: impulsi tabel käsu ja mõõdetu kõrval, ja anduri koht voolikus koos põhjusega.
2. **Tilga suurus** — vähemalt viis impulsi pikkust, kümme tilka igaühega, heledale tilgaplaadile, mille peale läheb klaas vahetükkide peale. Pildistab tööriista kaamera, ja programm loeb laigud pikslitest kokku. Iga tilga rõhukõver salvestatakse samuti. Siis Atomi ekraanipoole mudel, tilk ja klaas tema peal, ja laigu suurus ning koht ekraani keskpunktist. Tulemus: `drops.csv`, `placement.csv`, graafik tilga suurusest impulsi vastu hajuvusega, ja retsept.
3. **Filter ja tuletis** — salvestatud kõverate peal: toores muutumise kiirus on müra, ja spekter näitab, miks. Vähemalt kaks filtrit, igaühe kohta müra ja viivitus. Siis sama Labori 2 pooliku haarde logil, ja kolm doseerimise kõverat kõrvuti: tavaline tilk, kinnine otsik, tühi süstal. Tulemus: valitud filter numbritega ja tunnus, mille järgi katkestus lülitub.
4. **Katkestus** — komparaator Falstadis hüstereesiga, siis plaadil LM358N teise poolena. Tema väljund läheb Atomi viiku, katkestus paneb klapi kinni ja lipu püsti, ja ülejäänu teeb põhitsükkel. Ostsilloskoop mõõdab reageerimise aja katkestusega ja ilma. Tulemus: kinnine otsik ja tühi süstal annavad alarmi, tavaline tilk ei anna, ja alarm jääb lukku, kuni ta maha võetakse.

### Kuidas töö käib

Repo ja töökord on Laborist 1 olemas ja samad. Tervet töölehte üle kopeerida ei ole vaja — too oma repo juurde see, mida vaja, ja täida `README.md` oma numbrite ja otsustega. Midagi ei kustutata: vale number jääb, parandus tuleb tema alla. Ei tulnud esimesel korral välja, tule homme tagasi ja proovi uuesti.

Esimesel päeval uusi osi ei ole — ehita sellest, mis riiulil on. Süstlad täidab õppejõud. Vaigu ja UV LED-i juures on kõigil kindad ja kaitseprillid, ja valgustamine käib katte all.

### Komponendid selle labori jaoks

Tellimus läheb välja 06.11.26 ja jõuab kohale enne kaitsmist. Valmis nimekirja ei ole: meeskond paneb tellimuse ise kokku faili `docs/bom.md`, iga rea juures üks lause, milline osa või number seda küsib. UV LED-i ja draiveri valib meeskond ise, ja õppejõud ostab need Mouserist.

### Kaitsmiseks on vaja

Ainult git repositooriumi link, tag `data-acquisition-lab3`. Kaustas `data-acquisition/lab3/` peab olema:

* `src/` püsivara ja logijaga, `data/` kaustas `drops.csv`, `placement.csv`, kõverad ja tilgaplaatide pildid, `notebooks/` tilkade, muutumise kiiruse ja spektritega
* `docs/`: skeemi foto, ostsilloskoobi pildid, Falstadi eksport, `recipe.md`, `latency.csv`, uuendatud `pump_control.md`, `bom.md`
* Täidetud `README.md` koos arenduspäevikuga
* `AGENTS.md` uuendatud

Kaitsmine on lihtne suuline 15 minuti jutuajamine. Teed ühe tilga retsepti järgi ja näitad selle rõhukõverat. Paned peale kinnise otsiku ja näitad ostsilloskoobil, kuidas klapp lahti lastakse ja kui kiiresti. Näitad, et teine tilk ei tule enne, kui alarm on maha võetud. Avad oma arenduspäeviku. Umbes viis küsimust selle kohta, kuidas sa selle tegid. Kaitsta saab nii mitu korda, kui vaja.
