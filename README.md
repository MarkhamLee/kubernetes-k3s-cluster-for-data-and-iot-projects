# Kubernetes - K3s cluster for Data & IoT Projects

This repo contains documentation, links to tutorials, notes, installation instructions, values.yaml files for installing applications and custom code I used to build a high availability K3s cluster. I built this cluster to support my [Productivity, Home IoT, Weather, et al project](https://github.com/MarkhamLee/productivity-music-stocks-weather-IoT-dashboard) in addition to some other things I'm working on. While I knew this would be a project in of itself I wasn't planning on creating a separate repo for it, instead, I was just going to drop a short .md file describing the cluster into the repos for the projects it was supporting. However, afer spending more time on the cluster than its related coding projects, editing 100s of lines of yaml, taking pages of notes, mapping out a CI/CD pipeline, etc., I decided to create this repo if for no other reason than to help others (and my future self) avoid some frustration when standing up k3s clusters.  

TL/DR: getting Kubernetes setup properly can be difficult (especially for first timers), difficulties that are oft compounded by a lot of out of date and/or incomplete documentation, values.yaml files, tutorials, et al. Making things worse is the fact that a lot of the documentation is for building something rather basic, so things can get even more frustrating for those of us trying to something that is high availability, uses proper secure certificates, etc. 

 #### I created this repo for a couple of reasons:

 * To document everything I've learned for later use
 * To store a series of automations, re-useable .yaml files and the like to make building future clusters quick and easy. 
 * To pay it forward and hopefully add to the body of knowledge that others can use to spin up their own clusters for the first time. K8s is challenging and I really hope I can save some folks from some of the frustration that I experienced. 
    * E.g., a lot of tutorials leave out the need to setup a local DNS for your cluster, or that if you want things to scale horizontally you need to set your persistent volume claims to ReadWriteMany <-- this tripped me up for three days. 

*Note: it goes without saying that you should use anything here at your own risk, I guarantee nothing and am just sharing how I built out my setup/what worked for me.*

#### General approach, relevant technologies, etc. 

* Everything here is based on building out a high availability cluster, i.e., one with at least three server nodes and deploying three pods (when possible) for each workload. 
* I built everything on devices running Ubuntu, which implies that everything here "should" work on any debian distro and on Linux in general. Outside of that, just know that you'll probably run into some issues. 
* I took the approach of *"how would I build out something to support a minimally viable product or proof of concept for an edge deployment/project at work?"*. Meaning: cloud back-up, shared storage, secure certificates/encrypted connections, CI/CD for custom code, etc. AKA a purposely over-engineered homelab cluster. *E.g., Grafana doesn't need to be HA when it's just me using it, but I did it anyway* TL/DR: I tried/am trying to build something that might not get quite to the level of "production production"*, but should be close. 

#### My Cluster: High Availability, multi-architecture - arm64 and x86 
* **Hardware:** 
    * **Server/control plane nodes:** three "Intel NUC like" **Beelink SER5s running Ryzen 5 5560u processors (6c/12t), 64 GB of RAM and 2 TB of storage**. I got them for around $225.00/each on sale from Amazon (down from around $300). With Geekbench 6 scores around 7k (in my testing), you can think of them as getting about 80% of the performance of an 11th gen desktop i5 while using a fraction of the power. The fans also run quieter than the ones in my 12th Gen Intel NUC, albeit at the cost of higher temperatures. 
    * **Agent - Specialized Nodes:** 3 x Raspberry Pi 4B 8GB and that are deployed around my home for monitoring climate, communicating with smart devices and other pending IoT related functions as "sensor_nodes. These nodes all have a "NoSchedule" taint on them and Key Kubernetes components like Loki, Longhorn and Prometheus have a corresponding toleration, so that key Kubernetes components are deployed on these nodes but general workloads are excluded. 
        * I did try adding a 4GB Raspberry 4B but it was causing problems with the Prometheus monitoring stack due to lack of RAM. This is on my list of things to resolve, as being able to support low power edge devices for IoT applications is one of my core goals for this cluster.  
* **Software:**
    * I use **Rancher** to manage the cluster, do quick and dirty deployments (especially for testing containers) etc.
    * I use **Longhorn** to aggregate the hard drives on each device into a shared pool of storage, Longhorn reserves about 2/3rds of the total storage on each device for shared storage. 
    * I use **AWS S3** to back-up both Longhorn storage and Rancher. 
    * I use the **Grafana-Loki stack** for log aggregation
    * I use the **Kube-Prometheus-Stack** to monitor the cluster and **Alerts Manager** integrated with Slack to send alerts. 
    * **Kubectl** to deploy things from the command line, manage namespaces, etc.
    * I use **Letsencrypt.org certs + Cloudflare and a publically available domain name** to secure the cluster and ensure all connections are encrypted/secure. I.e., avoid any browser errors from using self-signed certs. 
    * I use **Traefik** for the ingress and **metallb** for the load balancer 
    * I'm running a custom router with **pfSense** as the firewall software, aside from the obvious I also use this to create custom local domains for each service. Think: grafana.local.example.com. I also use Letsencrypt.org certificates to encrypt the connection to the web UI (no pesky browser warnings). pfSense is also configured to send alerts via Slack and to make firewall data available via Prometheus and Telegraf. [Setup instructions pending]
    * I have **Portainer** installed on each device that I use to run custom code in docker containers for things like monitoring device temps independently from the cluster, I also use it to test Docker containers before deploying them to the cluster. 

#### Future Items 
* Currently deploying, testing integrating **Argo CD** for managing CI/CD pipelines 
* Automated, graceful cluster shutdown in response to a power outage, i.e., when the UPS is activated, graceful shutdown to avoid some of the nasty storage issues that from abrubt shutdowns. 
* Add dedicated agent nodes, as currently each node is functioning as a server and an agent/worker
* Add general purpose low power ARM64 agent/worker nodes, Orange pi 5+ or similar devices equipped with a Rockchip 3588 System on a Chip(SOC) [Currently Testing]
* Add two nodes that are solely dedicated to storage
* Add at least one MiniIO node, in particular to support Argo Workflows 
* Experiment with [Project Akri](https://github.com/project-akri/akri), it allows you to add the USB devices attached to your various nodes as resources available to your entire cluster. I think this project holds some interesting possibilities for home automation projects and the like, in addition to edge deployments in agricultural or industrial spaces that leverage edge devices and sensors to monitor various processes. I.e., your USB devices just become network devices and the software for them isn't tied to a specific piece of hardware. 
* Either move the motherboards in the Beelinks into a shared enclosure of some sort and/or upgrade the fans in order to better control temperatures. 
* Add automation for both setup and day to day management, i.e. handle the day DevOps/MLOps/Sys Admin tasks using some combination of Ansible, Flux and/or Terraform. 


### Acknowledgements & References: 
  
* I wouldn't have made it far enough to be able to know enough to share with others if it weren't for likes of [Techno Tim, follow him on YouTube](https://www.youtube.com/@TechnoTim/videos), after finding his channel I started building and tearing down clusters, giddy over being able to get the basics setup in a few minutes as opposed to the not so fun time I was having prior.
