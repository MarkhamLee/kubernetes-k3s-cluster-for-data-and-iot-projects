## External Workloads

Between redundancy, database clustering, networking workloads and workloads that don't play nicely with K8s, there was a need for external servers that aren't part of K3s, but are just as critical to a broader "Private Cloud". This folder will contain documentation, Docker compose, and other content related to deploying and managing workloads on these machines. 

### Typical Delivery Model 
* Docker compose stored in Git, deployed on the server either from the command line or by Portainer. 

### Networking
* Each stand-alone server typically runs its own instance of [Traefik](../../runbook/networking/traefik_external/readme.md) as a proxy server to route requests to the app. Secure certificates are handled by Lets Encrypt and Cloudflare or Tailscale. 
    * A good rule of thumb is that if the server is setup to be deployed anywhere (e.g. back ups storage at a relative's house) than it would use Tailscale for secure certs, otherwise, it's Cloudflare. 
* Technitium is used as DNS to create the local domains, e.g., service.local.your-private-cloud-domain.com, you would create the local domain and point to the IP of the server running Traefik 
* Stand alone servers are usually running Tailscale for VPN even if they're not using it for secure certificates. 
