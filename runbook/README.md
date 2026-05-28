## K3s Runbook

The documentation in this folder covers the following topics:
* Day 1, Day 2 style tasks after you get the cluster up and running (W.I.P)
* Preparation style tasks, like how to [configure your network](networking/external_preparation.md) prior to creating the cluster 
* Resolving issue that may occur once the cluster is running related to networking, storage, and managing hardware. 

## Current Content

### Databases
* [Fixing PVC issues](databases/postgres/fixing_postgres_pvc.md) when your database grows too big for its volume claim 

### Hardware
* [Adding hardware](hardware/adding_worker_nodes.md) to a Rancher managed cluster that was originally built with Ansible 

### Networking
* Setting up external networking resources like [pfsense](networking/pfSense)
* Fixing [DNS problems](networking/fixing_dns_problems.md) on the individual nodes 

### Storage
* [Fixing Volume attach issues](storage/fixing_volume_attach_errors.md)
* [Fixing PVC claim size issues](storage/updating_pvc_claim_size.md) 