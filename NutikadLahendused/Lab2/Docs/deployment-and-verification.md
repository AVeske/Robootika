# Seitsme sammu kontroll

## 1. Server töötab ka pärast SSH sulgemist

`python app.py` töötab SSH-terminali protsessina ja võib ühenduse sulgemisel
peatuda. Püsivaks käivitamiseks kasuta `systemd` teenust `robot-postoffice`.
Teenust haldab Ubuntu, nii et SSH võib sulgeda. Teenus käivitub rebooti järel
ning protsessi väljumisel käivitatakse see 3 sekundi pärast uuesti.
`systemctl stop robot-postoffice` peatab teenuse siiski tahtlikult.

### Paigaldamine või olemasoleva teenuse uuendamine

Käivita järgmised käsud **dropletis**, mitte kohalikus Windowsi terminalis.
Too repo muudatused enne serverisse. Näites on repo `/root/Robootika` all;
muu asukoha puhul muuda teenusefailis WorkingDirectory ja ExecStart radu.

```bash
cd /root/Robootika/NutikadLahendused/Lab2/Server
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Võti peab olema kas `Server/.env` failis või `/etc/robot-postoffice.env` failis:

```text
ATOM_API_KEY=sinu-tegelik-võti
```

Olemasolev `Server/.env` sobib: rakendus loeb seda ise. Kui võti on mõlemas
failis, on teenuse `/etc/robot-postoffice.env` väärtus eelistatud. Ära loo
võtmele uut väärtust, kui Atom juba kasutab olemasolevat võtit.
Vajadusel loo teenuse seadistusfail olemasolevat faili tühjendamata:

```bash
sudo touch /etc/robot-postoffice.env
sudo chmod 600 /etc/robot-postoffice.env
sudo nano /etc/robot-postoffice.env
```

Kui samas SSH-terminalis töötab praegu Flask, peata see Ctrl+C abil.
Kui teenus teatab hõivatud pordist, kontrolli `sudo ss -ltnp 'sport = :5000'`
abil, milline protsess seda kasutab; peata konkreetne vana serveriprotsess.

```bash
sudo cp robot-postoffice.service /etc/systemd/system/robot-postoffice.service
sudo systemctl daemon-reload
sudo systemctl enable robot-postoffice
sudo systemctl restart robot-postoffice
sudo systemctl enable --now caddy
sudo systemctl status robot-postoffice --no-pager
curl --fail http://127.0.0.1:5000/api/status
curl --fail https://narva1.roboarena.org/api/status
```

Caddy olemasolev `reverse_proxy 127.0.0.1:5000` sobib teenusega.
Gunicorn kasutab ühte worker'it ja ühte thread'i, sest tööde olek on RAM-is.
Teenusel on praeguse root-paigalduse õigused. Eraldi teenusekasutajale
üleminekul vii projekt näiteks /opt alla ja määra teenuses User=.

### Kontroll pärast SSH sulgemist

1. Veendu, et mõlemad curl-kontrollid õnnestusid.
2. Sulge SSH `exit` käsuga.
3. Ava veebileht telefonis mobiilse andmesidega ja värskenda seda.
   Leht peab endiselt avanema. Kui Atom on väljas, on OFFLINE õige tulemus:
   see kirjeldab Atomi ühendust, mitte veebiserveri tööd.
4. Ühendu SSH-ga uuesti ja kontrolli:

```bash
systemctl is-enabled robot-postoffice
systemctl is-active robot-postoffice
systemctl is-enabled caddy
systemctl is-active caddy
```

Oodatavad vastused on enabled ja active. Rebooti katseks kasuta sobival
hetkel `sudo reboot`, oota serveri taastumist ning korda lehe ja teenuste kontrolli.
SSH seansi sulgemine teenust ei restardi. Serveri tegelikul restardil kaovad
RAM-is hoitud tööd ning last_seen; kettale salvestatud pildid säilivad.

Vea korral:

```bash
sudo journalctl -u robot-postoffice -n 80 --no-pager
sudo journalctl -u caddy -n 50 --no-pager
```

Koodi uuendamise järel: `sudo systemctl restart robot-postoffice`.
Teenusefaili muutmisel kopeeri see uuesti /etc/systemd/system alla ja tee
`daemon-reload`, seejärel restart. Teenus ei taga kättesaadavust dropleti,
DNS-i või võrgu rikke ajal, kuid ei sõltu avatud SSH-terminalist.

## 2–4. Kaks tööd

Veebilehe valikus on `letter` ja `show_image`.
Letter võtab ühe tähe A–Z. `show_image` kasutab veebilehel üles laaditud PNG pilti.
Vali PNG ja vajuta UPLOAD PNG, seejärel SEND JOB. Varem üles laaditud
pildid saab valida samast nimekirjast ka pärast serveri restarti.
Server kontrollib faili sisu: staatiline PNG kuni 1 MiB ja 2048 × 2048 pikslit.
Pilt skaleeritakse proportsionaalselt 128 × 128 mustale taustale.
Pildid säilivad `Server/instance/images` kaustas, mida Git ei jälgi.
Soovi korral määra `IMAGE_DIR` keskkonnamuutujaga teine kirjutatav kaust.
Paigalda uuendatud requirements.txt (lisatud Pillow) ja taaskäivita teenus.

`show_image` argumendiks on üleslaadimisel saadud pildi ID.
Poll-vastuses on lisaks `image_url`, näiteks `/api/images/<id>/png`.
Atom küsib selle tee samast HTTPS serverist, lisades `X-API-Key` päise,
laeb PNG alla ja kuvab ekraanil. Alles pärast edukat kuvamist saadab
`/api/result` kaudu `done`; allalaadimis- või kuvamisvea korral `error`.
Allalaadimise ajal kadunud ühenduse puhul peab Atom proovima uuesti.
Varem pakutud `smile`, `heart`, `checker` nimed enam ei kehti.
Selles repos Atomi/jaama lähtekoodi ei ole: allalaadimine ja kuvamine
vajavad Atomi püsivara muudatust ning seadmega katsetamist.

## 5. Unknown job → refused

Saada `/api/jobs` JSON `{"job":"unknown","arg":null}`.
Oodatav: HTTP 400, `status: refused`; olemasolev töö jääb alles.
Vigane argument saab samuti refused. Lubatud tööd pannakse FIFO järjekorda.

## 6. Vana töö aegub

Jäta Atom välja, saada töö ja oota vühemalt 30 sekundit.
Lehe järgmine staatusepäring näitab `expired` ka siis, kui Atom on väljas.
Seejärel Atomi poll peab tagastama `{"msg":null}`.
Aegumine puudutab ootel tööd; juba saadetud töö võib lõpuni töötada.

## 7. ONLINE/OFFLINE ja last_seen

Enne esimest autentitud polli: OFFLINE ja last_seen puudub.
õige X-API-Key päisega poll: ONLINE ja ajatempliga last_seen.
üle 10 sekundi ilma pollita: OFFLINE, eelmine last_seen jääb nühtavaks.
Leht käsib staatust iga 2 sekundi järel. Vale võtmega poll ei uuenda last_seen'i.
Serveri ühendusvea korral näitab leht SERVER ERROR.

## Kohalik API kontroll

Serveri kaustas: `python -m unittest discover -s tests -v`.
See kontrollib serveri protokolli, mitte Atomi ekraani ega roboti liikumist.

Nõuete koodikontroll, katkestuskatsed ja latentsuse mõõtmise juhend: [verification-and-latency.md](verification-and-latency.md).
