## Details on Hardware

Just some quick details on the hardware I used to build this cluster, tips and tricks, problems I ran into, etc. 


#### Beelink SER5s - Ryzen 5 5560U
* These have been problem free, I got them, opened them up, replaced the RAM and NVME drives that came with them, installed Ubuntu and it's been smooth sailing. 
* The fans do have a slight "whir" noise in the background and they'll spin up more when you deploy services, however, you can reduce the temps and noise by placing them on their sides.


#### Orange Pi 3B
* Depending on your benchmark you get about 50-80% of the performance of a Raspbery Pi 4B, only with onboard NVME and eMMC support.
* Deploying workloads fresh to the device rarely caused an issue, but moving some workloads from another node can cause this error when you get a "pod out of memory" error and new pods being constantly generated. This doesn't happen on the other nodes with the same workload so I suspect it's something specific to the Orange Pi 3B and its community Armbian distro. 
    * Note: I'm using this distro because a) it's faster the ones created by Orange Pi, as in faster sysbench and Geekbench results. E.g, 2,200 vs 3500 total sysbench events b) I'm not too keen on downloading a distro that sits on a Google drive. 
* CPU temps were about the same running a workload on Kubernetes vs running the same thing via Portainer. 

#### Raspberry Pi 4Bs 
* No issues save Prometheus errors when I tried to run a 4GB Pi 4B; using 8 GB Rpis feels like a waste to run a few USB or GPIO devices so figuring how to resolve this is on my "nerd to do" list. 
* Temps ranged about 5-7 degrees hotter vs the same workload as docker containers without Kubernetes. 
* I've excluded this device from sharing its storage as part of the longhorn service, meaning it stores all of its data on the control nodes over the network. Hopefully, this should prevent any issues with the SD card wearing out. 


#### General 
* Get as much RAM as you can, the basic setup for this cluster with just the three control nodes, Prometheus for monitoring, ingress and encryption setup/configuration(s), longhorn and Rancher was using close to 40 GB of RAM and that was before I started deploying workloads. I.e. if you're going to follow my setup, I'd suggest maxing out on RAM. 