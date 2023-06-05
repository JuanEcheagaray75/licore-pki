# Broker Configuration

- [Broker Configuration](#broker-configuration)
  - [Mosquitto Installation](#mosquitto-installation)
  - [Mosquitto Setup](#mosquitto-setup)


## Mosquitto Installation

Mosquitto is already part of the Ubuntu 20.04 LTS repository. To install it, run the following commands:

```bash
sudo apt-get update;
sudo apt install -y mosquitto
```

As soon as you install the package, check its status:

```bash
sudo systemctl status mosquitto
```

You should see something like this:

```bash
● mosquitto.service - Mosquitto MQTT Broker
     Loaded: loaded (/lib/systemd/system/mosquitto.service; enabled; vendor preset: enabled)
     Active: active (running) since Fri 2023-05-26 01:49:00 UTC; 2 days ago
       Docs: man:mosquitto.conf(5)
             man:mosquitto(8)
    Process: 45552 ExecStartPre=/bin/mkdir -m 740 -p /var/log/mosquitto (code=exited, status=0/SUCCESS)
    Process: 45553 ExecStartPre=/bin/chown mosquitto /var/log/mosquitto (code=exited, status=0/SUCCESS)
    Process: 45554 ExecStartPre=/bin/mkdir -m 740 -p /run/mosquitto (code=exited, status=0/SUCCESS)
    Process: 45555 ExecStartPre=/bin/chown mosquitto /run/mosquitto (code=exited, status=0/SUCCESS)
    Process: 50139 ExecReload=/bin/kill -HUP $MAINPID (code=exited, status=0/SUCCESS)
   Main PID: 45556 (mosquitto)
      Tasks: 1 (limit: 1141)
     Memory: 3.3M
        CPU: 1min 27.856s
     CGroup: /system.slice/mosquitto.service
             └─45556 /usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf

May 26 01:49:00 ip-172-31-40-207 systemd[1]: Starting Mosquitto MQTT Broker...
May 26 01:49:00 ip-172-31-40-207 mosquitto[45556]: 1685065740: Loading config file /etc/mosquitto/conf.d/default.conf
May 26 01:49:00 ip-172-31-40-207 systemd[1]: Started Mosquitto MQTT Broker.
```

## Mosquitto Setup

The default configuration file is located at `/etc/mosquitto/conf.d/default.conf`. You can edit it to change the default settings. Copy and paste the `default.config` file from this repository to the `default.conf` file.

```txt
# Basic Configuration
allow_anonymous false
password_file /etc/mosquitto/passwd

# Unsecure MQTT
listener 1883 localhost

# SSL settings
listener 8883
cafile /etc/mosquitto/ca_certificates/ca-root-cert.crt
keyfile /etc/mosquitto/certs/broker.key
certfile /etc/mosquitto/certs/broker.crt

require_certificate true
use_identity_as_username true
```

As you can see from the previous text snippet, we need to install the specific certificates and keys into the previous directories. By this step the Control Center must have already created them. If not, please check the documentation on the [Certificate Creation Guide](../.test_certs/README.md)