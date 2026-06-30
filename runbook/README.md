## K3s Runbook

The documentation in this folder covers the following topics:
* Day 1, Day 2 style tasks after you get the cluster up and running (W.I.P)
* Preparation style tasks, like how to [configure your network](networking/external_preparation.md) prior to creating the cluster 
* Resolving issue that may occur once the cluster is running related to networking, storage, and managing hardware. 

## Current Content

### Databases
* [Fixing PVC issues](databases/postgres/fixing_postgres_pvc.md) when your Postgres database grows too big for its volume claim 

### Hardware
* [Adding hardware](hardware/adding_worker_nodes.md) to a Rancher managed cluster that was originally built with Ansible 

### General Networking

Many of the networking topics are external to K3s as they cover networking infrastructure critical for a K3s cluster to function, but also protect the network in general and facilitate the deployment of services on servers external to K3s. 

* Setting up [OPNsense](networking/opnsense/readme.md)
* Setting up [Technitium](networking/technitium/readme.md) for DNS, Domain Filtering and DHCP 
* Deploying [Pi-Hole](networking/pi-hole/readme.md) 

### Kubernetes Networking
* Fixing [DNS problems](networking/fixing_dns_problems.md) on the individual K3s nodes

### K3s Storage via Longhorn
* [Fixing Volume attach issues](storage/fixing_volume_attach_errors.md)
* [Fixing PVC claim size issues](storage/updating_pvc_claim_size.md) 

### Archived Items 

Useful documentation but not currently being used by the private cloud, so it's probably out of date or will be in the future. 

* Setting up [pfsense](networking/pfSense/readme.md)