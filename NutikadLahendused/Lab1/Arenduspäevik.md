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








## 24.10.2026

- Failid paigutati laborijuhendi kaustajaotuse järgi; README-sse lisati otselingid.
- Dokumentatsioon on `docs/` all. Programmi- ja veebikoodi sisu ei muudetud.
- Kõrvalrepo püsivara põhjal täiendati `docs/atom_page.md`: lehe osad, nupud, API teed, salvestamine ja katsejuhis.

- **ÜldResult (`cd4b5b8`, `88e4d1b`).** Lisati `AtomS3_Pildi_edastamine_ja_kuvamine_1.MOV`, `AtomS3_Pildi_edastamine_ja_kuvamine_2.MOV` ja `MG400_Tahtede_joonistamine.MOV` kausta `ÜldResult/Lab1&2/`. Täiendati [ühiskatse kirjeldust](../../ÜldResult/Lab1&2/Kirjeldus.md): seal on kirjas Atomi pildikuva, veebist saadetud tähtede joonistamine ning otse seadmest saadetud H. Samas kirjeldatakse vetruva pastakahoidiku käitumist.
- **Failide leitavus (`88e4d1b`).** `atom_page.md` ja `letter_writer.md` viidi `docs/` alla ning lisati labori ja aine README-de lingid. `src/`, `firmware/` ja `data/` README-d selgitavad väliste projektide ning asendifaili asukohta.
- **Atomi lehe kirjeldus (`88e4d1b`).** Dokument koondab pildipesad, eelvaate, pildi saatmise, nupužestid ja `TEST DISPLAY` testi ning kirjeldab nende kontrollimist.

