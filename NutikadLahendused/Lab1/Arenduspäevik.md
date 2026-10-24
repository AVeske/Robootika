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








## 24.10.2026 — failistruktuuri korrastamine

- Failid paigutati laborijuhendi kaustajaotuse järgi; README-sse lisati otselingid.
- Dokumentatsioon on `docs/` all. Programmi- ja veebikoodi sisu ei muudetud.


## 24.10.2026 — Atomi lehe seadete ja testide dokumentatsioon

- Kõrvalrepo püsivara põhjal täiendati `docs/atom_page.md`: lehe osad, nupud, API teed, salvestamine ja katsejuhis.
- `TEST DISPLAY` ning pildi- ja žestiseaded on koodis olemas.
- Selgitati, kuidas tähevaliku režiim mõjutab nupužestide kasutamist. Püsivara ei muudetud ega laaditud seadmesse.
