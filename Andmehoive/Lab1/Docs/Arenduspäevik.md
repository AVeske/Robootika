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

Simulatsioon müraga: [Falstadi skeem](https://www.falstad.com/circuit/circuitjs.html?ctz=DwYwlgTgBAZgvAIgAwKgFwM6KQOiUgRlTBEQNwCZ8KB2GgZiQA4KA2ATnZtRACNEArCigAHfgiGoAbhEGoAtpkEBTALQEiAPgBQUKMClQAHmVZIojACxQCZmzVap4yVAHdnRWLISf5AQyMpRAocS1ReMD8sBBDHKEhsPEIEAHodPWAAc2NTcysbO3p6OOcUNN19VxyfOwIHG3YKexLsVPT9P2r823NLfALhZyYFP0R6HHoFMFaoTNGffEW2iuAqkwRuy2tuggonVvKMtbGkaw0mvvNz-ZdDyurLm12oR56bsvbVh-6el-ZWAbvZYZADyD3+AygAi2gNgZFQGFIt0+Rm+UAoMI0AIx3DhLigGGmPj26GUiAAggA7AAmAFdoEgADQUQDIBAIoAA1YH6VHrCgQihUF62dEUSZ44SEsgktBkhDkgAiAGEoPJabSafSoEgWfRGfROdzgLzEJYIQQIdCmhb2ECCUTdqhZRTlVApGAwABrI3HHyNZoWU7NIF3YAAJWqFut9SjTxJHji7kQJW8ZhGgTk8W8uHwRFDAHsoMpKYhhgSRKYbkYSRWXO0MiI3TNEXI7g2izMgviWxIjSl8zpgClwBAdEA)

1. Lisati kaardistuse märkmed Git-reposse.
2. Lisati esimesed AtomS3 ja arvuti vahelised rõhu mõõtmise ning pumba juhtimise skriptid.
   - Atom loeb anduri ADC väärtust ja saadab selle USB-seriali kaudu arvutisse.
   - Python teisendab näidu rõhuks, logib selle CSV-faili ning saadab pumba režiimi MG400 API-le.
   - Lisati kaks katsetusvarianti: käsitsi kirjutatud skriptid ja eraldi `scripts_ai` variant.
3. Täiendati käsitsi variandi logimist.
   - CSV-sse lisati ajatempel, pinge, arvutatud rõhk ja pumba režiim.
   - Pumbakontrollerisse lisati Escape-klahviga seiskamine.

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
