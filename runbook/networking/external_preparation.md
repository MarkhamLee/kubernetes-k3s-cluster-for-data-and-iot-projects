## External Network Preparation

Before building a K3s cluster, the local network will need to have some combination of Firewall and DNS server with the following capabilities: 

* **Define custom local domains:** meaning a domain name that only works on your local network, e.g., grafana.local.myhomelab.com - having this ability will be critical to setting up secure ingresses to your Kubernetes services. 
* **Control how IP addresses are assigned:** while even the worst of ISP software will allow you to assign static IP addresses, you'll need to also have the ability to ability to reserve ranges of IPs that the router won't dynamically assign to devices that connect to it. The reason for this is that you'll need to have a range of IPs that are reserved for the Kubernetes load balancer and another range that you can use for assigning static IPs to devices. If your router software only allows you to create static assignments, but doesn't allow you to reserve IP address ranges, you can easily run into issues where your router tries to assign an IP that Kubernetes expects to be able to use to for services. 

There are open source options for all the software you'd need to build a robust home network, everything from Firewalls, Routers, IP address (DHCP) and domain name (DNS) management. The Firewall and Router apps described below will both protect your network, plus give you a full featured array of features related to managing internal domains and IP addresses. They can also provide you with ad blocking, DNS filtering and other security features. 

* **Firewall:** [OPNsense[(https://opnsense.org/)] and [pfSense](https://www.pfsense.org/download/) are both great options for an enterprise software firewall that is available for free. Which one is better is up to you, but you can't go wrong with either option. Keep in mind that since both sell commercial versions of their product, it's easy to get lost on that part of their web sites, the links I provided take you to the community editions.
* **Router software:** [OpenWRT]](https://openwrt.org/) can be used in conjunction with the above to manage wireless access points OR it can be used stand alone as it has many of the same capabilities of the 'senses'. One cool thing about OpenWRT is that it was designed to give new life to low powered router hardware that would've otherwise been discarded, so it's fairly simple to find HW that can run it. 

In this folder there are setup instructions for both OPNsense and pfSense, but only OPNsense is currently being used for the cluster and the pfSense may be outdated. 

**Caveat:** many of these packages will require more control over your home network than your ISP may be willing to allow (E.g., Comcast), as you won't be able to set your own domain control, control IP addresses, etc. A common pattern is despite implementing the variety of work arounds you can find online, your network will randomly go down once your ISP tries to exert control in a way that your firewall software perceives as a threat. 

#### Building the Firewall/Router/Primary Network Device:
* opnSense and pfSense will require an x86 device with at least two LAN ports. An 8th Gen Intel i5 or faster should be sufficient 
* OpenWRT can run on slower hardware than the "senses" but similar hardware is still a good idea so you can take full advantage of security features. 

I started out with an N100 mini PC but later moved to mini-itx build so I could run more security features and run my local network at 10Gbe, plus run more security features. You can 100% say it's overkill, but that arguably applies to most home lab/that's the fun part and since you're here.... 


##### Additional network related software 

These are apps that would allow you to make things more robust by removing a single point of failure by having DHCP and DNS and the Firewall on separate devices, or just to extend your ad blocking, DNS filtering, DHCP and DNS capabilities beyond what the firewall or router provides. You don't explicitly need them, but if your firewall goes down, you'll wish you had them <-- ask how I know. 

* **Pi-Hole:** while primarily a *"network wide ad blocker"* [Pi-hole](https://pi-hole.net/) does this via blocking access to domains that are used for capturing your information, tracking or full-fledged nefarious/attacker like activities. This means it can also be used to define custom domains and manage your network's IP addresses. IF you have an ISP that works well with a tool like pfSense or openSense, this means that in the event of a firewall hardware failure, you could change a few settings in your ISP router and maintain your network despite losing your firewall. 

* **Technitium:** is a robust, dedicated tool for self-hosting DNS and managing IP addresses. [Technitium](https://technitium.com/dns/) allows you to add/remove static IP assignments via an API, upload files with your custom domains and is more of an enterprise class solution for DHCP and DNS compared to Pi-Hole. It also has pi-holes domain filtering capabilities by using open source "bad domain" block lists, you can also supplement those lists with your own list of blocked domains. 

* **Traefik:** Traefik is used both in the cluster and on external servers running network related utilities as proxy server that enables access to Technitium, OPNsense and other utilities. The servers that run Technitium and OPNsense each have their own Traefik instance to enable access to the network services they're running.

#### Additional External Dependencies

* **Sign up for Cloudflare:** you'll need a Cloudflare account to register secure certificates for your K3s reverse proxy/services, think: you can access a service at https://your-self-hosted-service.example.com without getting a browser warning about an unsecure connection, which also makes your services far less vulnerable to "man in the middle attacks". Another benefit of this Cloudflare account is that you'll also be able to use it for securing services you self host outside of Kubernetes, securing the entrance pages of your router or firewall UIs, etc. It's free and a key part of your tool kit for securing your homelab, home networking and Kubernetes, so there is no reason not to get one.
* **Register a Domain:** the domain is the 2nd requirement for registering secure certificates. You won't need to make it public facing via a web site or anything, but you need a proper domain to tie the certificate to. 

My suggestion for the above is to sign-up for Cloudflare and then register the domain through them. 

