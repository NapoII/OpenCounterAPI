[![Downloads](https://img.shields.io/github/downloads/NapoII/OpenCounterAPI/total?style=for-the-badge)](https://github.com/NapoII/OpenCounterAPI/archive/refs/heads/main.zip)
[![Repo Größe](https://img.shields.io/github/repo-size/NapoII/OpenCounterAPI?style=for-the-badge)](https://github.com/NapoII/OpenCounterAPI)
[![Lizenz](https://img.shields.io/github/license/NapoII/OpenCounterAPI?style=for-the-badge)](https://github.com/NapoII/OpenCounterAPI/blob/main/LICENSE)
[![Letztes Commit](https://img.shields.io/github/last-commit/NapoII/OpenCounterAPI?style=for-the-badge)](https://github.com/NapoII/OpenCounterAPI/commits/main)
[![Offene Issues](https://img.shields.io/github/issues/NapoII/OpenCounterAPI?style=for-the-badge)](https://github.com/NapoII/OpenCounterAPI/issues)
[![GitHub Stars](https://img.shields.io/github/stars/NapoII/OpenCounterAPI?style=for-the-badge)](https://github.com/NapoII/OpenCounterAPI/stargazers)
[![Discord](https://img.shields.io/discord/190307701169979393?style=for-the-badge)](https://discord.gg/knTKtKVfnr)

**The OpenCounterAPI** is a simple API for counting page visits and storing usage statistics. It runs on Flask and records visitor information such as IP address, browser data, and screen resolution. By sending a ***POST request*** to `/api/counter`, a page visit is logged and saved. The API uses JSON files for data storage and allows tracking of total visits and unique users. It’s ideal for websites that need a lightweight tracking solution without relying on external services.
## 📝 Table of Contents
+ [Demo / Working](#demo)
+ [How it works](#Use)
+ [Use free API](#usage_api)
+ [Host by your own](#usage_own)
+ [Buy me a coffee](#coffee)
+ [LICENSE](#LICENSE)
## 🎥 Demo / Working <a name = "demo"></a>

[ >> Demo Page <<](https://napoii.github.io/OpenCounterAPI/)

To see the API in action locally, open the HTML file inside the [Test Folder](test/) in your browser. This will allow you to interact with the API and observe how it tracks page visits.


## 💭 How it works <a name="Use"></a>

There are **two ways** to use the API:

A. **Use the free hosted API** – No setup required! Simply integrate it into your existing website with just a few clicks. [💻 A: Use free API](#usage_api).


B. **Self-host the API** – Run it on your own server for full control. Detailed setup instructions are provided in [💻 B: Host by your own](#usage_own).



## 💻 A: Use free API <a name="usage_api"></a>
The **free hosted API** allows you to integrate page visit tracking into your website **with just a few clicks** – no setup required!

In the **[test/](test/)** folder, you will find example implementations that show how to easily connect your site to the API. Simply follow the provided examples to start tracking page visits effortlessly.

To integrate OpenCounterAPI into your website, add the following script tag inside your HTML:

```html
<script src="https://api.learntogoogle.de/OpenCounterAPI.js" data-page="YOUR_PAGE_NAME"></script>
```

Make sure to replace `YOUR_PAGE_NAME` with the actual name of your page.

## Example Usage
Add this snippet to display live statistics on your page:

```html
<h1>Live Stats</h1>
<p>👤 Now: <span data-placeholder="now">Loading...</span></p>
<p>🗓 Today: <span data-placeholder="24h">Loading...</span></p>
<p>🖖 This Week: <span data-placeholder="week">Loading...</span></p>
<p>🗓 This Month: <span data-placeholder="month">Loading...</span></p>
<p>👤 Unique Users: <span data-placeholder="user_uniq">Loading...</span></p>

<script src="https://api.learntogoogle.de/OpenCounterAPI.js" data-page="YOUR_PAGE_NAME"></script>
```

## Features
- **Free & Hosted**: No backend setup required.
- **Live Stats**: Get real-time visitor data.
- **Easy Integration**: Just a single script tag.

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

## 2. Clone the Repository
To set up the environment for the user `counter_apiuser`, clone the repository into the appropriate directory:

```bash
cd /home/counter_apiuser && git clone https://github.com/NapoII/OpenCounterAPI
```

## 2. Keep the Repository Updated Automatically
To ensure the repository stays updated, create a cron job:

```bash
crontab -e
```

If this is your first time using `crontab`, the system will prompt you to choose a default text editor. Select the corresponding number, for example, `1` for nano.

### Add the Following Line to the Crontab File
At the end of the file, append the following:

```ini
0 3 * * * cd /home/counter_apiuser/OpenCounterAPI && git reset --hard origin/main && git pull origin main --force
```

This cron job will check for updates and pull the latest changes from the repository every day at 3 AM.


## 3. Set Up a Virtual Environment
change the user to `counter_apiuser`

```bash
sudo su - counter_apiuser -s /bin/bash
```

Navigate to your project directory and set up the virtual environment:


```bash
cd /home/counter_apiuser
python3 -m venv venv
source venv/bin/activate
```

## 4. Install Flask and Gunicorn

```bash
pip install -r /home/counter_apiuser/OpenCounterAPI/requirements.txt
```

## 5. Configure Gunicorn as a Service
As a normel user or root:

Create a systemd service file for Gunicorn
`nano /etc/systemd/system/gunicorn.counter_api.service`

```ini
[Unit]
Description=Gunicorn instance to service OpenCounterAPI
After=network.target

[Service]
User=counter_apiuser
Group=www-data
WorkingDirectory=/home/counter_apiuser/OpenCounterAPI/OpenCounterAPI
ExecStart=/home/counter_apiuser/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8800 wsgi:app

[Install]
WantedBy=multi-user.target
```

## 7. Start and Enable the Service

Start the Gunicorn service and enable it to run at startup:
```bash
sudo systemctl start gunicorn.counter_api
sudo systemctl enable gunicorn.counter_api
sudo systemctl status gunicorn.counter_api
```

If an error occurs, you can retrieve logs using the following command:

```bash
sudo journalctl -u gunicorn.counter_api
```

## 8. Configure Nginx

Create an Nginx configuration file at `/etc/nginx/sites-available/open_page_counter_api`:

```nginx

# OpenCounterAPI
# change the config to your current setup

server {
    listen 80;
    listen [::]:80;
    server_name your_domain_or_ip.com;

    # Forwarding from HTTP to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name your_domain_or_ip.com www.your_domain_or_ip.com;

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

    # Serve OpenCounterAPI.js directly
    location /OpenCounterAPI.js {
        root /home/counter_apiuser/OpenCounterAPI/test/js;
        autoindex off;
        add_header Content-Type application/javascript;
    }
}


```

### Explanation of the Configuration

1. **Redirect HTTP to HTTPS**
   - The first server block listens on port 80 and redirects all requests to HTTPS using a 301 permanent redirect.

2. **Handling HTTPS Traffic**
   - The second server block listens on port 443 (SSL) and ensures secure communication.
   - It requires a valid SSL certificate and private key (update paths accordingly).
   - TLS v1.2 and v1.3 are enforced for security.

3. **Proxying Requests to the API**
   - Requests to the root (`/`) are forwarded to `http://127.0.0.1:8800`, where the Open Page Counter API is running.
   - Proxy headers are set to ensure proper forwarding of the request details.

4. **Serving the JavaScript API File**
   - The `OpenCounterAPI.js` file is served directly from the specified directory.
   - The correct content type (`application/javascript`) is added to the response.


## Applying the Configuration

After adding the configuration file, enable it by creating a symbolic link and restarting Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/open_page_counter_api /etc/nginx/sites-enabled/
sudo nginx -t  # Test for syntax errors
sudo systemctl restart nginx
```

### Notes
- Replace `your_domain_or_ip.com` with your actual domain or server IP.
- Ensure that your SSL certificate paths are correctly set up.
- The Open Page Counter API should be running on port 8800 for this configuration to work properly.



# Important Commands for Managing the Gunicorn Service

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

## Fixing Permission Issues

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
