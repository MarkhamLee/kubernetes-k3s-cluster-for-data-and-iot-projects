# Kubernetes - K3s cluster for Data & IoT Projects

A K3s cluster I initially built to support my [Data Ingestion & IoT Project](https://github.com/MarkhamLee/productivity-music-stocks-weather-IoT-dashboard), my original plan was to maybe have a short .md file describing it in the repo for my other project as while I knew it would be a project in of itself I didn't think it was "repo" worthy. However, after noticing that this project was far more time intensive than the other one, dealing with hit or miss documentation, fixing charts, yaml files, etc., I quickly realized that this was not only a project in of itself, but one that was taking more time than the project it was built to support.  

Tl/DR: Kubernetes is hard, especially when you're trying to build out something that is HA, uses proper secure certificates, etc. I.e., it was easy for me to find the information I needed to do a basic setup, but something more robust, it was hit or miss, the only easy thing was to find out of date documentation. 

 #### I created this repo for a couple of reasons:

 * To document everything I've learned for later use 
 * To store what I hope will become a series of automations, re-useable .yaml files and the like to make building future clusters quick and easy. 
 * To pay it forward and hopefully add to the body of knowledge that others can use to spin up their own clusters for the first time. K8s is challenging and I really hope I can save some folks from some of the frustration that I experienced. 
    * E.g., a lot of tutorials leave out the need to setup DNS to support your cluster, or that if you want things to scale horizontally you need to set your persistent volume claims to ReadWriteMany <-- this tripped me up for three days. 

*Note: it goes without saying that you should use anything here at your own risk, I guarantee nothing and am just sharing how I built out my setup/what worked for me.*


#### My Cluster 
* Hardware: three "Intel NUC like" Beelink SER5s running Ryzen 5 5560u processors (6c/12t), 64 GB of RAM and 2 TB of storage. They're not on par with an Intel NUC 12th or 13th Gen i5s or even i3s, but given that they cost less than 1/2 as much for over 80% of the performance, I think they're a screaming deal. They also run fairly quiet, which is another bonus. I thought 64 GB of RAM might be overkill, but the system is currently using about 60GB of RAM total.. 
* I use **Rancher** to manage the cluster, deploy apps, etc., I use the **Kube-Prometheus-Stack** to monitor the cluster.
* I use **Longhorn** to aggregate the hard drives on each device into a shared pool of storage, Longhorn reserves about 2/3rds of the total storage on each device for shared storage. 
I use **AWS S3** to back-up both the Longhorn storage and Rancher. 
* I use **Letsencrypt.org certs + Cloudflare & a publically available domain name** to secure the cluster and ensure all connections are encrypted/secure, without using self-signed certificates and getting browser errors. 
* I use **Traefik** for the ingress and **metallb** for the load balancer 
* I'm running a custom router with pfSense as the firewall software, aside from the obvious I also use this to create custom local domains for each service. Think: grafana.local.example.com 
* I have **Portainer** installed on each device as a stand-alone app that I use to run a container that monitors device temps, reasons for this is just to capture some extra data I don't get in the Kube-Prometheus stack and because I might add some other telemetry like functionality in the future.  

#### Future Items
* Add some agent nodes 
* Add some arm64 nodes to experiment with a multi-architecture cluster 
* Either move the motherboards in the Beelinks into a shared enclosure of some sort and/or upgrade the fans, temps can spike into the mid 60s and I'm concerned of how hot they'll get as I add more workloads. 


#### A couple of items to illustrate how I approached this project: 

* I built everything on devices running Ubuntu, which implies that everything here "should" work on any debian distro and on Linux in general. Outside of that, just know that you'll probably run into some issues. 
* I took the approach of *"how would I build out something to support a minimally viable product that for some sort of edge deployment/project at work?"*. Meaning cloud back-up, shared storage, secure certificates/encrypted connections and the like. Meaning:  seems over-engineered for a homelab, well, that was the point. *I.e., it might not be "production production"*, but it should get close. 
* Everything here is based on building out a high availability cluster, i.e., one with at least three server nodes and deploying three pods (when possible) for each workload. 



### Acknowledgements & References: 
  
* I wouldn't have made it far enough to be able to know enough to share with others if it weren't for likes of [Techno Tim, follow him on YouTube](https://www.youtube.com/@TechnoTim/videos), after finding his channel I started building and tearing down clusters, giddy over being able to get the basics setup in a few minutes as opposed to the not so fun time I was having prior. 






