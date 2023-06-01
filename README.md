<img src='project_banner.png' width='800'>

# Secure MQTT: Lightweight and Safe Communication for IoT

## Table of Contents
- [Secure MQTT: Lightweight and Safe Communication for IoT](#secure-mqtt-lightweight-and-safe-communication-for-iot)
  - [Table of Contents](#table-of-contents)
  - [Problem Statement](#problem-statement)
  - [Project Summary](#project-summary)
  - [Appendix](#appendix)
    - [Prerequisites](#prerequisites)
    - [Credits](#credits)
    - [License](#license)

## Problem Statement

[(Back to top)](#table-of-contents)

The present project aims to develop a robust communication infrastructure for efficient and secure data exchange between auditors and a server (see Figure 1). With a focus on energy measurement and monitoring, we aim to establish a fast and secure channel that enables auditors to transmit data to a central server. Leveraging advanced technologies like public key infrastructure (PKI) and encryption algorithms, we will ensure the reliability, confidentiality, and integrity of the transmitted energy data.

|   <img src='docs/report/img/dataExchange.png' width='800'>    |
| :-----------------------------------------------------------: |
| *Figure 1: Data exchange between the auditors and the server* |

By implementing a PKI, we aim to address the following challenges:

1. **Authentication and Authorization**: The system needs a reliable method to authenticate the identities of the auditors and the server. Only verified and authorized members should be able to access the server and exchange data with it. The server should also be able to authenticate the auditors to send them general updates and alerts.

2. **Confidentiality**: The system needs to ensure that the data exchanged between the auditors and the server is encrypted and protected from unauthorized access.

3. **Data Integrity and Non-repudiation**: Without a robust PKI in place, there is no guarantee of data integrity and non-repudiation, making it challenging to verify the accuracy and authenticity of audit information exchanged between the auditors and the server.

4. **Scalability and Performance**: As the volume of audit data increases, the network infrastructure must be able to balance the highly variable communication load

Addressing these challenges is critical to ensuring the confidentiality, integrity, and availability of audit information throughout the communication process. By implementing a PKI, we aim to establish a secure channel that enables encrypted communication, robust authentication and authorization mechanisms, data integrity, non-repudiation, and scalable performance. This will bolster the trustworthiness of the communication channel, enhance audit processes, and provide a solid foundation for the secure exchange of sensitive information between the auditors and the server.

## Project Summary

[(Back to top)](#table-of-contents)

## Appendix

### Prerequisites

[(Back to top)](#table-of-contents)

- Domain acquisition
  - Acquired through IONOS with a discount for 1 year
  - The domain does not need to be protected by an SSL certificate in the site from which the domain was bought, the SSL certificate will be created later on inside the EC2 instance
  - Modify default DNS servers to use those created by the hosted zone
- Setup AWS account
  - Security Groups
  - Request SSL Certificate for acquired domain, create records in Route 53 when finished
  - Create EC2 instance
  - Add public ip address of EC2 instance to a new record in Route 53

### Credits

[(Back to top)](#table-of-contents)

### License

[(Back to top)](#table-of-contents)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.