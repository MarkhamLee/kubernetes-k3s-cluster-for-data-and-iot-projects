## Current Hardware Architecture (July 2025)

After having some problems last fall with the refurbished HP G4s and Raspberry Pi devices having out of RAM errors, randomly shutting down, almost losing my Longhorn storage pool, etc., I decided to take advantage of Christmas sales and upgrade a lot of the hardware in late '24/early '25. While the result arguably falls into the realm of over-engineering, I haven't had to reboot any of the nodes, deal with out of memory errors, storage instability, etc., even after a power outage, everything came back up without a hitch. I.e., as I add more and more apps and increasingly use this cluster to run apps I use daily, it's less over-engineering and more resiliency.


### Overview


After experimenting with various hardware, K3s configurations, hardware roles, etc., I've settled on the following approach that I finished deploying in January of 2025. Some additional details & thoughts:

* Always max out RAM if possible, it will give your apps and containers more room to breathe and you can avoid those nasty issues where you have dozens of failed pods that failed to deploy due to the amount of RAM being reserved to run existing pods.

* I swapped out the traditional thermal paste on all of these devices (save the control nodes) for Honeywell PTM7950 Phase Change thermal pads. To apply it you just put it in the freezer for 10-15 minutes to cool it down, cut into the shape of your CPU, remove the plastic covering and then stick it on. On average I've seen a 5-10 degree C reduction in temperatures and boosts in Geekbench scores of 10-20%.

* Keep a close eye on CPU utilization, temps and the like, it will be your first sign that a machine is overworked, struggling, needs a cooling upgrade, etc.

#### **Dedicated Control Nodes**  

I use labels, taints and tolerations to ensure that these nodes only run the Kubernetes orchestration software, manage the API and run critical network infrastructure like Cert Manager and Traefik. The reason for only running network apps like Traefik on the control nodes, is that if they were comprised those nodes don't access to any apps or their data. While this may seem like overkill when I first setup the cluster I was only running three nodes that did everything, and I'd get concessional instability and the devices I was using (Beelink SER 5s with AMD 5 5560Us) would thermal throttle fairly regularly. I.e., while it seems like overkill, it really isn't. Currently, the control nodes are **three Beelink SER5s running Ryzen 5 5560U chips with 64 GB of RAM**, and despite being a bit overworked in the beginning they've been problem free.

  

Future Plans: replace the Beelink devices with ones with 2.5Gbe networking and that can support two m.2 drives, so I can deploy the OS into a ZFS pool as opposed to a single disk.


#### **Data Nodes**


These nodes are dedicated to running Longhorn for pooled storage and data intensive apps like databases. My thinking was that it just made sense to put things like InfluxDB, MariaDB, Postgres and Redis on the devices that are "closest" to the storage. A 70/30 node affinity is used to ensure the cluster prefers these nodes for data intensive apps, with a similar ratio used for the general workloads/general worker nodes. Currently, the data nodes are two Minisforum MS-O1 mini workstations running Intel 13900H CPUs with 96 GB of RAM; a special feature of these devices is having dual 10Gbe SFP+ ports, which I intend to use to build a dedicated storage network to ensure data replication runs as fast as possible.

Future plans:

* Add a 3rd data node that will step into Longhorn duties if either node goes offline

* Build a dedicated 10Gbe (or faster) storage network for the data nodes + my NAS devices, in order to ensure that data replication happens as fast as possible.

#### **Worker Nodes**

These nodes are just general purpose worker nodes that run anything not designated as a "data intensive" or aren't reserved for the control node. This is managed via using a node affinity with a 70/30 weighting for nodes labeled "k3s_role: x86_worker" vs non control nodes in general. There are currently two sets of control nodes:

* Two Minisforum MS-A1s with AMD Ryzen 7 7700x CPUs and 96GB of RAM
* Two HP G6 Minis running Intel i5-10500 and 64 GB of RAM

My original plan was to remove the HP G6s 30 days after I added the MS-A1s and were sure they were a stable addition to the cluster, but I never got around to it and given that I never had any issues with them prior to the HW upgrades and they've continued to be trouble free I left them. 

Future Plans:
* Replace the two HPs with a single device with 96 GB of RAM and dual 2.5Gbe networking like the MS-A1s
* Once I remove the HPs I'll either use them to build a beta cluster or potentially upgrade the networking to Gbe and redeploy them as control nodes/replace the Beelinks with them.



