## A couple of preparation steps before getting started with encryption
* Setup a custom router using a firewall package like [pfSense](https://www.pfsense.org/) or [OPNsense](https://opnsense.org/), ideally you'd install this on a computer with at least two LAN ports (e.g., a firewall appliance) but any machine that can run Linux should do. I run mine on a Trigkey G5 N100 with dual 2.5Gbe and it's worked flawlessly. 
* Make sure you know how to create local domains (or host overrides) on your local network
    * In pfSense it's under services --> resolver 
* Create a CloudFlare account and setup a publicly available domain if you want to go the full encryption route 


### Setting up your cluster with secure certificates

* The simple answer is to just follow [Tim's tutorial](https://www.youtube.com/watch?v=G4CmbYL9UPg&t=1344s), but with a couple of extra points that should make your life easier: 
    * When looking at the traefik dashboard, the full URL will be something like: traefik.local.example.com/dashboard/ make sure you have the /dashboard/ after your URL or you'll get a 404 message. 
    * If the above doesn't work, go back a few steps and just do them over, it's a lot of information to work through and it's easy to miss a step. 
    * 404 messages aren't actually bad, they mean you're hitting the right service, but you've made a small error in your URL somewhere 
    