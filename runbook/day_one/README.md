## K3s Knowledge Base

I'm going to move a lot of the setup and day to day management documentation here, as well as start continually adding content around all the things I've learned on my *"Kubernetes based Homelab Journey"*. I have a large number of log entries, notes and the like around k3s that I've never shared and will start putting that content here. This front page will have a short list of key things to consider before getting started, followed by a table of contents for the rest. 


#### IMPORTANT Before Getting Started: seriously, read this first 

**You'll need to change the network interface names** on your K3s nodes so that they're ALL THE SAME, not doing this can cause issues with the load balancer and other networking. It's one of those things where it will seem like it's fine and everything is working, until things fall apart. A lot of the networking components will reference the same interface names for all devices, even if they're not all the same, so it's best to normalize the ethernet port names before you get started. 

**Read up on cluster management tools** and make sure you understand how they’ll impact your cluster before you start the build out. The reason for is that some tools are “read only” and don’t impact your cluster, while with others you’re effectively importing your cluster into a management plane that now has control of your cluster. More specifically:
* **Managing with Portainer:** Portainer is a "read only" management tool, so you can use it to manage your cluster and not impact anything you did with Ansible. 
* **Managing with Rancher:** AKA my preferred path, is a "management plane" meaning that when you deploy Rancher it effectively takes over your cluster and your K3s cluster becomes a ***Rancher Cluster***, and from that point on you need to do handle things like upgrading the K3s version, managing hardware and the like via Rancher, otherwise you can run into some rather nasty/irritating errors and problems. 

TL/DR – Management planes modify your cluster so they can monitor and maintain it’s health/state, while read only tools just make the requested changes and don’t per se “know anything” about your cluster. 

**To properly secure** your cluster you’ll need to have a domain name (for SSL certificates), and a firewall or router that allows you setup custom domains on your LAN. If you’re just tinkering this probably doesn’t matter but if you want to deploy things you’ll make regularly use of, properly securing things is just the way to go. See the [networking section](../networking/readme.md) for more.

**Take lots of notes and document everything**, especially when you figure out something difficult. 

The above out of the way, see the sections below for more information. 


### Available Content 


#### Kubernetes Management tools 

* Installing [Kubectl](../k3s_mgmt_tools/kubectl.md) on remote machines for managing your k3s cluster from the command line 

#### Networking 
* [Preparing](../networking/external-preparation.md) your home network to support Kubernetes 
* [Deploying Traefik](../../platform_services/traefik/readme.md) with secure certificates to enable secure access to the services you're hosting on Kubernetes.
* [Troubleshooting and solving K3s level DNS problems](../networking/fixing_dns_problems.md)

#### Storage
* [Fixing Volume Attach Errors](../storage/fixing_volume_attach_errors.md) - fixing a common cause(s) of volume attach errors when redeploying a workload.



