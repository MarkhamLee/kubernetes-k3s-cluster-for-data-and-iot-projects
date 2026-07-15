## Tailscale Deployed Services 

These services are deployed directly to a server that is functioning a Tailscale deployed private cloud server, meaning the services are only available to devices on my Tailnet with the appropriate permissions. These deployments differ from the typical stand-alone deployment in a couple of ways: 

* Instead of using Traefik + Cloudflare + LetsEncrypt for Certificates, certificates are managed via Traefik and Tailscale. 
* You can have multiple secure paths to your services, this dual approach gives you the ability to have simple local LAN access and a Tailscale only URL that you use when you're away from home. Keep in mind the 2nd path is optional, 
    * Tailscale access in the form of: <tailscale_server_url>/service_name. Keep in mind that the  Traefik configs will require some extra steps/special changes so the services are available
    * You can use a separate Traefik instance (e.g., a Traefik instance on your DNS server), to still configure local LAN access in the form of service_name.local.your-private-cloud-domain.com. 

The advantage of this type of approach is that you could deploy a server or back-up server running critical application at a relative's house, at a co-location, etc., as long as the device has internet it's just plug and play in terms of deploying the server outside of your home. 

