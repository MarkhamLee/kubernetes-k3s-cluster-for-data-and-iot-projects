The current hardware architecture is built around the following principles:

- Dedicated nodes for control, data/storage, and stateless workloads. This separation of concerns provides for a cleaner and easier to manage cluster, while also enabling hardware to be selected and/or customized specifically for their workload type. E.g., Data/storage nodes have significantly faster networking than the control nodes. 
- Data nodes and stateless nodes should each be powerful enough to run the majority of the cluster’s workloads in the event of a major failure.
- Data/storage nodes should support 10 Gbps networking and be purchased new to minimize the risks associated with used hardware.
- The majority of stateless compute capacity should be purchased new, and all stateless nodes should support at least 2.5 Gbps networking.

These principles are the result of running the cluster in several configurations, including a three-node setup, mixed x86 and small ARM devices (Raspberry Pis), and a mix of used/refurbished x86 hardware. Those earlier iterations surfaced reliability, performance, and capacity limits that informed the current design.

All nodes have upgraded cooling via Honeywell PTM7950 thermal pads. This higher‑end thermal interface material reduced average CPU temperatures (on average) by 6° C. 

CPU temperatures, NVME drive temps, and average load are monitored in real time so that hardware issues related to over-allocation can be identified and addressed proactively.

## Control nodes – K3s control plane and networking

The three control nodes run the K3s control plane (for example, the Kubernetes API server) and management-plane workloads such as Rancher. They are also responsible for networking related workloads like cert-manager and Traefik. Using three control nodes enables the cluster to run in a High Availability cluster, if one of the nodes goes down the others can continue to run the cluster. 

## Data nodes – storage and stateful workloads

The data nodes are the only nodes that run Longhorn and thus provide the storage backbone for the entire cluster. They are also the preferred placement for stateful workloads such as MariaDB and PostgreSQL, ensuring that data‑intensive applications run on the machines closest to the storage layer.

Longhorn is restricted to only run on these nodes, while stateful applications are deployed with a 70/30 preference for data nodes over general worker nodes. As long as data nodes have the compute capacity they will receive the stateful workloads, and even some stateless workloads if the stateless worker nodes go down or lack capacity. 

The selected data‑node platform is the Minisforum MS‑01 with the Intel 13900H CPU. This platform combines strong compute capacity with dual 2.5 GbE and 10 GbE networking. The 10 GbE interfaces are intended for a future dedicated Longhorn storage network, so that data replication traffic can run over a high‑bandwidth, isolated path. In line with the hardware principles, these devices are purchased new and are capable of running most cluster workloads if a large portion of the fleet becomes unavailable.

## Worker nodes – stateless workloads

Worker nodes are responsible for everything that does not fall under cluster management, stateful applications, or storage. Typical workloads include agentic AI workloads, data ingestion jobs, and applications such as Grafana and Linkwarden.

The primary worker nodes are two Minisforum MS‑A1 systems. Each MS‑A1 is capable of running most cluster workloads and can host a full‑sized NVIDIA GPU via an external dock, which is useful for AI agents and other accelerated workloads. Both MS‑A1s have dual 2.5 Gbps networking, and their CPUs (currently AMD 7700X) can be upgraded or replaced with other AMD AM5 compatible processor. 

The MS‑A1s are supplemented by two HP G6 mini PCs that have been upgraded to support 2.5 Gbps networking. These units act as “spillover” or pressure‑relief nodes, ensuring that even when the MS‑A1s are heavily utilized, there is still stateless capacity available so those workloads are not scheduled onto the data nodes under normal conditions.

Stateless workloads are deployed with a 70/30 preference for worker nodes over data nodes. This provides flexibility for failover while still keeping storage nodes primarily focused on stateful workloads and the storage subsystem.

## Failure tolerance

A manual failure test was performed to validate how much the cluster could shrink and still remain functional. During that test, both MS‑A1 systems, one HP G6, and one MS‑01 were powered off to simulate a serious hardware or power‑outage event. For approximately three weeks, the cluster was run as usual, with only a few highly available applications scaled down from three replicas to two.

The cluster continued to run reliably during this period, and no significant performance issues were observed beyond the remaining G6 and MS‑01 nodes running hotter than usual. This test demonstrated that the cluster is highly resilient and can tolerate a substantial loss of hardware while remaining operational.

One caveat is that this test was completed before the addition of the agentic workloads, which only run on the MS‑A1 nodes. In a future large‑scale failure or power‑constrained event, it is likely that the cluster would need to be scaled down to a smaller footprint, such as a single MS‑01 and a single MS‑A1. Given that the MS‑A1 is significantly more capable than the HP G6, it is reasonable to expect similar stability, but this scenario should be revalidated as workload profiles evolve.

## Scheduling model

Node labels are used to express cluster roles clearly:

- `k3s_role: data_node` for nodes intended to host stateful workloads.
    
- `k3s_role: x86_worker_node` for nodes intended to host primarily stateless workloads.
    
- `agent_type: x86_worker` for both groups, allowing broader placement targeting when needed.

- `k3s_role: control_node` combined with the `taint node-role.kubernetes.io/master=true:NoSchedule` ensures that control nodes are excluded from general workload scheduling. Only control-plane–related applications (such as Traefik) that have a matching toleration for this taint can be scheduled onto the control nodes.

Workloads are deployed using a 70/30 weighting for their preferred node type versus general worker nodes. For example, a database workload is configured with a 70% preference for data nodes and a 30% allowance for general worker nodes. This keeps scheduling flexible enough for failover while still expressing strong placement intent.