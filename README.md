# Kubernetes - K3s cluster for Data & IoT Projects

This repo contains documentation, links to tutorials, notes, installation instructions, values.yaml files for installing applications and custom code I used to build a high availability K3s cluster. I built this cluster to support my [Productivity, Home IoT, Weather, et al project](https://github.com/MarkhamLee/productivity-music-stocks-weather-IoT-dashboard) in addition to some other things I'm working on. While I knew this would be a project in of itself I wasn't planning on creating a separate repo for it, instead, I was just going to drop a short .md file describing the cluster into the repos for the projects it was supporting. However, afer spending more time on the cluster than its related coding projects, editing 100s of lines of yaml, taking pages of notes, mapping out a CI/CD pipeline, etc., I decided to create this repo if for no other reason than to help others (and my future self) avoid some frustration when standing up k3s clusters.  

TL/DR: getting Kubernete setup properly can be difficult (especially for first timers), difficulties that are oft compounded by a lot of out of date and/or incomplete documentation, values.yaml files, tutorials, et al. Making things worse is the fact that a lot of the documentation is for building something rather basic, so things can get even more frustrating for those of us trying to something that is high availability, uses proper secure certificates, etc. 

 #### I created this repo for a couple of reasons:

 * To document everything I've learned for later use 
 * To store what I hope will become a series of automations, re-useable .yaml files and the like to make building future clusters quick and easy. 
 * To pay it forward and hopefully add to the body of knowledge that others can use to spin up their own clusters for the first time. K8s is challenging and I really hope I can save some folks from some of the frustration that I experienced. 
    * E.g., a lot of tutorials leave out the need to setup a local DNS for your cluster, or that if you want things to scale horizontally you need to set your persistent volume claims to ReadWriteMany <-- this tripped me up for three days. 

*Note: it goes without saying that you should use anything here at your own risk, I guarantee nothing and am just sharing how I built out my setup/what worked for me.*

#### General approach, relevant technologies, etc. 

* Everything here is based on building out a high availability cluster, i.e., one with at least three server nodes and deploying three pods (when possible) for each workload. 
* I built everything on devices running Ubuntu, which implies that everything here "should" work on any debian distro and on Linux in general. Outside of that, just know that you'll probably run into some issues. 
* I took the approach of *"how would I build out something to support a minimally viable product or proof of concept for an edge deployment/project at work?"*. Meaning: cloud back-up, shared storage, secure certificates/encrypted connections, CI/CD for custom code, etc. AKA a purposely over-engineered homelab cluster. *E.g., Grafana doesn't need to be HA when it's just me using it.* TL/DR: I tried/am trying to build something that might not get to the level of "production production"*, but should be close. 

#### My Cluster 
* **Hardware:** 
    * **Server/control plane nodes:** three "Intel NUC like" **Beelink SER5s running Ryzen 5 5560u processors (6c/12t), 64 GB of RAM and 2 TB of storage**. I got them for around $225.00/each on sale from Amazon (down from around $300). With Geekbench 6 scores around 7k (in my testing), I think they comapre quite favorably to 12th gen Intel NUC i3s and arguably even i5s from a price to performance perspetive when you consider those units cost 2 - 2.5x as much.  The fans also run quieter than the ones in my 12th Gen Intel NUC, albeit at the cost of higher temperatures. 
    * **Agent/worker nodes:** 3 x Raspberry Pi 4B 8GB that are deployed around my home for monitoring climate, communicating with smart devices and other pending IoT related functions. I've set a "no schedule" taint on all of them as they're only being used to interact with hardware like Zigbee hubs, air quality sensors & other IoT devices. Note: I did try adding a 4GB Raspberry 4B but it was causing problems with the prometheus monitoring stack due to lack of RAM. 
    * The next planned hardware addition is likely a Rockchip 3588 device to experiment with running ML workloads on its NPU. 
* I use **Rancher** to manage the cluster, deploy apps, etc., I use the **Kube-Prometheus-Stack** to monitor the cluster.
* I use **Longhorn** to aggregate the hard drives on each device into a shared pool of storage, Longhorn reserves about 2/3rds of the total storage on each device for shared storage. 
* I use **AWS S3** to back-up both Longhorn storage and Rancher. 
* I use **Letsencrypt.org certs + Cloudflare and a publically available domain name** to secure the cluster and ensure all connections are encrypted/secure. I.e., avoid any browser errors from using self-signed certs. 
* I use **Traefik** for the ingress and **metallb** for the load balancer 
* I'm running a custom router with pfSense as the firewall software, aside from the obvious I also use this to create custom local domains for each service. Think: grafana.local.example.com 
* I have **Portainer** installed on each device that I use to run custom code in docker containers for things like monitoring device temps independently from the cluster. 

#### Future Items
* Find an alternative to the Kube-Prometheus stack for monitoring the cluster. As currently deployed it eats up a lot of system resources compared to what it does (I had to increase the RAM limit to 8 GB to keep it from crashing), and I think it's clearly veered into the uncertainty principle of having too much influence on that which it is observing. 
* Add dedicated agent nodes, as currently each node is functioning as a server and an agent
* Add arm64 nodes as part of experimenting with a multi-architecture cluster[DONE - Limited Scope]
    * Raspberry Pi 4B and Orange Pi 3B single board computers that are only being used to collect data from USB based devices and sensors, general purpose ARM nodes are pending. Those will likely be Orange pi 5+ or similar devices equipped with a Rockchip 3588 System on a Chip(SOC)
* Add two nodes that are solely dedicated to storage. 
* Experiment with [Project Akri](https://github.com/project-akri/akri), it allows you to add the USB devices attached to your various nodes as resources available to your entire cluster. I think this project holds some interesting possibilities for home automation projects and the like, in addition to edge deployments in agricultural or industrial spaces that leverage edge devices and sensors to monitor various processes. I.e., stronger redundancy, centralizing the control software for those sensors, etc. 
* Either move the motherboards in the Beelinks into a shared enclosure of some sort and/or upgrade the fans in order to better control temperatures. 
* Add automation for both setup and day to day management, i.e. handle the day DevOps/MLOps/Sys Admin tasks using some combination of Ansible, Flux and/or Terraform. 


### Acknowledgements & References: 
  
* I wouldn't have made it far enough to be able to know enough to share with others if it weren't for likes of [Techno Tim, follow him on YouTube](https://www.youtube.com/@TechnoTim/videos), after finding his channel I started building and tearing down clusters, giddy over being able to get the basics setup in a few minutes as opposed to the not so fun time I was having prior.
