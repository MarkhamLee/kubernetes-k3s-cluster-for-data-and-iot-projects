## Detailed Updates


### June 27, 2025

This update covers changes made in the last six months, plus provides details on what's being tested/planned for the future. 

I made a significant number of changes since the last update with respect to hardware, storage, cluster management and software, will just summarize the high level items:
* **Hardware Changes:** This past January I replaced most of the hardware after dealing with some occassional issues with the HP G4 and G5 devices; the cluster is becoming my own "personal cloud" for personal and work activities and I needed things to be a bit more robust. 
    * The updated hardware architecture is as follows:
        * Storage nodes replaced with two Minisforum MS-O1 (13900H CPU with 96 GB of DDR5 RAM) designated as data nodes, meaning they're used for shared storage and are the preferred nodes for deploying databases and other data intensive applications: 
            * Longhorn storage runs on these devices and they each have a dedicated 4 TB drive for this purpose. 
            * The node affinity for applications like CouchDB, InfluxDB, Joplin-Server, MariaDB, Postgres, etc., prefer these nodes.
            * I picked these as they have a small footprint, fast processors, and have dual 2.5Gbe in addition to dual 10Gbe SFP+ fiber connections. In a future state they will connect to K3s via the 2.5Gbe ports and talk to each other via the 10Gb ports for data replication + connecting to external storage, but for right now are just using the 2.5Gbe connections. 
        * I added two Minisforum MS-A1s, each with an AMD 7700X processor and 96GB of DDR5 RAM as general purpose worker nodes. 
        * I still have two HP G6 10500 devices in the cluster, I left them in as I was swaping out the other 
        hardware and swapping in the MS-A1s in case the new HW had issues, and never got around to removing them as they never caused any problems. 
        * I replaced the thermal paste on all the servers with Honeywell PTM7950 thermal pads and saw CPU temperature drops between 5-10+ degrees C, prior to the change temps in the 
        * Future hardware items will include:
            * Replacing the Beelinks with devices that support 2.5Gbe and can run dual NVME drives
            * Replacing the HP G6s with two devices on par with the Minisforum devices, one of them will be a general worker node and the other will be a data node that will just run data intensive apps, but can also be a "failover" for Longhorn if one of the existing Longhorn nodes goes offline.
    * I did rebuild the cluster from scratch when I was replacing the hardware and that went flawlessly as I had everything backed up and didn't run into issues restoring things. I did this as the original cluster had the Beelink devices serving as control, storage and worker nodes and *rebuilding right* "felt" cleaner. Additionally, I was having occassional issues with the control nodes being provisioned for Longhorn when the G4 storage node would go down, sometimes getting general workloads, etc. Post rebuild everything deploys/is allocated as it's supposed to be. 

* **Software changes:** have mostly been around deploying more apps and utilizing the data nodes as described above, but there have been some changes related to the software used to manage & monitor the cluster:
    * I'm running an external Portainer instance that I use to "co-manage" the cluster along with Rancher, I rarely use it, it's just a back-up in case I have issues with Rancher. E.g., accidentally letting certificates expire. 
    * I still use Prometheus only it's now deployed via ArgoCD instead of the Prometheus monitoring stack available to deploy via the Rancher UI. It's a more streamlined and less resource intensive implementation.
    * I no longer use the Loki-Stack for logging and have switched to Victoria Logs and Open Telemetry, additionally Victoria logs is used to gather logs from devices/systems outside of the cluster.
    * MinIO is available via TrueNAS but I'm experimenting with replacing it with Garage.
    
* **Networking Updates:**
    * I've deployed Tailscale on my firewall and only access the services running in the cluster (and elsewhere in my homelab) via Tailscale.
    * I have a TrueNAS instance that I use for network storage and it only "talks" to the cluster via Tailscale/
