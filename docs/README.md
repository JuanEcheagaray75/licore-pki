# EC2 Setup

- Domain acquisition
  - Acquired through IONOS with a discount for 1 year
  - The domain does not need to be protected by an SSL certificate in the site from which the domain was bought, the SSL certificate will be created later on inside the EC2 instance
  - Modify default DNS servers to use those created by the hosted zone
- Setup AWS account
  - Security Groups
  - Request SSL Certificate for acquired domain, create records in Route 53 when finished
  - Create EC2 instance
  - Add public ip address of EC2 instance to a new record in Route 53
