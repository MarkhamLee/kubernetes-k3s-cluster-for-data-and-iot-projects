## Technitium

Technitium's scope goes beyond the cluster as its managing numerous functions at the network level, not just for the cluster, including: 

* Local DNS, e.g., service.local.my-private-cloud-domain.com 
* DHCP - assigning IP addresses for all the devices on my home network, not just the nodes in the cluster
* Security: domain filtering, similar to what you get with pi-hole, filtering out bad domain requests, blocking tracking domains, etc. 
* Tracking domain requests/network activity per client/device 

The firewall (OPNsense) is configured to use the Technitium servers for DNS and DHCP. Each technitium instance runs its own instance of Traefik that uses Cloudflare and Lets Encrypt certificates to secure access to the technitium UI and to any other services running on that server. 

The initial approach was to use two Technitium server in parallel and then use the API to quickly mirror configs, static IPs, custom domain configurations, etc. However, Technitium recently release clustering and now two Technitium servers are run in a cluster to ensure redundancy. 


### Deploying Services

#### K3s Services 
Deploying a new service on K3s involves the following networking related steps:
* Add a DNS entry for that service in Technitium (via the API or the UI), which points to the main load balancer IP for the cluster. E.g. 192.168.59.125
* The configured domain is added to the service's ingress definition 

After the service is deployed to the cluster by Argo CD, requests for that service will be routed to the cluster by Technitium in concert with the Firewall/Router, and then to the service by Traefik. 


#### Stand Alone Services

"Stand alone" refers to a service or app deployed outside of Kubernetes. 

The typical approach to deploying stand-alone services involves:
* Using Traefik for the reverse proxy, either on the same server or on a separate one.
* Deploying the service as a Docker container, configuring it to use Traefik
* Creating a custom DNS entry in Technitium, e.g., 'servicename.local.homelab-domain.com' that points to the IP of the Traefik instance the service was configured for. 

