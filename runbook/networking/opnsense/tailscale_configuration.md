## Initial Tailscale Configuration

### Tailscale and opnSense

#### Basic Setup

* You're going to find instructions online telling you to install Tailscale from the command line:
    * Don't, it won't work, you'll get errors, install from the UI instead
    * You will, however, need to do the initial login from the command line 
    * Your mileage may vary here, but that's what worked for me. 

#### Routing non Tailscale devices to Tailscale IPs

If you're using your opnSense router as an exit node or subnet router, expect inconsistent behavior and/or the configuration below not to work. Not saying it can't be done, just saying that I had issues with this on pfSense and OpenWRT so I didn't bother trying it on opnSense. 

* If you want your router to route requests from non Tailscale devices to Tailscale IPs:
    * Setup the appropriate ACLs in Tailscale to limit access
    * Create an Alias of only the devices you want to be able to do this, opening up your entire Tailnet to your LAN runs contrary to the point of using Tailscale, no? 
    *  Add the Tailscale interface via the same process indicated above for interfaces 
    * Create a NAT rule:
        * Type: Hybrid Outbound
        * Interface: Tailscale
        * Source: your alias with the select group of servers
        * Source, Destination & NAT ports should be wildcards or "*" UNLESS you have a select group of ports you want to limit things to. 
        * For destination use a select # of Tailscale IPs via an Alias (ideal) or you could put * here, or the subnet for your Tailnet
        * For NAT address use Interface address
        * Select "Static Port" 
    * Everything "should" work with the NAT rule but it's good practice to also create a firewall rule:
        * Just clone an existing "Allow Any" rule and make two changes:
            * Use the Alias of your non Tailscale devices as the source and then make the destination your Tailscale interface name + "net" E.g., "Tailscale net" 
