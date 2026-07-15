## Technitium for Self Hosted DNS

### General Overview

Technitium's scope goes beyond the cluster as its managing numerous functions at the network level, not just for the cluster, including: 

* Local DNS, e.g., service.local.my-private-cloud-domain.com 
* DHCP - assigning IP addresses for all the devices on my home network, not just the nodes in the cluster
* Security: domain filtering, similar to what you get with pi-hole, filtering out bad domain requests, blocking tracking domains, etc. 
* Tracking domain requests/network activity per client/device 

The firewall (OPNsense) is configured to use the Technitium servers for DNS and DHCP. Each technitium instance runs its own instance of Traefik that uses Cloudflare and Lets Encrypt certificates to secure access to the technitium UI and to any other services running on that server. 

### Redundancy 

The initial approach was to use two Technitium server in parallel and then use the API to quickly mirror configs, static IPs, custom domain configurations, etc. However, Technitium recently added clustering and now the two Technitium servers part of a technitium cluster.  


### Deployment Resources 

* An example Docker Compose is available [here](deployment/compose.yaml) and the deployment instructions are available [here](deployment/readme.md)
*  [Instructions](deploying_services.yaml) on using Technitium for deploying services on your home network.





