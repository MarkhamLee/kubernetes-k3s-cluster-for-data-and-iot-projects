## Basic Setup 

Ideally you would use a device with multiple LAN ports, as this would allow enable you to designate one for management only and/or be a fallback position if you have network issues and can't access the device from the main network. I.e., you'd have WAN(s), the management only LAN and then the LAN(s) for your network. Here is how I set things up:

### Initial Interfaces

* You'll likely need to configure the initial ones from the command line, so plug a monitor and a keyboard into your opnSense instance.
    * It "should" automatically detect your LAN vs WAN, but this didn't work for me (with two different devices) so I had to do it manually. My advice, plug in the WAN first and then if you're not sure which is which, use trial and error until you get an IP address from the WAN. 
    * Repeat the above until you see the IP for port you want to use as LAN
* Once I had LAN port designated with the baseline 192.168.1.1 IP I connected a Raspberry Pi to it that was running Tailscale and was advertising the subnet 192.168.1.1/24. This gave me my entry point. I would suggest not changing this IP as it can break things, and then you'll find yourself not able to access OPNsense without direct/physical access to the firewall, on top possibly needing to reset opnSense to factory settings. Also: if you try to change the baseline IP, OPNsense strongly warns you not to, so, why go through the trouble? 
* I never changed the DHCP server for this interface either, I let opnSense manage this one and then used my external DNS and DHCP servers for the rest. Similarly to the above, it just gives you secure fallback position in case of broader network problems. 


### Setting up your primary network interfaces

1) Go to Interfaces --> Assignments
2) All you're doing on this page is "activating" the interface, by selecting it from the drop down, giving it a name and clicking "add". That's all you can do on this page. Once you do this you should see the interface listed when you click interfaces. 
3) Click the name of the interface so you can configure and use it:
    1) Click "Enable Interface" to start configuring the interface, doing so will cause the rest of the options to appear. 
    2) If you're configuring a WAN network click both of the "Block" options for private and bogon networks. 
    3) Set a static IP so that the device always has the same IP, as this will be the "gateway" IP that other devices (including your DNS server) will use to reach the firewall and from there the public internet. 
    4) **Here is a gotcha:** input a static IP but make sure the drop down to the right of the static IP is set to 24 NOT the default value of 32. 
    5) Click save. 
    6) DNS and DHCP 
        1) If you're using external DNS and DHCP your firewall will pick those up from your network, but it's a good idea to configure the DNS IPs under System --> Settings --> General --> Networking --> DNS Servers 
        2) If you're using one of the DNS and DHCP options included with opnSense:
            1) For Dnsmasq DNS & DHCP just click that option and under interface the drop down will let you select multiple interfaces.
            2) For ISC DHSCPv4 if you click that option, a sub-menu will appear that will show your interface name, just click that to configure it. 
    4) At this point the interface will work fine for internal access, but it won't be able to reach the internet until you configure a firewall rule for it. The initial interface you configure will have automatic firewall rules configured for it, but the additional ones "wait for the admin" to configure the rules. 
        1) Go to firewall --> rules, and click the interface called LAN (or whatever the initial interface you configured was called). Click the clone option to clone the rule.
        2) Change the interface drop down to the name of your new interface and then change Source to the "name of interface net" e.g., "LAN2 net". Do this for both IPv4 and IPv6 (or whatever you're using)

From here your interface should be able to reach the internet. 

One additional item, you can select the parent WAN for an interface, so it's possible to have multiple WANs and use them for different networks. 

### Configuring Telegraf

This is fairly simple, but there are a couple of pitfalls you can encounter if you're using multiple LAN ports, IP ranges, external DNS and the like. 

* This probably seems obvious, but the instructions for InfluxDB in opnSense show using a URL + the Port #. Don't use the port number if you're using a reverse proxy into InfluxDB that already handles the port #. 
* Set the timeout to 30 seconds, otherwise you may run into issues, especially the first time you try to connect and InfluxDB is behind a proxy. 
* If you're using a local/LAN only domain name for your InfluxDB (or other destination) URL, you should configure DNS servers under System --> Settings --> General --> DNS Servers so that general system functions like Telegraf to reach those domains. I would also disable the default localhost 127.0.0.1 as an option (Settings --> General --> DNS Server Options), otherwise Telegraf will look for the domain via 127.0.0.1 and it won't be able to find it. 


### Firewall Rules 

* If you setup an alias, make sure to hit enter after each host, ip, etc., otherwise spaces or other unneeded characters will get inserted and your alias won't work. 


