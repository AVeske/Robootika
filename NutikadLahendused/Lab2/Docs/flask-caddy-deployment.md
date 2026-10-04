# Flask serveri avalikustamine Caddy kaudu

### Hetkeseis: 04.10

Flask rakendus käivitati Ubuntu serveris ning see kuulab lokaalselt aadressil:

`127.0.0.1:5000`

Flaski ei avalikustatud otse internetti. Väliste HTTPS-päringute vastuvõtmiseks kasutatakse Caddy veebiserverit, mis töötab reverse proxy'na (vahendab välised päringud sisemisele Flask serverile).

Lahenduse ülesehitus:

`Internet → HTTPS → Caddy → 127.0.0.1:5000 → Flask`

Caddy konfiguratsioon asub failis:

`/etc/caddy/Caddyfile`

Projektis kasutatav konfiguratsioon:

```
narva1.roboarena.org {
    reverse_proxy 127.0.0.1:5000
}
```

Varasem Caddy vaikimisi `:80` HTTP-plokk eemaldati, kuna domeeninime kasutamisel haldab Caddy HTTPS-i automaatselt. Caddy hangib domeenile TLS-sertifikaadi ning suunab HTTP-päringud automaatselt HTTPS-i.

Konfiguratsiooni kontrollimiseks ja rakendamiseks kasutati:

```
caddy fmt --overwrite /etc/caddy/Caddyfile
caddy validate --config /etc/caddy/Caddyfile
systemctl reload caddy
systemctl status caddy
```

Flaski lokaalse töötamise kontrollimiseks kasutati:

```
curl http://127.0.0.1:5000
```

Avaliku HTTPS-ühenduse kontrollimiseks:

```
curl -I https://narva1.roboarena.org
```

Lõplikult kontrolliti veebilehe kättesaadavust ka välisest võrgust, kasutades telefonis mobiilset internetti:

`https://narva1.roboarena.org`

Seega on veebirakendus avalikult HTTPS-i kaudu kättesaadav, kuid Flask ise jääb lokaalsele liidesele. Caddy toimib interneti ja Flask rakenduse vahel turvalise reverse proxy kihina.
