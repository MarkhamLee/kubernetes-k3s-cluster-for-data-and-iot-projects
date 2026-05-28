## Networking 

In many respects, your cluster will only be as stable as the networking infrastructure you build around it, e.g., if your firewall provides DHCP (IP Addresses), DNS in addition to handling firewall functions and it goes down for some reason, your entire cluster will be thrown into disarray due to not being able to connect to the internet and disrupting a lot of internal cluster communications. this section will cover things that aren't per se Kubernetes specific but are absolutely important to properly maintaining your cluster. 

TL/DR - don't ignore the external networking content, as in many cases it's often more important than the internal networking, as a good Kubernetes distribution + a solid reverse proxy application like Traefik will take care of a lot of those things for you. 

P.S. if it's a networking problem, there is a 99% chance that it's DNS

### How to use this section

* The markdown files directly in this folder are the key things to read/learn before getting started, they'll ensure that you have a rock solid foundation and help you to avoid most issues. 
* After the above things are split up by broad category, e.g., apps, deployments, management tools and networking. You'll find a mixture of general FAQs + folders/files with more detailed deep dives into specific subjects like home networking, service ingresses, etc.

Current content:

* [External preparation](external_preparation.md) has information on planning out your networking software/hardware stack, and how to resolve key dependencies like a cloudflare account and domain name for secure certificates.
* The [OPNsense](opnsense/readme.md) folder contains information on initial setup for opnSense, inclusive of initial setup, creating multiple LANs, setting up firewall rules and configuring a VPN. 
* [Traefik](../../platform_services/traefik/readme.md) covers setting up secure access to the services hosted on your K3s cluster via the Traefik reverse proxy app, cert manager and free let's encrypt secure certificates. The information provided includes documentation + deployment files. 
* [Fixing DNS Problems](fixing_dns_problems.md)