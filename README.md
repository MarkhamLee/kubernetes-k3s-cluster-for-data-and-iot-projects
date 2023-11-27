# K3s cluster for Data & IoT Projects

 My original plan was to just have a small .md file describing my k3s cluster that I'd add to the repo for one of my other projects. While I knew that building the k3s cluster would be a project in of itself, I greatly underestimated the amount of config files/deployment manifests, documentation/notes and custom code would be generated from it. I created this repo for a couple of reasons:

 * To document everything I've learned for later use 
 * To store what I hope will become a series of automations, re-useable .yaml files and the like to make building future clusters quick and easy. 
 * To pay it forward and hopefully add to the body of knowledge that others can use to spin up their own clusters for the first time. K8s is challenging and I really hope I can save some folks from some of the frustration that I experienced. One of the reasons I started assembling some of the documentation was because it was easy to learn how to get things up and running in a basic way, but securing your connections, exposing services outside of the cluster, high availability, etc., always required a bit of modification. Also, this space changes fast and the amount of out of date materials I found online was astonishing. 

*Note: it goes without saying that you should use anything here at your own risk, I guarantee nothing and am just sharing how I build out my setup/what worked for me.*


 ### A couple of assumptions 

A couple of items just to illustrate how I approached this project: 

* I built everthing on devices running Ubuntu, which implies that everything here "should" work on any debian distro and on Linux in general. Outside of that, just know that you'll probably run into some issues. 
* I took the approach of *"how would I build out something to support a minimally viable product for some sort of edge deployment/project at work?"*. Meaning cloud back-up, shared storage, secure certificates/encrypted connections and the like. Meaning: when this gets to a point where it seems rather over-engineered for a homelab, well, that was the point. I.e., it might get to be production production, but it should get close. 
* Everything here is based on building out a high availability cluster, i.e., one with at least three server nodes. I used small *"Intel NUC like"* Beelink SER5 Machines I picked up for $230/each on Amazon, 6C/12, 64GB of RAM, 2 TB NVME. I think they're a great deal price to performance wise, they made me question why I spent almost double for a 12th gen Intel NUC.  
* I use traefik for the ingress and letsencrypt to generate secure certs to make sure all of my connections are secure. 
* You want all services accessible on your home network via internal only domains, e.g., influxdb.local.yourdomain.com 
* I'm running firewall software on a dedicated machine that allows me to define domain names on my local network, e.g., grafana.local.example.com. If you're going to build a similar cluster you'll need something like pfSense or OPNsense, plus have an ISP that will give you the auth credentials to have your custom router login to your internet service without using the ISP supplied router. 
    * You might be able to configure the DNS and domains on the ISP supplied router, but I've never tried it and just bought a small form factor PC with dual 2.5 Gb ethernet, installed firewall software on it and kept it moving. 
* I have a publicly available domain name for setting up the secure certs
* I have an AWS account with S3 that I use for backing up longhorn (the shared storage solution)


### Acknowledgements & References: 
  
* I wouldn't have made it far enough to be able to know enough to share with others if it weren't for likes of [Techno Tim, follow him on YouTube](https://www.youtube.com/@TechnoTim/videos), after finding his channel I started building and tearing down clusters, giddy over being able to get the basics setup in a few minutes. 






