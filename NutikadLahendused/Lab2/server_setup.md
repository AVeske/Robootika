# Dropleti seadistamine

See dokument kirjeldab Nutikate Lahenduste Labor 2 jaoks kasutatava Ubuntu dropleti esmast seadistamist.

Serveri ülesanne on olla avalikus internetis paiknev vaheserver ehk **postkontor** kasutaja ja laboris oleva Atomi vahel.

Lõplik andmevoog:

```text
Kasutaja / brauser
        |
        | HTTPS
        v
      Caddy
        |
        | localhost
        v
   Flask server
        |
        | Internet
        v
      AtomS3R
        |
        | kohalik võrk
        v
       jaam
        |
        v
      MG400
```

Droplet ei loo ise ühendust laboris oleva Atomi või robotiga. Atom loob ise ühenduse dropletiga ja küsib perioodiliselt, kas talle on uusi töid.

---

## 1. SSH võtme loomine

Serverisse sisselogimiseks kasutatakse parooli asemel SSH võtmepaari.

Windows PowerShellis:

```powershell
ssh-keygen -t ed25519 -C "nimi-arvuti"
```

Vaikimisi salvestatakse võtmed:

```text
C:\Users\<kasutaja>\.ssh\id_ed25519
C:\Users\<kasutaja>\.ssh\id_ed25519.pub
```

Failide tähendus:

```text
id_ed25519      -> privaatne võti
id_ed25519.pub  -> avalik võti
```

Privaatset võtit ei saadeta kellelegi ega lisata Git reposse.


Avalik võti saadeti serveri haldajale, kes lisas selle dropleti:

```text
/root/.ssh/authorized_keys
```

Igal arvutil on oma SSH võti.

---

## 2. Serverisse ühendamine

Serverisse ühendamiseks:

```powershell
ssh root@<SERVERI_IP>
```

## 3. Uue tiimiliikme SSH võtme lisamine

Tiimiliige loob enda arvutis samuti SSH võtme:

```powershell
ssh-keygen -t ed25519 -C "nimi-arvuti"
```

Ta saadab ainult faili:

```text
id_ed25519.pub
```

sisu.

Serveris avada:

```bash
nano /root/.ssh/authorized_keys
```

Lisada uus avalik võti eraldi reale.

## 4. DNS

```bash
http://narva1.roboarena.org/
```

## 5. Ubuntu uuendamine

Enne rakenduste paigaldamist uuendati serveri paketiloend ja olemasolevad paketid.

```bash
apt update
```

`apt update` uuendab infot selle kohta, millised paketiversioonid Ubuntu repositooriumides saadaval on.

Seejärel:

```bash
apt upgrade -y
```

`apt upgrade` paigaldab olemasolevate pakettide uuemad versioonid.

Seda tehakse enne rakenduse paigaldamist, et server kasutaks värskeid turva- ja veaparandusi.

---

## 6. Vajalikud põhipaketid

Paigaldati:

```bash
apt install -y python3 python3-venv python3-pip git curl
```

### Python 3

```text
python3
```

Flask server kirjutatakse Pythonis.

Kontroll:

```bash
python3 --version
```

### python3-venv

Võimaldab luua Python **virtual environment'i**.

See hoiab selle projekti Python paketid eraldi Ubuntu süsteemipakettidest.

Näiteks:

```bash
python3 -m venv .venv
```

Aktiveerimine:

```bash
source .venv/bin/activate
```

### pip

```text
python3-pip
```

Python pakettide paigaldamiseks.

Näiteks hiljem:

```bash
pip install flask
```

või:

```bash
pip install -r requirements.txt
```

### Git

```text
git
```

Kasutatakse koolitöö repo serverisse kloonimiseks ja muudatuste uuendamiseks.

Kontroll:

```bash
git --version
```

### curl

```text
curl
```

Kasutatakse HTTP päringute, serverite ja API-de testimiseks.

Näiteks:

```bash
curl http://127.0.0.1:8000
```

---

## 7. Firewall ehk UFW

Server kasutab UFW-d ehk **Uncomplicated Firewall**.

Kontroll:

```bash
ufw status verbose
```

Enne tulemüüri aktiveerimist lubati SSH:

```bash
ufw allow OpenSSH
```

See on oluline, sest vastasel juhul oleks võimalik enda SSH ühendus serveriga blokeerida.

Veebiserveri jaoks lubati HTTP:

```bash
ufw allow 80/tcp
```

ja HTTPS:

```bash
ufw allow 443/tcp
```

Seejärel:

```bash
ufw enable
```

Kontroll:

```bash
ufw status
```

Avalikult peavad olema vajalikud ainult:

```text
22/tcp    SSH
80/tcp    HTTP
443/tcp   HTTPS
```

Flaski enda porti, näiteks `8000`, ei ole vaja avalikku internetti avada.

Flask kuulab ainult lokaalselt:

```text
127.0.0.1:8000
```

ja Caddy suhtleb Flaskiga serveri sees.

---

## 8. Caddy

Caddy paigaldati HTTPS pöördproksina.

**Pöördproksi ehk reverse proxy** võtab internetist kasutaja päringu vastu ja suunab selle sisemisele Flask rakendusele.

Lõplik struktuur:

```text
Internet
    |
    | HTTPS :443
    v
  Caddy
    |
    | localhost
    v
127.0.0.1:8000
    |
    v
  Flask
```

Caddy kasutamise põhiline põhjus on automaatne HTTPS sertifikaatide haldus.

Kontroll:

```bash
caddy version
```

Caddy teenuse olek:

```bash
systemctl status caddy
```

Teenust saab vajadusel restartida:

```bash
systemctl restart caddy
```

Konfiguratsiooni põhifail:

```text
/etc/caddy/Caddyfile
```

Lõplik konfiguratsioon hakkab olema ligikaudu:

```caddy
<SERVERI_DNS_NIMI> {
    reverse_proxy 127.0.0.1:8000
}
```

See tähendab:

```text
https://http://narva1.roboarena.org/
```

suunatakse lokaalselt töötavale Flask serverile:

```text
http://127.0.0.1:8000
```

---


## 9. Git repo kloonimine

Koolitöö Git repo klooniti dropletisse.

Repo on kloonitud:

```bash
cd /root
git clone <REPO_URL> Robootika
```

Tulemus:

```text
/root/Robootika/
```

## 10. Hetkeseis - 03.10.2026

Valmis:

- SSH võtmega ühendus dropletisse
- mitme tiimiliikme SSH võtmed
- Ubuntu paketid uuendatud
- Python 3 paigaldatud
- Python `venv` tugi paigaldatud
- `pip` paigaldatud
- Git paigaldatud
- `curl` paigaldatud
- UFW tulemüür seadistatud
- SSH port lubatud
- HTTP port lubatud
- HTTPS port lubatud
- Caddy paigaldatud
- Git repo serverisse kloonitud

Järgmised sammud:

- Flask postkontori rakendus
- Flask `requirements.txt`
- Flask virtual environment
- Flaski lokaalne test
- Caddy `reverse_proxy` seadistus
- HTTPS test avaliku DNS nime kaudu
- Flask rakenduse automaatne käivitamine `systemd` abil
- Atom polling API ühendamine
- sõnumite aegumine
- Atom `last_seen`
- töö tulemuse serverisse tagastamine

---

SSH privaatvõti jääb ainult arvutisse, kus see loodi.

Atom API võti salvestatakse hiljem Atomi seadistusse, mitte Git reposse.

Avalikku internetti ei avata Flaski sisemist porti. Flaskile pääseb väljast ligi Caddy ja HTTPS kaudu.