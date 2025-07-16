## Architecture Diagrams

This folder will contain the architecture diagrams for the cluster:

* Overall Architecture/Tech Stack 
* Hardware
* Networking 
* Storage

The most recent diagrams will be directly in this folder, while the diagrams for prior iterations, older versions of things, etc, will be in the archive subfolder. 

### Current Architecture as of July 16, 2025

![Cluster Architecture Diagram](k3s_architecture-techstack_July16-2025.png)

A couple of notes: 
* Migrated off of Minio for day to day object storage and secondary backups due to recent product changes, making it harder to depend on for critical items. 
* I've been using Portainer as a secondary/just in case UI Mgt. interface for K3s since January, I rarely use it but it has saved me when I had some cert issues. 
* I use an overlay network for VPN and to access services outside of my home network, added that to the firewall section 
    * This is also how some of the devices that collect climate data but aren't part of the cluster communciate with the cluster. 

