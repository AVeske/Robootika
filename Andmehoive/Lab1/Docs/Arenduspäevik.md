# Andmehõive

## 12.09.2026

**Kohal olid: Ats, Serafima, Ivan, Daniil**

1. Kaardistada, mis asju on vaja ja mis iga asi teeb.
   - Andur - Monolithic silicon absolute pressure sensor - MPX5700AP

   - AtomS3 - Miniature Programmable controller - Built around ESP32-S3

   - Maketeerimisplaat - Korduvkasutatav jootmisvaba alus alektroonikalülituste kiireks kokkupanemiseks ja testimiseks

   - Passiivkomplekt - Takistid, Kondensaatorid, Potentsiomeetrid, dioodid, valgusedioodid

   - Multimeeter - Mõõtmiseks and shit, et asju läbi ei põletaks

   - Ostsilloskoop - Elektrisignaalide reaalajas jälgimiseks, mõõtmiseks ja anaslüüsimiseks

   - 4 mm voolik - Mõeldud siis õhu/rõhu juhtimisele

   - T-liitmik - Õhu liikumiseks, kompressorist ühendub see andurisse ja selleni, mis päriselt tööd teeb

   - vooliku kork - peatada vool ühes voolikus
   - Iminapp - Täiturseade, mida kasutatakse objektide haaramiseks, tõstmiseks ja liigutamiseks vaakumi abil.

   - Polükarbonaatklaas - Klaas noh

2. Setup ühendus arvuti ja Roboti vahel:
   - Klooni Repo: https://github.com/KKallas/mg400-base
   - Setup Python environment (juhend README.md's)

3. Robot käitub kui ELETRILINE Energiaallikas !

4. How to Code this?
   - Ühenda DATA USB kaabliga arvuti külge.
   - Ava Thonny -> Run -> Configure Interpreter -> MicroController (ESP32) -> Vali õige MicroController (COM6 meie juhul).
   - Meil oli ka vaja updateida Microcontrollerit ennast, enne kui saime edukalt koodi seal jooksutada.
   - Mis on edasised sammud, kuidas saame Andurist infot ja mis selelga täpselt koodis vaja teha ?
     - Kuidas salvestada see Microcontrolleri peale, et päriselt ka töötaks pärast ja ühendada see olemasoleva ekosüsteemiga.
   - Vaja panna see kood samasse Giti, et saaks kutsuda API'd

5. Postman to Test API
   - API on olemas Gitis
   - Postman:
     - Text type to JSON; Muidu ei tööta


## 13.09.2026

**Kohal olid: Ats, Serafima, Ivan, Daniil**

1. Lisati kaardistuse märkmed Git-reposse.
2. Lisati esimesed AtomS3 ja arvuti vahelised rõhu mõõtmise ning pumba juhtimise skriptid.
   - Atom loeb anduri ADC väärtust ja saadab selle USB-seriali kaudu arvutisse.
   - Python teisendab näidu rõhuks, logib selle CSV-faili ning saadab pumba režiimi MG400 API-le.
   - Lisati kaks katsetusvarianti: käsitsi kirjutatud skriptid ja eraldi `scripts_ai` variant.
3. Täiendati käsitsi variandi logimist.
   - CSV-sse lisati ajatempel, pinge, arvutatud rõhk ja pumba režiim.
   - Pumbakontrollerisse lisati Escape-klahviga seiskamine.


Falstad skeem müraga:
[Link](https://www.falstad.com/circuit/circuitjs.html?ctz=DwYwlgTgBAZgvAIgAwKgFwM6KQOiUgRlTBEQNwCZ8KB2GgZiQA4KA2ATnZtRACNEArCigAHfgiGoAbhEGoAtpkEBTALQEiAPgBQUKMClQAHmVZIojACxQCZmzVap4yVAHdnRWLISf5AQyMpRAocS1ReMD8sBBDHKEhsPEIEAHodPWAAc2NTcysbO3p6OOcUNN19QxMfOwIHKApLczqS7DdnEu8zBQCg5DwBYm9cfCJyjNccmKb7VgskaxanNvH9Pyn823Mm5u7YRCYexHocegUwNqhMvzJ8O9T0-UnqzctrTYIKZZdV4GfjhY2T5QHZAr77H6PP5TUEaCgg-AFYSlB4VaHVWF2SzsOZbb5lKEAeRhOKRUAEbyR308GFIkLRRhh5kai1sDUs3AhwgwFx84LQykQAEEAHYAEwArtAkAAaCiAZAIBFAAGqojKM6p1awUAjaoQNOr41A8sj8wUIACyAB+IOsAI36+Sq34a4KkihUEFsj1nLnG3mfVAC4UAEQAwlB5BKxcoADZQJDy+gy+gqtX6V0IbG40kU+EEThGqAmvlB81C8NQKRgMAAa3TwAA9lBlCKDsaRKZvkZwZ2XI8MiIq5daXJVoOW5c+ty6YNfilGzpgClwBBNEA)
![Skeem](Skeem.JPG)

Skeem demonstreerib, et 0,2–5 V andurisignaal koos müraga ei mahu otse 0–3,3 V ADC sisendvahemikku ning üle 3,3 V olev signaal lõigatakse ära.

Skeemi kirjeldus:
- Andur 0,2–5 V. See on vahelduvpingeallikas, mis simuleerib päris anduri väljundit. Selle signaal muutub ajas vahemikus 0,2 V kuni 5 V.
- Müra ±50 mV. See on eraldi väike vahelduvpingeallikas, mis lisab andurisignaalile väikese juhusliku või kiiresti muutuva häire. Selle eesmärk on modelleerida päriselus tekkivat elektrilist müra. Näiteks kui andur annab parasjagu 2,00 V ja müra on +0,04 V, siis ADC mudelisse jõuab umbes 2,04 V. Kui müra on −0,03 V, jõuab sinna umbes 1,97 V. Müra amplituud on palju väiksem kui põhisignaalil, seega ta ei muuda kogu signaali olemust, vaid tekitab selle ümber väikese "värina".
- ADC mudel 0–3,3 V. ADC tähendab Analog-to-Digital Converter ehk analoog-digitaalmuundurit. Selle ülesanne päris mikrokontrolleris oleks analoogpinge digitaalseks väärtuseks teisendada. Antud skeemis kasutatakse op-võimendit pingejärgurina, et näidata ADC sisendi lubatud pingevahemikku. Op-võimendi väljund on piiratud vahemikku 0–3,3 V.
- Tagasiside op-võimendil. Op-võimendi väljund on ühendatud tagasi tema negatiivsele − sisendile. See tekitab negatiivse tagasiside ja muudab op-võimendi pingejärguriks.
- ADC viik. See on lihtsalt skeemi väljundpunkt, mis tähistab mikrokontrolleri ADC sisendviiku. Ehk see on pinge, mida ADC "näeks".
- Scope. Scope ehk ostsilloskoop kuvab ADC viigu pinge ajas. Selle pealt peaks olema näha kaks asja:
   - müra tõttu ei ole joon täiesti sile;
   - kui andurisignaal läheb üle 3,3 V, lõigatakse laine ülemine osa ära.



## 03.10.2026

1. Täiendati käsitsi variandi pumbakontrollerit.
   - Seriali pordiks muudeti COM5 (115200 baud).
   - Mõõteread kirjutatakse `log.csv` faili ja prinditakse samal kujul ka konsooli.
   - Escape-klahvi või Ctrl-C vajutamisel ning tavalisel juhtsilmusest väljumisel küsitakse API-lt pumba väljalülitamist.
2. Eemaldati vana `orchestrator.py`.
   - `pump_controller.py` saadab nüüd `controller.py` sisu ise AtomS3-le; eraldi `mpremote`-i protsessi ei käivitata.
   - Kasutada tuleb õiget seriali porti ning vältida sama pordi samaaegset avamist teise programmi poolt.

   Anduri, maketeerimisplaadi ja AtomS3 ühenduse foto:

![Rõhuandur ühendatuna maketeerimisplaadi kaudu AtomS3-ga](atom-andur-maketeerimisplaat.jpg)


