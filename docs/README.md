# EC2 Broker Setup

The Mosquitto Broker needs to be setup in a central server, in this case an EC2 instance from AWS; the following steps were taken to setup the broker.

## Domain Name Acquisition

The present project acquired its domain name from [IONOS](https://www.ionos.com/), but we encourage you to use any domain name provider of your choice. The following links provide information on how to acquire a domain name from IONOS and how to acquire a domain name in general.

- [IONOS Domain Acquisition Guide](https://www.ionos.com/digitalguide/domains/domain-tips/how-do-you-buy-a-domain-name/) **(Recommended)**
- [Google Domains](https://support.google.com/domains/answer/4491208?hl=en)

**NOTE**: The domain does not need to be protected by an SSL certificate in the site from which the domain was bought, the SSL certificate will be created later on inside the EC2 instance.

## EC2 Instance Setup

Before setting up the broker, follow this guides in order:

1. [EC2 Account Setup](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html)
2. [EC2 Instance Setup](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)

The project created an EC2 instance with the following specs:

- OS: Ubuntu 22.04.3 LTS
- Instance Type: t2.micro
- CPU: 1 vCPU @ 2.4GHz
- RAM: 1 GiB
- Storage: 30 GiB

### Domain Name Server Setup

1. Create a public hosted zone in Route 53 for the acquired domain name, follow [this guide](https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-public.html)
   1. As soon as the hosted zone is created, go back to the domain name provider and modify the default DNS server values to use those created by the hosted zone.

| <img src='report/img/hosted-ns.png' width='800'> |
| :---------------------------------------------------------------: |
| *Figure 1: Custom NS from hosted zone (on the right)*  |

2. Request a public certificate from AWS Certificate Manager (ACM) for the acquired domain name, following the steps in [this guide](https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-public.html). Register both your domain and the wildcard domain (e.g. `example.com` and `*.example.com`). Wait for the certificate to be verified, this can take up to 30 minutes.
   1. Once the certificate becomes available, click on it; and select _Create record in Route 53_ for both domains.
3. Modify the default Security Group assigned to the EC2 instance to allow inbound traffic from ports 1883 and 8883 from anywhere; there is no need to modify HTTPS, SSH or HTTP ports.
4. In the EC2 instance dashboard look for its public IP address and copy it.
   1. Go back to the hosted zone in Route 53 and create a new record with the copied IP address, this will be the address used to access the broker, you can follow the previous guide to create the record.
