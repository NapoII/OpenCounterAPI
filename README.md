[![downloads/total](https://img.shields.io/github/downloads/NapoII/OpenCounterAPI/total?style=for-the-badge)](https://github.com/NapoII/OpenCounterAPI/archive/refs/heads/main.zip) [![github/repo-size](https://img.shields.io/github/repo-size/NapoII/OpenCounterAPI?style=for-the-badge)](https://github.com/NapoII/OpenCounterAPI/archive/refs/heads/main.zip) [![github/license](https://img.shields.io/github/license/NapoII/OpenCounterAPI?style=for-the-badge)](https://github.com/NapoII/OpenCounterAPI/blob/main/LICENSE) [![github/last-commit](https://img.shields.io/github/downloads/NapoII/OpenCounterAPI/total?style=for-the-badge)](https://img.shields.io/github/issues/NapoII/OpenCounterAPI?style=for-the-badge) [![github/issues_open](https://img.shields.io/github/issues/NapoII/OpenCounterAPI?style=for-the-badge)](https://img.shields.io/github/issues-raw/NapoII/OpenCounterAPI?style=for-the-badge) [![github/stars](https://img.shields.io/github/stars/NapoII/OpenCounterAPI?style=for-the-badge)](https://github.com/NapoII/OpenCounterAPI/stargazers) [![discord](https://img.shields.io/discord/190307701169979393?style=for-the-badge)](https://discord.gg/knTKtKVfnr)

**The OpenCounterAPI** is a simple API for counting page visits and storing usage statistics. It runs on Flask and records visitor information such as IP address, browser data, and screen resolution. By sending a ***POST request*** to `/api/counter`, a page visit is logged and saved. The API uses JSON files for data storage and allows tracking of total visits and unique users. It’s ideal for websites that need a lightweight tracking solution without relying on external services.
## 📝 Table of Contents
+ [Demo / Working](#demo)
+ [How it works](#Use)
+ [Use free API](#usage_api)
+ [Host by your own](#usage_own)
+ [Buy me a coffee](#coffee)
+ [LICENSE](#LICENSE)
## 🎥 Demo / Working <a name = "demo"></a>

To see the API in action locally, open the HTML file inside the [Test Folder](test/) in your browser. This will allow you to interact with the API and observe how it tracks page visits.


## 💭 How it works <a name="Use"></a>

There are **two ways** to use the API:

A. **Use the free hosted API** – No setup required! Simply integrate it into your existing website with just a few clicks. [💻 A: Use free API](#usage_api).


B. **Self-host the API** – Run it on your own server for full control. Detailed setup instructions are provided in [💻 B: Host by your own](#usage_own).




## 💻 A: Use free API <a name="usage_api"></a>
The **free hosted API** allows you to integrate page visit tracking into your website **with just a few clicks** – no setup required!

In the **[test/](test/)** folder, you will find example implementations that show how to easily connect your site to the API. Simply follow the provided examples to start tracking page visits effortlessly.



## 💻 B: Host by your own <a name = "usage_own"></a>

## Prerequisites

- Python 3 installed
- Flask installed
- Access to a Linux server with sudo privileges

## 1. Create a New User

It is good practice to create a dedicated user for running the application to enhance security and separate permissions.

```bash
useradd --system -s /usr/sbin/nologin counter_apiuser -m
sudo groupadd counter_apigroup
sudo usermod -aG counter_apigroup counter_apiuser
```

if you use FileZilla:
```bash
sudo usermod -aG counter_apigroup {user with FileZilla}
```

```bash
sudo chgrp -R counter_apigroup /home/counter_apiuser &&
sudo chmod -R 770 /home/counter_apiuser &&
sudo chmod g+s /home/counter_apiuser
```

***Switch to the user with:***
```bash
sudo su - counter_apiuser -s /bin/bash
```


## 2. Set Permissions for the New User

Replace `/home/counter_apiuser/counter_api` with the actual path to your project directory.

## 3. Set Up a Virtual Environment

Log in as the newly created user:

```bash
sudo su - counter_apiuser -s /bin/bash
```

Navigate to your project directory and set up the virtual environment:

```bash
cd /home/counter_apiuser
mkdir counter_api
cd counter_api
python3 -m venv venv
source venv/bin/activate
```

## 4. Install Flask and Gunicorn

Move `requirements.txt` to `/home/counter_apiuser`, then install Flask and Gunicorn inside the virtual environment:

```bash
pip install -r requirements.txt
```

## 5. Set Up the Flask Application `open_page_counter_api.py`

Clone the repository and move the contents:

```bash
git clone https://git.napo-ii.de/napo/OpenCounterAPI.git
mv * ../    # Move all files since the structure is too deep
mv .[^.]* ../  # Move hidden files like .git
```

Delete the empty folder:
```bash
cd ..
rm -r OpenCounterAPI
```

## 6. Configure Gunicorn as a Service

Create a systemd service file for Gunicorn at `/etc/systemd/system/gunicorn.counter_api.service`:

```ini
[Unit]
Description=Gunicorn instance to service open_page_counter_api
After=network.target

[Service]
User=counter_apiuser
Group=www-data
WorkingDirectory=/home/counter_apiuser/counter_api
ExecStart=/home/counter_apiuser/counter_api/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8800 wsgi:app

[Install]
WantedBy=multi-user.target
```

## 7. Start and Enable the Service

Start the Gunicorn service and enable it to run at startup:
```bash
sudo systemctl start gunicorn.counter_api
sudo systemctl enable gunicorn.counter_api
```

## 8. Configure Nginx

Create an Nginx configuration file at `/etc/nginx/sites-available/open_page_counter_api`:

```nginx

# OpenCounterAPI
# change the config to your current steups

server {
    listen 80;
    listen [::]:80;
    server_name your_domain_or_ip;

    # Forwarding from HTTP to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name your_domain_or_ip.de www.your_domain_or_ip;

    # Paths to your SSL certificate and your private key
    # Change this part to your SSL certificate setup
    ssl_certificate /etc/letsencrypt/live/your_domain_or_ip/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your_domain_or_ip/privkey.pem;

    # Recommended SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;


    location / {
        proxy_pass http://127.0.0.1:8800;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```

Activate the configuration:
```bash
sudo ln -s /etc/nginx/sites-available/open_page_counter_api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 9. Important Commands for Managing the Gunicorn Service

To manage the Gunicorn service, use the following commands:

- **Start the service:**
```bash
sudo systemctl start gunicorn.counter_api
```

- **Stop the service:**
```bash
sudo systemctl stop gunicorn.counter_api
```

- **Restart the service:**
```bash
sudo systemctl restart gunicorn.counter_api
```

- **Check the service status:**
```bash
sudo systemctl status gunicorn.counter_api
```

- **View service logs:**
```bash
sudo journalctl -u gunicorn.counter_api
```

## 10. Fixing Permission Issues

If you encounter permission issues, run:
```bash
sudo chmod -R 775 /home/counter_apiuser/
```


## ☕ Buy me a coffee <a name = "coffee"></a>

Feel free to show your appreciation by treating me to a virtual coffee. Your support means a lot and keeps the creative coding vibes going! 🚀

<a href='https://ko-fi.com/M4M0TS4ZM' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi1.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

## 📚 LICENSE <a name = "LICENSE"></a>

[GNU GENERAL PUBLIC LICENSE Version 3](LICENSE)

[OpenCounterAPI](OpenCounterAPI) was created on 04.February.2025 by [NapoII](https://github.com/NapoII)



<p align="center">
<img src="https://raw.githubusercontent.com/NapoII/NapoII/233630a814f7979f575c7f764dbf1f4804b05332/Bottom.svg" alt="Github Stats" />
</p>
