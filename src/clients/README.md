# LiCore Clients

The present directory hosts the available python scripts that interact with the MQTT broker. There is a publisher and a subscriber; the publisher is used to send messages to the broker, while the subscriber is used to receive messages from the broker and store them in a database.

Each of the clients will share some pre-requisites, which are listed below.

- The organization must have created and sent the appropriate certificates to the corresponding clients. Follow the guide provided in the [Certificate Creation Guide](../.test_certs/README.md)
- Each client must have a Python 3 installation, as of now every Linux distribution comes with Python 3 pre-installed.

## Publisher

The publisher role is played by the auditors who will be sending messages to the broker. This project assumes that the auditors will be using a Linux distribution, specifically a Raspberry Pi 3 Model B

### General Specs

- OS: Debian GNU/Linux 11 (bullseye) x86_64
- Kernel: 5.10.0-15-amd64
- **CPU: 1 vCPU @ 2.49GHz**
- RAM: 1024 MiB
- Disk: 15 GiB

The Raspberry Pi had to be emulated using VirtualBox. One will note that the CPU provided to the VM has almost twice the speed of the actual Raspberry Pi 3 Model B. This is because the Raspberry Pi 3 Model B has a 1.2GHz quad-core ARM Cortex-A53 CPU, and VirtualBox does not support individual CPU customization; we tried to reduce the overall power of the machine by just providing a single CPU.

### Setup

```bash
sudo apt-get update
git clone https://github.com/JuanEcheagaray75/licore-pki/tree/master
cd licore-pki/src
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Request the appropriate private key from the organization and place it in
# ../.test_certs/
python3 publisher.py
```

## Subscriber

### General Specs

- OS: Ubuntu 20.04.6 LTS
- Kernel: 5.10.16.3-microsoft-standard-WSL2
- CPU: 12th Gen Intel i5-12450H (12) @ 2.496GHz
- RAM: 3919MiB
- Disk: 256GiB SSD

### Database Management

- sqlite3: 3.31.1

```bash
sudo apt-get update
sudo apt install sqlite3
cd db
./create_db.sh
```