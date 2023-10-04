# hope
Hope For Better Future

## Usage
```console
# install nginx & certbot
apt install nginx certbot python3-certbot-nginx

# start nginx
service nginx restart

# get certificate
# replace "api.yourDomain.com" with your subdomain
certbot --nginx -d api.yourDomain.com

# stop nginx
service nginx restart


# clone repo
git clone https://github.com/mheidari98/hope.git

cd ./hope/nginx

# replace your subdomain
find . -type f -exec sed -i 's/api.domain.com/api.yourDomain.com/g' {} +

# copy certificate
cp /etc/letsencrypt/live/api.yourDomain.com/fullchain.pem .
cp /etc/letsencrypt/live/api.yourDomain.com/privkey.pem .
cp /etc/letsencrypt/ssl-dhparams.pem .
cp /etc/letsencrypt/options-ssl-nginx.conf .

# install docker
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh

# build
docker compose build

# up
docker compose up -d
```

---

 file structure
 ```
.
├── docker-compose.yaml
├── proxy
│   ├── Dockerfile
│   └── app
│       ├── main.py
│       └── requirements.txt
└── nginx
    ├── Dockerfile
    ├── fullchain.pem
    ├── nginx.conf
    ├── options-ssl-nginx.conf
    ├── privkey.pem
    └── ssl-dhparams.pem
 ```

