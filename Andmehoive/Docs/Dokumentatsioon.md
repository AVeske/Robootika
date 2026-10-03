# Andmehõive labori dokumentatsioon

See dokument võtab kokku Andmehõive labori tööruumis oleva sisu: riistvara, failid, andmevoo ja prototüüpide hetkeseisu. See kirjeldab nähtavaid faile ja koodi; riistvara tegelikku ühendust ega kõigi funktsioonide töötamist pole siin kontrollitud.

## Labori eesmärk ja süsteemi töö

Labori eesmärk on mõõta pumbakasti torustiku rõhku, kuvada või logida mõõtetulemus ning juhtida MG400 pumbakasti nii, et pump käivituks ja seiskuks rõhu järgi. Sama AtomS3 peaks valima ka tähe ja saatma selle jaama, kust robot saab selle joonistada.

```text
MPX5700AP rõhuandur
  -> AtomS3 ADC
  -> USB-serial arvutisse
  -> Python arvutab rõhu ja kirjutab CSV-faili
  -> Python saadab pumba käsu HTTP API-le
  -> MG400 DO väljund juhib pumbakasti
```

Toru T-liitmik jagab rõhuühenduse anduri ja iminapa vahel. Nii saab mõõta rõhku samal ajal, kui iminapp objekti haarab.

## Riistvara ja selle ülesanded

- **MPX5700AP rõhuandur** mõõdab absoluutrõhku ja väljastab rõhuga seotud analoogpinge. Python kasutab teisendust `P = (Vout / Vsupply - 0.04) / 0.0012858`, kus rõhk on kPa-des ja absoluutne.
- **AtomS3** on ESP32-S3-l põhinev mikrokontroller. Selle ADC loeb anduri väljundpinget; USB kaudu saab mõõteandmed arvutisse saata. Teises töövoos valib Atom ka tähe ja saadab selle üle WiFi.
- **Maketeerimisplaat ja juhtmed** ühendavad anduri, toite ja AtomS3 ADC sisendi ilma jootmiseta.
- **Takistid, kondensaatorid, potentsiomeetrid ja dioodid** on katseteks ning hilisemate signaalitöötluslahenduste jaoks.
- **Multimeeter** kontrollib toitepinget ja anduri väljundit enne ADC-ga ühendamist.
- **Ostsilloskoop** näitab signaali ajas ning aitab uurida müra ja sageduskomponente.
- **4 mm voolik, T-liitmik ja vooliku kork** moodustavad rõhu mõõtmise ja katsetamise torustiku.
- **Iminapp ja polükarbonaatklaas** võimaldavad kontrollida, kas pump tekitab piisava vaakumi ning kas haarats suudab klaasi hoida.
- **MG400 ja pumbakast** annavad pumbale juhtsignaali roboti digitaalväljundi ehk DO kaudu.
- **Arvuti** käitab Python-programmi, loeb Atomi seriali, salvestab CSV-d ja saadab pumba juhtkäske.

## Dokumentatsioonifailid

- [Labori tööleht](../README.md) sisaldab eesmärke, vahendeid, ülesandeid, ohutusjuhiseid, hindamist ja nõutud väljundeid. See on juhend, mitte veel täidetud tulemuste aruanne ega täielik arenduspäevik.
- [Kaardistamine.md](Kaardistamine.md) on esmane koosoleku- ja komponentide kaardistus. Seal on kirjas esialgne seadistus, COM6 kasutamine, Thonny ja API katsetamise märkmed.
- Tööruumi vaadeldud seisus pole loodud `sensor_choice.md`, `bom.md` ega `pump_control.md` faile, kuigi labori tööleht nõuab neid.

## `scripts_ai` failid

- [atom_sensor.py](../scripts_ai/atom_sensor.py) käib AtomS3 peal. See loeb GPIO 25 ADC-d, keskmistab 32 ADC näitu ja väljastab iga 10 ms järel rea kujul `aeg_ms,mikrovoltid`. See ei arvuta rõhku ega kuva seda ekraanil.
- [live_logger.py](../scripts_ai/live_logger.py) käib arvutis. See saadab `atom_sensor.py` sisu Atomile, loeb seriali, teisendab mikrovoltide väärtuse rõhuks, logib mõõtmised ning juhib kompressorit `compressor_client.py` kaudu. Tavalisel lõpetamisel proovib see pumba välja lülitada.
- [compressor_client.py](../scripts_ai/compressor_client.py) saadab HTTP POST päringu aadressile `http://127.0.0.1:8000/api/pump`. Päringu JSON sisaldab näiteks `{"mode":"suck"}` või `{"mode":"off"}`. See on klient; pumba API teenus peab eraldi töötama samas arvutis.
- [pump_control.py](../scripts_ai/pump_control.py) on teine, eraldi juhtimisprototüüp. See mõõdab rõhku arvutis, arvutab atmosfäärirõhu käivitumisel ning kasutab hüstereesi: üle 90 kPa absoluutrõhu korral pump sisse, alla 75 kPa korral välja. Suhtelise rõhu piirid `-70…+110 kPa` toimivad täiendava ohutuspiirina.
- [log.csv](../scripts_ai/log.csv) sisaldab hetkel ainult veerupäist `time_ms,microvolts,pressure_kpa,relative_kpa,compressor`; mõõteridu seal pole.

### `scripts_ai` variantide erinevus

`live_logger.py` kasutab olemasolevat `atom_sensor.py` faili, mille väljund on `aeg,mikrovoltid`. `pump_control.py` aga eeldab, et Atomil on `pressure.py`, mis võtab perioodi argumendina ja väljastab teistsuguseid välju. Sellist `pressure.py` faili Andmehõive kaustas pole. Need kaks prototüüpi ei kasuta seega praegu sama Atomi programmi ega sama andmeprotokolli.

## `scripts_by_hands` failid

- [controller.py](../scripts_by_hands/controller.py) käib Atomil. See loeb GPIO 25 ADC-d, väljastab pinge voltides (`"1.234 V"`) ja ootab iga näidu vahel 100 ms.
- [pump_controller.py](../scripts_by_hands/pump_controller.py) käib arvutis. See avab COM6, saadab `controller.py` Atomile, loeb pingeread, arvutab absoluutrõhu, kirjutab mõõte `live_logger.py` abil ja juhib pumpa. Lävendid on 98 kPa sisse ja 70 kPa välja; nende vahel hoitakse senist režiimi.
- [live_logger.py](../scripts_by_hands/live_logger.py) avab käivitamisel `log.csv` faili kirjutamiseks, lisab päise ja pakub `write_log()` funktsiooni. Iga rida kirjutatakse kohe kettale.
- [compressor_client.py](../scripts_by_hands/compressor_client.py) saadab pumba režiimi samale kohalikule HTTP API aadressile nagu `scripts_ai` klient.
- [orchestrator.py](../scripts_by_hands/orchestrator.py) käivitab eraldi protsessidena `mpremote`-i kaudu Atomi kontrolleri ja arvuti pumbakontrolleri.
- [log.csv](../scripts_by_hands/log.csv) sisaldab näidismõõtmisi. Veerud on `time_ms,volts,pressure_kpa,compressor`. Ajatempel on arvuti Unix-aeg millisekundites, rõhk on absoluutne kPa ja pumba veerg näitab logitud režiimi.

### `scripts_by_hands` variandi erinevus

Siin on kaks võimalikku viisi Atomile koodi käivitamiseks: `pump_controller.py` saadab koodi seriali kaudu, `orchestrator.py` käivitab `mpremote`-i. Neid ei tasu korraga kasutada, sest mõlemad võivad COM6 porti avada ning Atomi seriali juhtida. `pump_controller.py` kasutab lisaks kolmanda osapoole `keyboard` paketti Escape-klahvi lugemiseks.

## Andmete liikumine ja rõhu loogika

1. Atom käivitab ADC mõõtmise ja väljastab näidu USB-seriali kaudu.
2. Arvuti loeb seriali, teisendab pinge või mikrovoltid MPX5700AP valemiga absoluutrõhuks.
3. Juhtprogramm otsustab rõhu põhjal, kas pump peab töötama või seisma.
4. Pumba režiim saadetakse kohaliku HTTP API kaudu MG400 pumbakasti juhtimisele.
5. Mõõtmised ja valitud pumba režiim lisatakse CSV faili.

Koodis olevad lävendid on esialgsed väärtused, mitte veel tehase targa kasti mõõtmiste põhjal kinnitatud sihtmärgid. Absoluutrõhku ja atmosfääri suhtes arvutatud rõhku ei tohi omavahel segamini ajada.

## Praeguse koodi piirangud ja ohutus

- GPIO 25 kasutamine vajab AtomS3 konkreetse plaadi ja MicroPythoni püsivaraga kontrollimist. Enne sensoriga ühendamist tuleb kinnitada, et see on õige ADC-viik.
- MPX5700AP võib väljastada pinget, mis ületab ESP32 ADC lubatud sisendit. Andmelehe alusel tuleb kontrollida pinge kogu kasutatavas rõhuvahemikus; 5 V andurit ei tohi ühendada ADC külge, kui väljund võib ületada viigu piiri.
- Koodides eeldatakse anduri toitepingeks täpselt 5,0 V. Tegelik toitepinge mõjutab arvutatud rõhku, seega tuleb see mõõta ja arvutuses arvesse võtta.
- Pumbakliendid eeldavad, et arvutis töötab aadressil `127.0.0.1:8000` API, mis võtab vastu `suck` ja `off` käske.
- Pumba väljalülitus toimub tavapärasel lõpetamisel või Escape/Ctrl-C käsitlemisel. Kui protsess või arvuti katkeb ootamatult, ei taga praegune tarkvara ise, et pump lülitub välja.
- `scripts_ai/live_logger.py` lülitab pumba välja, kui absoluutrõhk langeb alla 75 kPa, ning muul juhul lülitab selle sisse, kui rõhk jääb etteantud ohutusvahemikku. See ei ole sama hüstereesiloogika, mida kasutab `scripts_ai/pump_control.py`.
- Praegused failid näitavad rõhu mõõtmise ja pumba juhtimise prototüüpe. Need ei tõenda veel 100 Hz logimise täpsust, tehase targa kasti mõõtmist, puhumisrežiimi, Atomi ekraanikuva ega USB kadumise korral ohutut seiskamist.
- Labori nõutud andmeanalüüsiks on vaja eraldi salvestada toormõõtmised, arvutada ADC sammu rõhueraldusvõime, uurida müra ja koostada spektrid.

## Soovitatav ühe prototüübi töövoog

1. Käivita MG400/pumba HTTP API teenus.
2. Ühenda andur ning kontrolli multimeetriga toitepinget ja anduri väljundit.
3. Ühenda AtomS3 arvutiga ja vali õige seriali port.
4. Käivita valitud töövoog. Ära kasuta samal ajal `mpremote`-i ja teist COM-porti avavat skripti.
5. Kontrolli, et seriali näidud on usutavad ja CSV-faili lisanduvad read.
6. Katseta pumba sisse- ja väljalülitumist, jälgides rõhku. Hoia hädaseiskamise võimalus käepärast.
7. Peata programm tavapäraselt ja kontrolli, et API kinnitas pumba väljalülitamise.

## Labori järgmised vajalikud tulemused

- Kinnitatud AtomS3 ADC viik ja ohutu sensoriväljundi ühendus.
- 10-sekundiline 100 Hz logi koos kontrolliga, et ridade arv ja multimeetri näit on nõutud piires.
- Mõõdetud müratase pump väljas ja pump sees ning nimedega spektritipud.
- Tehase targa kasti viieminutiline logi ja sellest arvutatud lülituspunktid, töö-/seisuajad ning käivitused minutis.
- Oma kasti juhtimisriba, minimaalne seisuaeg ja käivituste piir, mis põhinevad päris mõõtmistel.
- Katse, mis tõendab pumba väljalülitumist andmeside või USB katkemisel.
- `sensor_choice.md`, `bom.md` ja `pump_control.md` koos mõõtmiste, ühikute ja põhjendustega.
- Tähe saatmise ning jaamas vastuvõtmise ja robotiga joonistamise otsast lõpuni kontroll.

See dokument on koostatud tööruumis nähtavate Andmehõive failide põhjal. Riistvara ja API tegelik käitumine tuleb eraldi katsetega kinnitada.