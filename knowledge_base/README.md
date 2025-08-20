## k3s Knowledge Base

I'm going to move a lot of the setup and day to day management documentation here, as well as start continually adding content around all the things I've learned on my *"Kubernetes based Homelab Journey"*. I have a large number of log entries, notes and the like around k3s that I've never shared and will start putting that content here. This front page will have a short list of key things to consider before getting started, followed by a table of contents for the rest. 


#### IMPORTANT Before Getting Started: seriously, read this first 

**You'll need to change the network interface names** on your K3s nodes so that they're ALL THE SAME, not doing this can cause issues with the load balancer and other networking. It's one of those things where it will seem like it's fine and everything is working, until things fall apart. A lot of the networking components will reference the same interface names for all devices, even if they're not all the same, so it's best to normalize the ethernet port names before you get started. 

**Read up on cluster management tools** and make sure you understand how they’ll impact your cluster before you start the build out. The reason for is that some tools are “read only” and don’t impact your cluster, while with others you’re effectively importing your cluster into a management plane.  E.g., you can build with Ansible and import into Rancher, but once your cluster is in Rancher it’s effectively a “Rancher cluster” and you need to do as much around upgrading K3s versions, adding/removing HW, etc., in Rancher as doing those with Ansible can cause some nasty errors/problems. Conversely, you can build with Ansible and then manage with Portainer and still use Ansible to manage the HW without any problems. For the record, I love Rancher, but it’s still an important thing to keep in mind. 

TL/DR – Management planes modify your cluster so they can monitor and maintain it’s health/state, while read only tools just make the requested changes and don’t per se “know anything” about your cluster. 

**To properly secure** your cluster you’ll need to have a domain name (for SSL certificates), and a firewall or router that allows you setup custom domains on your LAN. If you’re just tinkering this probably doesn’t matter but if you want to deploy things you’ll make regularly use of, properly securing things is just the way to go. See the [networking section](networking/readme.md) for more.

**Take lots of notes and document everything**, especially when you figure out something difficult. 

The above out of the way, see the sections below for more information. 


### Available Content 


#### Kubernetes Management tools 

* Installing [Kubectl](mgmt_tools/kubectl.md) on remote machines for managing your k3s cluster from the command line 


#### Networking 
* [Preparing](networking/external-preparation.md) your home network to support Kubernetes 
* [Deploying Traefik](networking/traefik/) with secure certificates to enable secure access to the services you're hosting on Kubernetes.
* [Troubleshooting and solving K3s level DNS problems](networking/internal/fixing-common-problems.md)




