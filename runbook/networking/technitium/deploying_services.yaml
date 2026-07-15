## Deploying Services

Instructions for using Technitium to deploy services on your home network.

### Deploying K3s Services w/ Technitium
Deploying a new service on K3s involves the following networking related steps:
* Add a DNS entry for that service in Technitium (via the API or the UI), which points to the main load balancer IP for the cluster. E.g. 192.168.59.125
* The configured domain is added to the service's ingress definition 

After the service is deployed to the cluster by Argo CD, requests for that service will be routed to the cluster by Technitium in concert with the Firewall/Router, and then to the service by Traefik. 

### Deploying Alone Services w/ Technitium

"Stand alone" refers to a service or app deployed outside of Kubernetes. 

The typical approach to deploying stand-alone services involves:
* Using Traefik for the reverse proxy, either on the same server or on a separate one.
* Deploying the service as a Docker container, configuring it to use Traefik
* Creating a custom DNS entry in Technitium, e.g., 'servicename.local.homelab-domain.com' that points to the IP of the Traefik instance the service was configured for. 