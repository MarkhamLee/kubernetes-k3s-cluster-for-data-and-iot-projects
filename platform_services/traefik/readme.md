## Traefik for reverse proxy with Lets Encrypt Certificates for Encryption & Security

This section actually covers deploying multiple apps and setting up some integrations:
* Traefik for a reverse proxy and ingress to access your K3s services
* Lets Encrypt integration to generate secure certificates for free
* Cert Manager to manage the certificates
* Reflector to ensure that the certs are available within all the Kubernetes namespaces that need them. 

Once you complete the above, you'll be able to access the services deployed on K3s via secure connections to custom domains, E.g., "service.local.example.com" without triggering any browser warnings. 


### A couple of things before you get started: 

#### Details 

* The certificates are "wildcard certificates", think *.example.com, meaning, you don't need to register one for each service, you can just register one for the cluster and then clone that secret into each namespace that needs it. I.e., if you register a new certificate for each service, you're not registering a new certificate you're just renewing the same one over and over.
* While not required, "reflector" will make managing certificates and other resources a lot easier, as you can add a reflector annotation to a resource and then reflector will "reflect" it to each namespace you designated as needing it. 

### Pre-requisites

* This section presumes you've either read and/or completed the items discussed in in the section on [preparing your home network](../../external-preparation.md). Meaning:
    * You have a firewall or router up and running
    * You know how to create custom domains in the app above
    * You have your own domain setup and a cloudflare account 


You'll need to build a custom router/firewall like [pfSense](https://www.pfsense.org/) or [opnSense](https://opnsense.org/), to do this you'll need a "late model" x86 machine (preferably 8th gen Intel or newer) that has at least two LAN ports. While a mini PC can do just fine for this purpose your future upgrade options will likely be limited, if you want to ad more LAN ports, multiple WANs, support 10Gbe networking, etc., so choose HW with an upgrade path in mind. 

* Make sure you know how to create local domains (or host overrides) on your local network
    * In pfSense it's under services --> DNS resolver
* The secure certificates will require you to register a publicly available domain name (you won't need a public IP or to build a web site), and you'll need a Cloudflare account as well. Suggestion: create a Cloudflare account and then register the domain via same, you can get one from Cloudflare for an annual cost of $10. 

The above means you might have to pull together some hardware and wait for your new Domain to propagate to DNS servers, etc., before you get started. 

