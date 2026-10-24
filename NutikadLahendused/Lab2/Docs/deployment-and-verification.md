# Seitsme sammu kontroll

## 1. Automaatkäivitus Ubuntu dropletis

Need käsud tuleb käivitada dropletis, kuhu uuendatud repo on toodud.
Teenuse rajad järgivad olemasolevat `/root/Robootika` paigaldust.
Kui repo asub mujal, muuda teenuse WorkingDirectory ja ExecStart radu.
Teenusel on senise root-paigalduse õigused; eraldi teenusekasutajale
üleminekul tuleb projekt viia näiteks /opt alla ja lisada User=.

```bash
cd /root/Robootika/NutikadLahendused/Lab2/Server
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
sudo install -m 600 /dev/null /etc/robot-postoffice.env
sudo nano /etc/robot-postoffice.env
```

Viimasesse faili kirjuta `ATOM_API_KEY=sinu-tegelik-võti`.
Kui fail juba eksisteerib, jäta `install ... /dev/null` käsk vahele,
et olemasolevat võtit mitte kustutada. Võti peab ühtima Atomi seadistusega.
Peata enne teenuse käivitamist vana käsitsi käivitatud Flask, kui see kasutab porti 5000.

```bash
sudo cp robot-postoffice.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now robot-postoffice
sudo systemctl status robot-postoffice
curl http://127.0.0.1:5000/api/status
sudo journalctl -u robot-postoffice -n 50 --no-pager
```

Caddy olemasolev `reverse_proxy 127.0.0.1:5000` sobib teenusega.
Kasuta täpselt ühte Gunicorni worker'it ja ühte thread'i: tööde olek on RAM-is.
Restardiga kaovad tööd ja last_seen; vana töö ei lühe uuesti täitmisele.

Rebooti katse (katkestab serveri ühendused): `sudo reboot`.
Pärast uuesti ühendamist kontrolli:

```bash
systemctl is-enabled robot-postoffice
systemctl is-active robot-postoffice
curl https://narva1.roboarena.org/api/status
```

Koodi uuendamise järel: `sudo systemctl restart robot-postoffice`.

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
