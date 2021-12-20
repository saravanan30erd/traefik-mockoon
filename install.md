## Install mockoon-cli

We can install it using npm,

```
npm install -g @mockoon/cli
```

## Install Traefik HTTP provider

Clone this repository under `/opt` and copy the systemd file
`traefik-mockoon.service` to `/etc/systemd/system/traefik-mockoon.service`.

Enable and start the service,

```
systemctl enable traefik-mockoon
systemctl start traefik-mockoon
```

## Install and Configure Traefik

Download the traefik version which you want,

```
wget https://github.com/traefik/traefik/releases/download/v2.5.0/traefik_v2.5.0_linux_amd64.tar.gz
```

Unarchive and copy to bin folder,

```
tar -xvzf traefik_v2.5.0_linux_amd64.tar.gz
cp traefik /usr/local/bin/
chmod 755 /usr/local/bin/traefik
setcap 'cap_net_bind_service=+ep' /usr/local/bin/traefik
```

Create the traefik configuration folder,

```
mkdir /etc/traefik
mkdir /etc/traefik/dynamic
```

Configure the traefik static configuration file `/etc/traefik/traefik.yaml` as below,

```
global:
  checkNewVersion: true
  sendAnonymousUsage: true

entryPoints:
  web:
    address: :80
  websecure:
    address: :443

log:
  level: DEBUG
  filePath: "/var/log/traefik.log"

accessLog:
  filePath: "/var/log/traefik-access.log"

providers:
  file:
    filename: "/etc/traefik/dynamic/ssl.yaml"
  http:
    endpoint:
      - "http://127.0.0.1:8000/api/config?output=json"
```

Configure the dynamic configuration using file provider for SSL.
Example, Your Mock services FQDN is mock.example.com.
Place your SSL certificate `mock.crt` and private key `private.key`  of `mock.example.com`
under `/etc/traefik/ssl`.

Configure the default SSL settings in traefik `/etc/traefik/dynamic/ssl.yaml`,

```
tls:
  certificates:
    - certFile: /etc/traefik/ssl/mock.crt
      keyFile: /etc/traefik/ssl/private.key
      stores:
        - default

tls:
  stores:
    default:
      defaultCertificate:
        certFile: /etc/traefik/ssl/mock.crt
        keyFile: /etc/traefik/ssl/private.key
```

Thats all. Default configuration for traefik is done.

Traefik `routers` configuration for all the mock services will be generated automatically
by our `traefik-mockoon` HTTP provider.
