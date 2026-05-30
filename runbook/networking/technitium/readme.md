## Technitium

Technitium's scope goes beyond the cluster as its managing numerous functions at the network level, not just for the cluster, including: 

* Local DNS, e.g., service.local.my-private-cloud-domain.com 
* DHCP - assigning IP addresses for all the devices on my home network, not just the nodes in the cluster
* Security: domain filtering, similar to what you get with pi-hole, filtering out bad domain requests, blocking tracking domains, etc. 
* Tracking domain requests/network activity per client/device 

Two Technitium DNS servers are run in parallel to provide redundancy in case one of the servers is unavailable. The firewall (opnSense) is configured to use the Technitium servers for DNS and DHCP. Each server runs its own instance of Traefik that uses Cloudflare and Lets Encrypt certificates to secure access to the technitium UI and to any other services running on that server. 

Deploying a new service on K3s involves the following networking related steps:
* Add a DNS entry for that service in Technitium (via the API or the UI), which points to the main load balancer IP for the cluster. E.g. 192.168.59.125
* The onfigured domain is added to the service's ingress definition 

After the service is deployed to the cluster by Argo CD, requests for that service will be routed to the cluster by Technitium and the Firewall/Router, and then to the service by Traefik. 
