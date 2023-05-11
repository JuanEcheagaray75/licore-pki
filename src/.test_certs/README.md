# Certificate generation

As of the development of this project, the MQTT broker used is [Mosquitto](https://mosquitto.org/). The following commands were used to generate the certificates used by the broker and the clients. The following commands are meant to be run in the EC2 instance used to host the broker. The certificates are generated using the [OpenSSL](https://www.openssl.org/) toolkit.

For ease of development we recommend first creating all the below mentioned certificates into a test directory and then moving them to the appropriate location. This policy does not apply to a production environment.

- [Certificate generation](#certificate-generation)
  - [Root CA](#root-ca)
  - [Broker](#broker)
  - [Sample Clients](#sample-clients)
    - [Publisher Client](#publisher-client)
    - [Database Client](#database-client)
  - [Permissions setup](#permissions-setup)
  - [File structure](#file-structure)


## Root CA

```bash
openssl ecparam -name prime256v1 -genkey -noout -out ca.key
openssl req -new -key ca.key -out ca-cert-request.csr -sha256
openssl x509 -req -in ca-cert-request.csr -signkey ca.key -out ca-root-cert.crt -days 365 -sha256
```

## Broker

```bash
openssl ecparam -name prime256v1 -genkey -noout -out broker.key
openssl req -new -key broker.key -out broker-cert-request.csr -sha256
openssl x509 -req -in broker-cert-request.csr -CA ca-root-cert.crt -CAkey ca.key -CAcreateserial -out broker.crt -days 360
```

## Sample Clients

### Publisher Client

```bash
openssl ecparam -name prime256v1 -genkey -noout -out auditor_mona.key
openssl req -new -key auditor_mona.key -out auditor_mona-cert-request.csr -sha256
openssl x509 -req -in auditor_mona-cert-request.csr -CA ca-root-cert.crt -CAkey ca.key -CAcreateserial -out auditor_mona.crt -days 360
```

### Database Client

```bash
openssl ecparam -name prime256v1 -genkey -noout -out database_licore.key
openssl req -new -key database_licore.key -out database_licore-cert-request.csr -sha256
openssl x509 -req -in database_licore-cert-request.csr -CA ca-root-cert.crt -CAkey ca.key -CAcreateserial -out database_licore.crt -days 360
```

## Permissions setup

Run the following commands in the EC2 instance used as a host for the broker.

```bash
# CA files
sudo chown mosquitto ca.key
sudo chown mosquitto ca-root-cert.crt

# Broker certificates
sudo chown mosquitto broker.key
sudo chown mosquitto broker.crt
```

Run the following command in the host machine for each client needed. The _user\_name_ specified must be replaced by the appropriate username for your machine, ex. _ubuntu_, _ec2-user_, etc.

```bash
# Client certificates
sudo chown user_name auditor_mona.key
sudo chown user_name auditor_mona.crt
```

## File structure

The following file structure is recommended for the certificates. After creating every certificate, switch directories to `/etc/mosquitto`; the regular installation of Mosquitto uses the `/etc/mosquitto` directory to store every configuration file for the broker. The following structure is meant to be used in the host machine.

```bash
.
├── ca_certificates
│   ├── ca.key
│   ├── ca-root-cert.crt
├── certs
│   ├── broker.crt
│   └── broker.key
```
